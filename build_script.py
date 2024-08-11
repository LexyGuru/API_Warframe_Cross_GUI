import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Hiba történt a parancs futtatása közben: {command}")
        print(f"Hibaüzenet: {stderr.decode('utf-8')}")
        sys.exit(1)
    return stdout.decode('utf-8')


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
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    print(f"Aktiválja a virtuális környezetet a következő paranccsal: {activate_cmd}")
    return activate_cmd


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
              f"--exclude-module=PySimpleGUI " \
              f"--exclude-module=pytest " \
              f"--exclude-module=docutils " \
              f"--exclude-module=PIL " \
              f"--exclude-module=numpy " \
              f"--exclude-module=axios " \
              f"--clean "

    if platform == "windows":
        command += f"--add-binary \"venv\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\Qt6Core.dll{separator}PyQt6\\Qt6\\bin\" " \
                   f"--add-binary \"venv\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\Qt6Gui.dll{separator}PyQt6\\Qt6\\bin\" " \
                   f"--add-binary \"venv\\Lib\\site-packages\\PyQt6\\Qt6\\bin\\Qt6Widgets.dll{separator}PyQt6\\Qt6\\bin\" "

    command += "main_qt6.py"
    run_command(command)


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
    cleanup()

    print(f"Build folyamat befejezve {platform} platformra.")
    print("A végrehajtható fájl a 'dist' könyvtárban található.")


if __name__ == "__main__":
    main()