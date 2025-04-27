# -*- mode: python ; coding: utf-8 -*-
import os

# Create a runtime hook to help with path resolution
with open('runtime_hook.py', 'w') as f:
    f.write('''
import os
import sys
from pathlib import Path

# Make sure all required directories exist, regardless of compilation state
def ensure_app_directories():
    """Create all required application directories if they don't exist"""
    app_dirs = ['models', 'config', 'annotations', 'excel', 'data', 'images']
    
    # Determine base path based on whether we're frozen or not
    if getattr(sys, 'frozen', False):
        # Running as bundled exe
        base_path = Path(sys._MEIPASS)
    else:
        # Running as script
        base_path = Path(os.path.abspath('.'))
    
    # Create directories and set environment variables
    for dir_name in app_dirs:
        # Set environment variable
        data_dir = base_path / dir_name
        env_var = f'DEVISION_{dir_name.upper()}'
        if not os.environ.get(env_var):
            os.environ[env_var] = str(data_dir)
        
        # Always create these directories
        if dir_name in ['annotations', 'excel', 'data', 'images']:
            try:
                # Handle file/directory conflicts
                if os.path.isfile(data_dir):
                    print(f"Found file instead of directory at {data_dir}, removing it")
                    os.remove(data_dir)
                
                os.makedirs(data_dir, exist_ok=True)
                print(f"Ensured directory exists: {data_dir}")
            except Exception as e:
                print(f"Warning: Could not create directory {data_dir}: {str(e)}")

# Call the function to ensure directories exist
ensure_app_directories()
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
        # 'images' directory is created at runtime
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
