# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_qt5.py'],
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
    a.binaries,
    a.datas,
    [],
    name='main_qt5',
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
    name='main_qt5.app',
    icon=None,
    bundle_identifier=None,
)
