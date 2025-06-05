a = Analysis(
    ['./src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('models/xenopus-4-class', 'models/xenopus-4-class'),
        ('models/oyster_4-6mm', 'models/oyster_4-6mm'),
        ('models/oyster_2-4mm', 'models/oyster_2-4mm'),
        ('models/frog-egg-counter', 'models/frog-egg-counter'),
        ('models/Oyster_model', 'models/Oyster_model'),
        ('annotations', 'annotations'),
        ('excel', 'excel'),
        ('data', 'data'),
        # 'images' directory is created at runtime
    ],
    hiddenimports=['PIL._tkinter_finder'],
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
    name='DeVision',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='DeVision.app',
    icon=None,
    bundle_identifier=None,
)
