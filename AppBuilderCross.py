# Copyright (c) 2024 LexyGuru
# This file is part of the API_Warframe_Cross_GUI project, licensed under the MIT License.
# For the full license text, see the LICENSE file in the project root.

import sys
import os
import platform
import subprocess
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
import ssl
import certifi
import importlib
import tempfile
import logging
import atexit
import shutil

# Naplózás beállítása
logging.basicConfig(filename='app_log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

GITHUB_RAW_URL = "https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/"
LOCK_FILE = os.path.join(tempfile.gettempdir(), 'appbuilder_cross.lock')

ssl_context = ssl.create_default_context(cafile=certifi.where())


def check_temp_directory():
    temp_dir = tempfile.gettempdir()
    try:
        test_file = os.path.join(temp_dir, 'test_write.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        logging.info(f"Temporális könyvtár írható: {temp_dir}")
        return True
    except Exception as e:
        logging.error(f"Hiba a temporális könyvtár írásakor: {str(e)}")
        return False


def is_already_running():
    if not check_temp_directory():
        return False
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            if pid_exists(pid):
                logging.info(f"Folyamat fut a következő PID-del: {pid}")
                return True
            else:
                logging.info(f"Folyamat nem fut a következő PID-del: {pid}, lock fájl törlése")
                os.remove(LOCK_FILE)
        return False
    except Exception as e:
        logging.error(f"Hiba történt a lock fájl ellenőrzésekor: {str(e)}")
        return False


def pid_exists(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def create_lock_file():
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        logging.info(f"Lock fájl létrehozva: {LOCK_FILE}")
        atexit.register(remove_lock_file)
    except Exception as e:
        logging.error(f"Hiba történt a lock fájl létrehozásakor: {str(e)}")


def remove_lock_file():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
            logging.info(f"Lock fájl törölve: {LOCK_FILE}")
    except Exception as e:
        logging.error(f"Hiba történt a lock fájl törlésekor: {str(e)}")


class WorkerThread(threading.Thread):
    def __init__(self, queue, update_callback):
        threading.Thread.__init__(self)
        self.queue = queue
        self.update_callback = update_callback
        self.running = True

    def run(self):
        steps = [
            ("Rendszer ellenőrzése", self.check_system),
            ("Python ellenőrzése", self.check_python),
            ("GitHub fájlok ellenőrzése", self.check_github_files),
            ("Függőségek telepítése", self.check_and_install_dependencies),
            ("Alkalmazás építése", self.build_application)
        ]
        total_steps = len(steps)
        for i, (step_name, step_function) in enumerate(steps):
            if not self.running:
                break
            self.update_callback(f"{step_name}...", (i / total_steps) * 100)
            step_function()
        self.update_callback("Folyamat befejezve", 100)

    def check_system(self):
        system = platform.system()
        architecture = platform.machine()
        arch = self.get_architecture(system, architecture)
        self.update_callback(f"Operációs rendszer: {system}, Architektúra: {arch}", 20)

    def get_architecture(self, system, architecture):
        if system == "Windows":
            return {"AMD64": "Win64", "x86": "Win32", "ARM64": "ARM64", "AARCH64": "ARM64"}.get(architecture, "Unknown")
        elif system == "Linux":
            return "ARM64" if "arm" in architecture.lower() or "aarch" in architecture.lower() else architecture
        elif system == "Darwin":
            return {"x86_64": "x86_64", "arm64": "ARM64"}.get(architecture, "Unknown")
        return "Unknown"

    def check_python(self):
        try:
            python_version = sys.version.split()[0]
            self.update_callback(f"Python verzió: {python_version}", 40)
        except Exception as e:
            self.update_callback(f"Hiba a Python verzió ellenőrzésekor: {str(e)}", 40)

    def check_github_files(self):
        files_to_check = ["install_update_packages.py", "build_script.py"]
        for file in files_to_check:
            if not self.running:
                return
            url = GITHUB_RAW_URL + file
            try:
                response = requests.get(url, verify=certifi.where())
                status = "elérhető" if response.status_code == 200 else f"nem elérhető (Státusz kód: {response.status_code})"
                self.update_callback(f"{file} {status}", 60)
            except Exception as e:
                self.update_callback(f"Hiba a {file} ellenőrzésekor: {str(e)}", 60)

    def check_and_install_dependencies(self):
        self.update_callback("Függőségek ellenőrzése és telepítése...", 80)
        dependencies = ['PyQt6', 'PyQt6-Qt6', 'PyQt6-sip']
        for dep in dependencies:
            if not self.running:
                return
            try:
                importlib.import_module(dep.split('-')[0])
                self.update_callback(f"{dep} már telepítve van", 85)
            except ImportError:
                self.update_callback(f"{dep} telepítése...", 85)
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                    self.update_callback(f"{dep} sikeresen telepítve", 90)
                except subprocess.CalledProcessError as e:
                    self.update_callback(f"Hiba a {dep} telepítése során: {str(e)}", 90)

    def build_application(self):
        self.update_callback("Alkalmazás építése...", 95)
        build_script_url = GITHUB_RAW_URL + "build_script.py"
        try:
            response = requests.get(build_script_url, verify=certifi.where())
            response.raise_for_status()
            script_content = response.text

            # Módosítsuk a build scriptet, hogy a jelenlegi mappába építsen
            script_content = script_content.replace(
                'def main():',
                'def main():\n    os.chdir(os.path.dirname(os.path.abspath(__file__)))'
            )

            # A script tartalmának végrehajtása egy alfolyamatban
            current_dir = os.path.dirname(os.path.abspath(__file__))
            process = subprocess.Popen([sys.executable, '-c', script_content],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True,
                                       cwd=current_dir)

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.update_callback(f"Build: {output.strip()}", 97)

            rc = process.poll()
            if rc == 0:
                # Ellenőrizzük, hogy létrejött-e a dist mappa
                dist_path = os.path.join(current_dir, 'dist')
                if os.path.exists(dist_path):
                    # Másoljuk át a tartalmat a jelenlegi mappába
                    for item in os.listdir(dist_path):
                        s = os.path.join(dist_path, item)
                        d = os.path.join(current_dir, item)
                        if os.path.isdir(s):
                            shutil.copytree(s, d, dirs_exist_ok=True)
                        else:
                            shutil.copy2(s, d)
                    # Töröljük a dist és build mappákat
                    shutil.rmtree(dist_path, ignore_errors=True)
                    shutil.rmtree(os.path.join(current_dir, 'build'), ignore_errors=True)
                    self.update_callback("Alkalmazás sikeresen felépítve és áthelyezve a fő mappába", 100)
                else:
                    self.update_callback("Alkalmazás felépítve, de a dist mappa nem található", 100)
            else:
                self.update_callback(f"Hiba történt az alkalmazás építése során. Kilépési kód: {rc}", 100)
        except Exception as e:
            self.update_callback(f"Hiba: {str(e)}", 100)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keresztplatformos Alkalmazásépítő")
        self.geometry("800x600")

        self.queue = queue.Queue()
        self.create_widgets()

        self.worker_thread = None
        self.protocol("WM_DELETE_WINDOW", self.exit_application)

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.status_label = ttk.Label(main_frame, text="Készen áll")
        self.status_label.pack(pady=5)

        self.log_output = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
        self.log_output.pack(fill=tk.BOTH, expand=True, pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_process)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        self.exit_button = ttk.Button(button_frame, text="Kilépés", command=self.exit_application)
        self.exit_button.pack(side=tk.LEFT)

        self.force_start_button = ttk.Button(button_frame, text="Kényszerített indítás", command=self.force_start)
        self.force_start_button.pack(side=tk.LEFT, padx=(10, 0))

        self.open_folder_button = ttk.Button(button_frame, text="Mappa megnyitása", command=self.open_folder)
        self.open_folder_button.pack(side=tk.LEFT, padx=(10, 0))

    def start_process(self):
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showinfo("Folyamat fut", "A folyamat már fut.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.status_label.config(text="Folyamat kezdődik...")
        self.log_output.delete('1.0', tk.END)

        self.worker_thread = WorkerThread(self.queue, self.update_status)
        self.worker_thread.start()
        self.monitor_queue()

    def force_start(self):
        logging.info("Kényszerített indítás kezdeményezve")
        remove_lock_file()
        self.start_process()

    def update_status(self, message, progress):
        self.queue.put((message, progress))

    def monitor_queue(self):
        try:
            message, progress = self.queue.get_nowait()
            self.status_label.config(text=message)
            self.progress['value'] = progress
            self.log_output.insert(tk.END, message + "\n")
            self.log_output.see(tk.END)
        except queue.Empty:
            pass
        finally:
            if self.worker_thread and self.worker_thread.is_alive():
                self.after(100, self.monitor_queue)
            else:
                self.start_button.config(state=tk.NORMAL)
                self.status_label.config(text="Folyamat befejezve")

    def open_folder(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if sys.platform == "win32":
            os.startfile(current_dir)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", current_dir])
        else:
            subprocess.Popen(["xdg-open", current_dir])

    def exit_application(self):
        if self.worker_thread and self.worker_thread.is_alive():
            if messagebox.askyesno("Kilépés megerősítése", "A folyamat még fut. Biztosan ki akar lépni?"):
                self.worker_thread.running = False
                self.worker_thread.join()
            else:
                return
        self.quit()
        self.destroy()
        remove_lock_file()


def main():
    logging.info("Alkalmazás indítása")
    if is_already_running():
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesnocancel("Alkalmazás már fut",
                                             "Úgy tűnik, az alkalmazás már fut vagy nem záródott be megfelelően.\n"
                                             "Mit szeretne tenni?",
                                             icon='warning',
                                             detail="Igen: Új példány indítása\nNem: Kilépés\nMégse: Kényszerített indítás")
        if response is True:
            remove_lock_file()
        elif response is False:
            logging.info("Felhasználó nem kívánja elindítani az alkalmazást")
            print("Az alkalmazás már fut.")
            return
        elif response is None:
            logging.info("Felhasználó kényszerített indítást választott")
            remove_lock_file()
        else:
            return

    create_lock_file()

    try:
        app = MainWindow()
        logging.info("MainWindow létrehozva, alkalmazás indul")
        app.mainloop()
    except Exception as e:
        logging.error(f"Hiba történt az alkalmazás futtatása közben: {str(e)}")
    finally:
        remove_lock_file()
        logging.info("Alkalmazás bezárva")


if __name__ == "__main__":
    main()