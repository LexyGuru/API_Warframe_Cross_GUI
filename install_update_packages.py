# Copyright (c) 2024 LexyGuru
# This file is part of the API_Warframe_Cross_GUI project, licensed under the MIT License.
# For the full license text, see the LICENSE file in the project root.

import subprocess
import sys

def update_packages():
    packages = """
aiohappyeyeballs==2.3.4
aiohttp==3.10.0
aiosignal==1.3.1
altgraph==0.17.4
attrs==23.2.0
axios==0.4.0
bcrypt==4.2.0
certifi==2024.7.4
charset-normalizer==3.3.2
click==8.1.7
frozenlist==1.4.1
idna==3.7
lxml==5.2.2
macholib==1.16.3
Markdown==3.6
markdown-it-py==3.0.0
mdurl==0.1.2
modulegraph==0.19.6
multidict==6.0.5
packaging==24.1
pip==24.2
prettytable==3.10.2
py2app==0.28.8
pyasn1==0.6.0
Pygments==2.18.0
pyinstaller==6.9.0
pyinstaller-hooks-contrib==2024.7
PyQt5==5.15.11
PyQt5-Qt5==5.15.14
PyQt5_sip==12.15.0
PyQt6==6.7.1
PyQt6-Qt6==6.7.2
PyQt6_sip==13.8.0
PyQt6-WebEngine==6.7.0
PyQt6-WebEngine-Qt6==6.7.2
PyQt6-WebEngineSubwheel-Qt6==6.7.2
PyQtWebEngine==5.15.7
PyQtWebEngine-Qt5==5.15.14
PySimpleGUI==5.0.6
requests==2.32.3
rich==13.7.1
rsa==4.9
setuptools==72.1.0
urllib3==2.2.2
wcwidth==0.2.13
yarl==1.9.4
    """.strip().split('\n')

    for package in packages:
        package_name = package.split('==')[0]
        print(f"Frissítés: {package_name}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
        except subprocess.CalledProcessError as e:
            print(f"Hiba történt a(z) {package_name} frissítése közben: {e}")

if __name__ == "__main__":
    update_packages()