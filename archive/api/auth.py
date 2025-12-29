from fastapi import APIRouter, HTTPException, status, Depends, Form
from pydantic import BaseModel
from typing import Optional
from services.auth_service import create_user, authenticate_user, get_user

router = APIRouter()

class UserCreateRequest(BaseModel):
    username: str
    password: str
    enable_2fa: Optional[bool] = False

class UserLoginRequest(BaseModel):
    username: str
    password: str
    token: Optional[str] = None  # For 2FA

@router.post("/register")
def register_user(request: UserCreateRequest):
    try:
        user = create_user(request.username, request.password, request.enable_2fa)
        result = {"username": user["username"], "2fa_enabled": user["2fa_enabled"]}
        if user.get("2fa_enabled"):
            result["2fa_uri"] = user["2fa_uri"]  # QR code URI for authenticator app
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(request: UserLoginRequest):
    user = get_user(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
    if user.get("2fa_enabled") and not request.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="2FA token required."
        )
    if not authenticate_user(request.username, request.password, request.token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or 2FA token.")
    return {"message": "Login successful!"}
