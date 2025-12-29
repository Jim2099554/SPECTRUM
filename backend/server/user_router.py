from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

user_router = APIRouter()

# Modelo simple de usuario
class User(BaseModel):
    id: int
    email: str
    is_admin: bool

# Simulación de base de datos en memoria
users_db = [
    User(id=1, email="admin@example.com", is_admin=True),
    User(id=2, email="usuario1@sentinela.local", is_admin=False),
    User(id=3, email="usuario2@sentinela.local", is_admin=False),
]

@user_router.get("/users", response_model=List[User])
def get_users():
    return users_db

@user_router.post("/users", response_model=User)
def add_user(user: User):
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    user.id = max(u.id for u in users_db) + 1 if users_db else 1
    users_db.append(user)
    return user

@user_router.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    for u in users_db:
        if u.id == user_id:
            users_db = [usr for usr in users_db if usr.id != user_id]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
