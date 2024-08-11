import sys
import os
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import logging
import tempfile
import shutil

# Naplózás beállítása
logging.basicConfig(filename='app_log.txt', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

REPO_URL = "https://github.com/LexyGuru/API_Warframe_Cross_GUI.git"
REPO_DIR = os.path.join(tempfile.gettempdir(), "API_Warframe_Cross_GUI")


class WorkerThread(threading.Thread):
    def __init__(self, queue, update_callback):
        threading.Thread.__init__(self)
        self.queue = queue
        self.update_callback = update_callback
        self.running = True

    def run(self):
        steps = [
            ("GitHub repó klónozása", self.clone_repo),
            ("Függőségek telepítése", self.install_dependencies),
            ("Alkalmazás építése", self.build_application),
            ("Alkalmazás tesztelése", self.test_application)
        ]
        total_steps = len(steps)
        for i, (step_name, step_function) in enumerate(steps):
            if not self.running:
                break
            self.update_callback(f"{step_name}...", (i / total_steps) * 100)
            step_function()
        self.update_callback("Folyamat befejezve", 100)

    def clone_repo(self):
        if os.path.exists(REPO_DIR):
            shutil.rmtree(REPO_DIR)
        try:
            subprocess.run(["git", "clone", REPO_URL, REPO_DIR], check=True, capture_output=True, text=True)
            self.update_callback("GitHub repó sikeresen klónozva", 25)
        except subprocess.CalledProcessError as e:
            self.update_callback(f"Hiba a repó klónozása során: {e.stdout}\n{e.stderr}", 25)

    def install_dependencies(self):
        try:
            requirements_file = os.path.join(REPO_DIR, "requirements.txt")
            if os.path.exists(requirements_file):
                result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file],
                                        check=True, capture_output=True, text=True)
                self.update_callback(f"Függőségek sikeresen telepítve\n{result.stdout}", 50)
            else:
                self.update_callback("requirements.txt nem található", 50)
        except subprocess.CalledProcessError as e:
            self.update_callback(f"Hiba a függőségek telepítése során: {e.stdout}\n{e.stderr}", 50)

    def build_application(self):
        try:
            build_script = os.path.join(REPO_DIR, "build_script.py")
            if os.path.exists(build_script):
                result = subprocess.run([sys.executable, build_script],
                                        check=True, capture_output=True, text=True, cwd=REPO_DIR)
                self.update_callback(f"Alkalmazás build folyamat kimenete:\n{result.stdout}\n{result.stderr}", 75)

                # Ellenőrizzük, hogy létrejött-e a lefordított alkalmazás
                dist_dir = os.path.join(REPO_DIR, "dist")
                if os.path.exists(dist_dir):
                    files = os.listdir(dist_dir)
                    self.update_callback(f"Létrehozott fájlok: {', '.join(files)}", 80)
                else:
                    self.update_callback("A dist könyvtár nem található", 80)
            else:
                self.update_callback("build_script.py nem található", 75)
        except subprocess.CalledProcessError as e:
            self.update_callback(f"Hiba az alkalmazás építése során: {e.stdout}\n{e.stderr}", 75)

    def test_application(self):
        try:
            dist_dir = os.path.join(REPO_DIR, "dist")
            app_name = "WarframeInfoHub"  # vagy bármilyen név, amit a build script használ
            if platform.system() == "Windows":
                app_path = os.path.join(dist_dir, f"{app_name}.exe")
            else:
                app_path = os.path.join(dist_dir, app_name)

            if os.path.exists(app_path):
                result = subprocess.run([app_path], capture_output=True, text=True, timeout=10)
                self.update_callback(f"Alkalmazás teszt kimenete:\n{result.stdout}\n{result.stderr}", 100)
            else:
                self.update_callback(f"A lefordított alkalmazás nem található: {app_path}", 100)
        except subprocess.TimeoutExpired:
            self.update_callback("Az alkalmazás elindult, de nem adott kimenetet 10 másodpercen belül.", 100)
        except Exception as e:
            self.update_callback(f"Hiba az alkalmazás tesztelése során: {str(e)}", 100)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keresztplatformos Alkalmazásépítő")
        self.geometry("800x600")

        self.queue = queue.Queue()
        self.create_widgets()

        self.worker_thread = None

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

        self.exit_button = ttk.Button(button_frame, text="Kilépés", command=self.quit)
        self.exit_button.pack(side=tk.LEFT)

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


def main():
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()