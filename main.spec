# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Collect PyQt5 data files and libraries
pyqt5_data = collect_data_files('PyQt5')
pyqt5_binaries = collect_dynamic_libs('PyQt5')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt5_binaries,
    datas=pyqt5_data + [
        ('API_Warframe_Cross_GUI/gui', 'gui'),
        ('API_Warframe_Cross_GUI/gui/styles', 'gui/styles'),
        ('API_Warframe_Cross_GUI/gui/Script', 'gui/Script'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngine',
        'PyQt5.QtNetwork',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtSvg',
        'PyQt5.QtSerialPort',
        'bcrypt'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WarframeApp',
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
    icon='path/to/your/icon.ico'  # Add your icon path here
)