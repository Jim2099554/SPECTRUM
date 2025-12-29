from fastapi import APIRouter, HTTPException, Request

auth_router = APIRouter()

import smtplib
from email.mime.text import MIMEText


@auth_router.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    # Usuario de prueba: admin@example.com / admin123
    if email == "admin@example.com" and password == "admin123":
        from backend.core.auth.verification import generate_code, send_email, verification_codes, CODE_EXPIRY_SECONDS, lock
        import time
        code = generate_code()
        expiry = time.time() + CODE_EXPIRY_SECONDS
        with lock:
            verification_codes[email] = {"code": code, "expiry": expiry}
        try:
            send_email(email, code)
        except Exception as e:
            print("Error enviando correo:", e)
            raise HTTPException(status_code=500, detail="No se pudo enviar el correo de 2FA")
        return {"requires_2fa": True, "message": "Código enviado"}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")
