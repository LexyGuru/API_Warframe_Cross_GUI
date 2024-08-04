import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

GITHUB_RAW_URL = "https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warframe Info Hub")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Bal oldali menü
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        menu_buttons = [
            ("Kezdőlap", self.load_home_page),
            ("Keresés", lambda: self.load_page("search")),
            ("Ciklusok", lambda: self.load_page("cycles")),
            ("Események", lambda: self.load_page("events")),
            ("Void Fissures", lambda: self.load_page("fissures")),
            ("Sortie", lambda: self.load_page("sortie")),
            ("Nightwave", lambda: self.load_page("nightwave")),
            ("Arbitration", lambda: self.load_page("arbitration")),
            ("Baro Ki'Teer", lambda: self.load_page("baro"))
        ]

        for button_text, function in menu_buttons:
            button = QPushButton(button_text)
            button.clicked.connect(function)
            menu_layout.addWidget(button)

        menu_layout.addStretch()
        main_layout.addWidget(menu_widget, 1)

        # Web nézet
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        main_layout.addWidget(self.web_view, 4)

        # Kezdő oldal betöltése
        self.load_home_page()

    def load_page(self, page_name):
        html_content = self.download_file(f"gui/{page_name}.html")
        js_content = self.download_file(f"gui/{page_name}.js")

        full_html = f"""
        <html>
        <head>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>{js_content}</script>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        self.web_view.setHtml(full_html, QUrl(GITHUB_RAW_URL))

    def load_home_page(self):
        self.load_page("home")

    def download_file(self, filename):
        url = GITHUB_RAW_URL + filename
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Could not download {filename}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())