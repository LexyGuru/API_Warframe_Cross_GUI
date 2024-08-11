# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_qt6.py'],
    pathex=[],
    binaries=[],
    datas=[('gui', 'gui'), ('gui/Script', 'gui/Script'), ('gui/Styles', 'gui/Styles')],
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
    name='main_qt6',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Icons/AppIcon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main_qt6',
)
app = BUNDLE(
    coll,
    name='main_qt6.app',
    icon='Icons/AppIcon.icns',
    bundle_identifier=None,
)
