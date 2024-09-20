# -*- mode: python ; coding: utf-8 -*-
added_files = [
    ('C:/Users/alexm/PycharmProjects/GUI/config/*.json', 'config'),
    ('C:/Users/alexm/PycharmProjects/GUI/Icons/*.png', 'Icons'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/frog-egg-counter', 'models'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/frog-egg-counter/*.json','models/frog-egg-counter'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/frog-egg-counter/*.h5','models/frog-egg-counter'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/Oyster_model/*.json','models/Oyster_model'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/Oyster_model/*.h5','models/Oyster_model'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/Xenopus Frog Embryos Classification Model/*.json','models/Xenopus Frog Embryos Classification Model'),
    ('C:/Users/alexm/PycharmProjects/GUI/models/Xenopus Frog Embryos Classification Model/*.h5','models/Xenopus Frog Embryos Classification Model'),
    ('C:/Users/alexm/PycharmProjects/GUI/docs/*.txt','docs')
]

a = Analysis(
    ['App.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='App',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='App',
)
