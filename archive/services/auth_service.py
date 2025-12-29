import re
import secrets
import string
from typing import Optional
from passlib.context import CryptContext
import pyotp

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password complexity requirements
def validate_password(password: str) -> bool:
    # Minimum 15 characters, at least one uppercase, one lowercase, one digit, one special char
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{15,}$'
    return re.match(pattern, password) is not None

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate TOTP secret
def generate_2fa_secret() -> str:
    return pyotp.random_base32()

# Get TOTP provisioning URI for QR code
def get_2fa_provisioning_uri(username: str, secret: str, issuer: str = "SpectrumApp") -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)

# Verify TOTP code
def verify_2fa_token(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

# Example user storage (replace with DB integration in production)
_users = {}

# Create a new user
def create_user(username: str, password: str, enable_2fa: bool = False) -> Optional[dict]:
    if username in _users:
        raise ValueError("Username already exists.")
    if not validate_password(password):
        raise ValueError("Password does not meet complexity requirements.")
    hashed_pw = hash_password(password)
    user = {"username": username, "password": hashed_pw, "2fa_enabled": enable_2fa}
    if enable_2fa:
        secret = generate_2fa_secret()
        user["2fa_secret"] = secret
        user["2fa_uri"] = get_2fa_provisioning_uri(username, secret)
    _users[username] = user
    return user

# Authenticate user (with optional 2FA)
def authenticate_user(username: str, password: str, token: Optional[str] = None) -> bool:
    user = _users.get(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    if user.get("2fa_enabled"):
        if not token or not verify_2fa_token(user["2fa_secret"], token):
            return False
    return True

# For demonstration/testing purposes only (not for production)
def get_user(username: str) -> Optional[dict]:
    return _users.get(username)
