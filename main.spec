# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['backend/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend/photos/*', 'backend/photos'),
        ('backend/transcripts.db', 'backend'),
        ('venv311/lib/python3.11/site-packages/es_core_news_sm/*', 'es_core_news_sm'),
        # Agrega aquí otros recursos o modelos de spaCy si los usas
    ],
    hiddenimports=[
        'plotly',
        'pandas',
        'scipy',
        'sklearn',
        'spacy',
        # Agrega aquí otros módulos si los necesitas
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
