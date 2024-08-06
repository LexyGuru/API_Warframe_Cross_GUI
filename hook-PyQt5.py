from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

datas = collect_data_files('PyQt5')
binaries = collect_dynamic_libs('PyQt5')

hiddenimports = [
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebEngine',
    'PyQt5.QtNetwork',
    'PyQt5.QtPrintSupport',
    'PyQt5.QtSvg',
    'PyQt5.QtSerialPort'
]