"""
Script para actualizar la contraseña del usuario admin@example.com a 'admin123'
"""
import os
import sys
import hashlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from db import Base, engine, SessionLocal
from sqlalchemy.exc import NoResultFound

def update_admin_password():
    email = "admin@example.com"
    new_password = "admin123"
    password_hash = hashlib.sha512(new_password.encode()).hexdigest()

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, index=True)
        password = Column(String)
        is_admin = Column(Boolean, default=False)
        is_active = Column(Boolean, default=True)

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user:
            print(f"❌ No se encontró el usuario '{email}' en la base de datos.")
            return
        user.password = password_hash
        db.commit()
        print(f"✅ Contraseña de '{email}' actualizada correctamente.")
    except Exception as e:
        print(f"❌ Error actualizando contraseña: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_admin_password()
