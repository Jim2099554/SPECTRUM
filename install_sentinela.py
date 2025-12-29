#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil

REQUIRED_PYTHON = (3, 9)
RECOMMENDED_PYTHON = (3, 10)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')
REQUIREMENTS_FILE = os.path.join(os.path.dirname(__file__), 'requirements.txt')


def check_python_version():
    print(f"\n[1/6] Verificando versión de Python...")
    version = sys.version_info
    print(f"  Versión detectada: {version.major}.{version.minor}.{version.micro}")
    if version < REQUIRED_PYTHON:
        print(f"[ERROR] Se requiere Python >= {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}. Por favor, actualiza Python.")
        sys.exit(1)
    elif version < RECOMMENDED_PYTHON:
        print(f"[ADVERTENCIA] Se recomienda Python >= {RECOMMENDED_PYTHON[0]}.{RECOMMENDED_PYTHON[1]} para máximo soporte.")
    else:
        print("  ✔ Versión de Python adecuada.")

def check_node_version():
    print(f"\n[2/6] Verificando versión de Node.js...")
    try:
        output = subprocess.check_output(['node', '--version'], stderr=subprocess.STDOUT).decode().strip()
        version_str = output.lstrip('v')
        major, minor, *_ = map(int, version_str.split('.'))
        print(f"  Versión detectada: {version_str}")
        if major < 18:
            print("[ERROR] Se requiere Node.js >= 18. Por favor, actualiza Node.js.")
            sys.exit(1)
        else:
            print("  ✔ Versión de Node.js adecuada.")
    except Exception:
        print("[ERROR] Node.js no está instalado o no está en el PATH. Instálalo antes de continuar.")
        sys.exit(1)

def ask_external_db():
    print(f"\n[3/6] Configuración de base de datos externa para PPL info")
    use_external = input("¿Quieres usar una base de datos externa para datos y fotos de PPL? (s/n): ").strip().lower()
    if use_external == 's':
        db_url = input("  Ingresa la URL de conexión (por ejemplo, postgresql://user:pass@host:port/db): ").strip()
        photo_api = input("  Ingresa el endpoint o ruta para obtener fotos de PPL (puede ser API REST o ruta de red): ").strip()
        # Prueba conexión a base de datos externa
        print("  Probando conexión a la base de datos externa...")
        try:
            from sqlalchemy import create_engine
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            print("    ✔ Conexión a base de datos exitosa.")
        except Exception as e:
            print(f"    [ERROR] No se pudo conectar a la base de datos externa: {e}")
            print("    Verifica la URL y credenciales antes de continuar.")
            sys.exit(1)
        # Prueba conexión al API/fotos
        import requests
        print("  Probando acceso a fotos de PPL...")
        try:
            resp = requests.head(photo_api) if photo_api else None
            if resp is not None and resp.status_code == 200:
                print("    ✔ Endpoint de fotos accesible.")
            elif resp is not None:
                print(f"    [ERROR] El endpoint de fotos respondió status {resp.status_code}")
                sys.exit(1)
            else:
                print("    [ADVERTENCIA] No se proporcionó endpoint de fotos, omitiendo prueba.")
        except Exception as e:
            print(f"    [ERROR] No se pudo acceder al endpoint de fotos: {e}")
            sys.exit(1)
        # Guardar en .env o mostrar instrucciones
        with open('.env', 'a') as f:
            f.write(f"\nPPL_DB_URL={db_url}\nPPL_PHOTO_API={photo_api}\n")
        print("  ✔ Configuración guardada en .env. El backend está listo para consumir estos endpoints.")
    else:
        print("  Se usará la base de datos local por defecto para PPL info y fotos.")

def install_python_deps():
    print(f"\n[4/6] Instalando dependencias de Python (backend)...")
    # Opción de entorno virtual
    use_venv = input("¿Deseas crear un entorno virtual para Python? (s/n): ").strip().lower()
    if use_venv == 's':
        venv_dir = os.path.join(os.path.dirname(__file__), 'venv')
        if not os.path.exists(venv_dir):
            subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
            print(f"  ✔ Entorno virtual creado en {venv_dir}")
        # Activar entorno virtual
        if platform.system() == 'Windows':
            activate_cmd = os.path.join(venv_dir, 'Scripts', 'activate')
        else:
            activate_cmd = f"source {os.path.join(venv_dir, 'bin', 'activate')}"
        print(f"  [INFO] Activa el entorno virtual ejecutando: {activate_cmd}")
        pip = os.path.join(venv_dir, 'Scripts' if platform.system() == 'Windows' else 'bin', 'pip')
    else:
        pip = shutil.which('pip') or shutil.which('pip3')
    if not pip:
        print("[ERROR] pip no encontrado. Instálalo antes de continuar.")
        sys.exit(1)
    subprocess.check_call([pip, 'install', '-r', REQUIREMENTS_FILE])
    print("  ✔ Dependencias de Python instaladas.")

def install_node_deps():
    print(f"\n[5/6] Instalando dependencias de Node.js (frontend)...")
    if not os.path.exists(os.path.join(FRONTEND_DIR, 'package.json')):
        print(f"[ERROR] No se encontró package.json en {FRONTEND_DIR}")
        sys.exit(1)
    subprocess.check_call(['npm', 'install'], cwd=FRONTEND_DIR)
    print("  ✔ Dependencias de Node.js instaladas.")

def final_instructions():
    print(f"\n[6/6] Instalación completada.")
    print("\nPara iniciar el backend ejecuta:")
    print("  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000\n")
    print("Para iniciar el frontend ejecuta:")
    print("  npm run dev   # dentro de la carpeta frontend\n")
    print("Revisa el archivo .env para ajustar variables de entorno si usas bases de datos externas.\n")

def main():
    print("\n==============================")
    print("  INSTALADOR SENTINELA (Python)")
    print("==============================\n")
    check_python_version()
    check_node_version()
    ask_external_db()
    install_python_deps()
    install_node_deps()
    final_instructions()

if __name__ == '__main__':
    main()
