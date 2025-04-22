# -*- mode: python ; coding: utf-8 -*-
import os

# Create a runtime hook to help with path resolution
with open('runtime_hook.py', 'w') as f:
    f.write('''
import os
import sys
from pathlib import Path

# Make sure the bundled data directories are accessible
def add_data_dir(dir_name):
    if getattr(sys, 'frozen', False):
        # Running as bundled exe
        base_path = Path(sys._MEIPASS)
        data_dir = base_path / dir_name
        if not os.environ.get(f'DEVISION_{dir_name.upper()}'):
            os.environ[f'DEVISION_{dir_name.upper()}'] = str(data_dir)
        # Create directory if it doesn't exist
        if dir_name in ['annotations', 'excel', 'data', 'images']:
            os.makedirs(data_dir, exist_ok=True)
    else:
        # Running as script
        base_path = Path(os.path.abspath('.'))
        data_dir = base_path / dir_name
        if not os.environ.get(f'DEVISION_{dir_name.upper()}'):
            os.environ[f'DEVISION_{dir_name.upper()}'] = str(data_dir)
        # Create directory if it doesn't exist
        if dir_name in ['annotations', 'excel', 'data', 'images']:
            os.makedirs(data_dir, exist_ok=True)

add_data_dir('models')
add_data_dir('config')
add_data_dir('annotations')
add_data_dir('excel')
add_data_dir('data')
add_data_dir('images')
''')

a = Analysis(
    ['./src/Pages.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('models/xenopus-4-class', 'models/xenopus-4-class'),
        ('models/oyster_4-6mm', 'models/oyster_4-6mm'),
        ('models/oyster_2-4mm', 'models/oyster_2-4mm'),
        ('models/frog-egg-counter', 'models/frog-egg-counter'),
        ('models/Xenopus Frog Embryos Classification Model', 'models/Xenopus Frog Embryos Classification Model'),
        ('models/Oyster_model', 'models/Oyster_model'),
        ('annotations', 'annotations'),
        ('excel', 'excel'),
        ('data', 'data'),
        ('images', 'images'),
    ],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
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
