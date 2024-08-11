import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Hiba történt a parancs futtatása közben: {command}")
        print(f"Hibaüzenet: {stderr}")
        sys.exit(1)
    return stdout


def get_platform():
    if sys.platform.startswith('darwin'):
        return 'darwin'
    elif sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('win'):
        return 'windows'
    else:
        raise OSError("Nem támogatott operációs rendszer")


def create_virtual_env():
    print("Virtuális környezet létrehozása...")
    run_command("python -m venv venv")
    if sys.platform.startswith('win'):
        return "venv\\Scripts\\activate"
    return "source venv/bin/activate"


def install_dependencies(activate_cmd):
    print("Függőségek telepítése...")
    run_command(f"{activate_cmd} && pip install -r requirements.txt")
    run_command(f"{activate_cmd} && pip install pyinstaller")


def build_application(activate_cmd, platform):
    print(f"Alkalmazás buildelése {platform} platformra...")
    icon_path = "Icons/AppIcon.icns" if platform == "darwin" else "Icons/AppIcon.ico"
    separator = ":" if platform != "windows" else ";"

    command = f"{activate_cmd} && pyinstaller --name=WarframeInfoHub " \
              f"--onefile --windowed " \
              f"--add-data \"gui{separator}gui\" " \
              f"--add-data \"gui/Script{separator}gui/Script\" " \
              f"--add-data \"gui/Styles{separator}gui/Styles\" " \
              f"--add-data \"README.md{separator}.\" " \
              f"--icon={icon_path} " \
              f"--exclude-module=tkinter " \
              f"--exclude-module=matplotlib " \
              f"--exclude-module=PyQt5 " \
              f"--exclude-module=numpy " \
              f"--exclude-module=pandas " \
              f"--exclude-module=scipy " \
              f"--exclude-module=PIL " \
              f"--exclude-module=PySimpleGUI " \
              f"--exclude-module=pytest " \
              f"--exclude-module=IPython " \
              f"--exclude-module=notebook " \
              f"--exclude-module=sqlite3 " \
              f"--exclude-module=email " \
              f"--exclude-module=html " \
              f"--exclude-module=http " \
              f"--exclude-module=multiprocessing " \
              f"--exclude-module=xml " \
              f"--exclude-module=jsonschema " \
              f"--noupx " \
              f"--clean " \
              f"--strip " \
              f"main_qt6.py"

    if platform == "windows":
        command += f" --add-binary \"venv\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\Qt6Core.dll{separator}PyQt6\\Qt6\\bin\" " \
                   f"--add-binary \"venv\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\Qt6Gui.dll{separator}PyQt6\\Qt6\\bin\" " \
                   f"--add-binary \"venv\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\Qt6Widgets.dll{separator}PyQt6\\Qt6\\bin\" "

    run_command(command)


def optimize_size():
    print("Fájlméret optimalizálása...")
    if sys.platform.startswith('win'):
        upx_command = "upx --best --lzma dist\\WarframeInfoHub.exe"
    else:
        upx_command = "upx --best --lzma dist/WarframeInfoHub"
    run_command(upx_command)


def cleanup():
    print("Takarítás...")
    shutil.rmtree("build", ignore_errors=True)
    if os.path.exists("WarframeInfoHub.spec"):
        os.remove("WarframeInfoHub.spec")


def main():
    platform = get_platform()
    print(f"Build folyamat indítása {platform} platformra...")

    activate_cmd = create_virtual_env()
    install_dependencies(activate_cmd)
    build_application(activate_cmd, platform)
    optimize_size()
    cleanup()

    executable_path = "dist\\WarframeInfoHub.exe" if platform == "windows" else "dist/WarframeInfoHub"
    size_bytes = os.path.getsize(executable_path)
    size_mb = size_bytes / (1024 * 1024)

    print(f"Build folyamat befejezve {platform} platformra.")
    print(f"A végrehajtható fájl mérete: {size_mb:.2f} MB")
    print(f"A végrehajtható fájl itt található: {executable_path}")


if __name__ == "__main__":
    main()