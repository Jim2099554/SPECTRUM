# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file para SENTINELA - Versión Administrador Global
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Increase recursion limit for large projects with many dependencies
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

# Datos adicionales a incluir
datas = [
    ('backend/data', 'backend/data'),
    ('backend/config', 'backend/config'),
    ('backend/photos', 'backend/photos'),
    ('backend/transcripts', 'backend/transcripts'),
    ('backend/audios', 'backend/audios'),
    ('backend/client', 'backend/client'),
]

# Incluir modelos de spaCy
datas += collect_data_files('es_core_news_sm')

# Módulos ocultos necesarios
hiddenimports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'passlib.handlers.bcrypt',
    'sqlalchemy.sql.default_comparator',
    'backend.core.auth.verification',
    'backend.core.auth.user_manager',
    'backend.core.database.database_manager',
    'backend.core.licensing.license_manager',
    'backend.server.user_router',
    'backend.server.dangerous_words_router',
    'backend.server.report_router',
    'backend.server.database_config_router',
    'backend.server.license_router',
    'google.cloud.speech',
    'google.cloud.storage',
]

a = Analysis(
    ['backend/main_admin.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SENTINELA_Admin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icono_Sentinela.ico' if sys.platform == 'win32' else 'icon-Sentinela.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SENTINELA_Admin',
)
