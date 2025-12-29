import random
import smtplib
import threading
import time
import os
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException, Request

# =========================
# Configuración flexible SMTP por entorno
# =========================
# Variables de entorno soportadas:
#   SMTP_HOST: host SMTP ("mailhog", "smtp.gmail.com", etc)
#   SMTP_PORT: puerto SMTP (1025 para Mailhog, 587 para Gmail)
#   SMTP_USER: usuario SMTP (solo para Gmail/empresarial)
#   SMTP_PASS: contraseña SMTP (o app password)
#   SMTP_TLS: "true" para activar STARTTLS (Gmail/empresarial)
#   SENDER_EMAIL: correo remitente
CODE_LENGTH = 8
CODE_EXPIRY_SECONDS = 120  # 2 minutos
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_TLS = os.getenv("SMTP_TLS", "false").lower() == "true"
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@sentinela.local")

# Almacenamiento en memoria (usuario: {code, expiry})
verification_codes = {}
lock = threading.Lock()

def generate_code():
    code = str(random.randint(10**(CODE_LENGTH-1), 10**CODE_LENGTH - 1))
    print(f"[2FA] Generando código: {code}")
    return code

def send_email(recipient, code):
    subject = "Tu código de verificación SENTINELA"
    body = f"Tu código de verificación es: {code}\nEste código expira en 2 minutos."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        if SMTP_TLS:
            server.starttls()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SENDER_EMAIL, [recipient], msg.as_string())

router = APIRouter()

@router.post("/request-2fa")
async def request_2fa(request: Request):
    print("[2FA] Solicitud de código 2FA recibida")
    data = await request.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email requerido")
    code = generate_code()
    expiry = time.time() + CODE_EXPIRY_SECONDS
    with lock:
        verification_codes[email] = {"code": code, "expiry": expiry}
    try:
        send_email(email, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enviando email: {e}")
    return {"message": "Código enviado"}

import jwt
from datetime import datetime, timedelta

from backend.config import JWT_SECRET as SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

@router.post("/verify-2fa")
async def verify_2fa(request: Request):
    data = await request.json()
    email = data.get("email")
    code = data.get("code")
    if not email or not code:
        raise HTTPException(status_code=400, detail="Email y código requeridos")
    with lock:
        entry = verification_codes.get(email)
        if not entry or entry["expiry"] < time.time():
            verification_codes.pop(email, None)
            raise HTTPException(status_code=401, detail="Código expirado o inválido")
        if entry["code"] != code:
            raise HTTPException(status_code=401, detail="Código incorrecto")
        verification_codes.pop(email, None)
    # Generar access_token JWT válido por 10 minutos
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

