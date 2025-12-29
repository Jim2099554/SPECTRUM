"""
Script para crear un usuario administrador en la base de datos de SENTINELA
Usuario: admin
Contraseña: S3ntinel@ismypass (hash SHA512)
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import hashlib
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from db import Base, engine, SessionLocal
from sqlalchemy.exc import IntegrityError

# Ajusta el nombre de la tabla y los campos según tu modelo real
def crear_admin():
    email = "admin@example.com"
    password = "admin123"
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    is_admin = True
    is_active = True

    # Modelo de usuario dinámico (ajusta si tienes un modelo User definido)
    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, index=True)
        password = Column(String)
        is_admin = Column(Boolean, default=False)
        is_active = Column(Boolean, default=True)

    # Crea la tabla si no existe
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Verifica si ya existe
        existente = db.query(User).filter_by(email=email).first()
        if existente:
            print(f"⚠️ El usuario '{email}' ya existe.")
            return
        nuevo = User(email=email, password=password_hash, is_admin=is_admin, is_active=is_active)
        db.add(nuevo)
        db.commit()
        print(f"✅ Usuario admin creado exitosamente: {email}")
    except IntegrityError:
        print("❌ Error: El usuario ya existe o hay un problema de integridad.")
    finally:
        db.close()

if __name__ == "__main__":
    crear_admin()
