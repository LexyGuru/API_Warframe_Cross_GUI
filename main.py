import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, \
    QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebChannel import QWebChannel


class WebBridge(QObject):
    @pyqtSlot(str)
    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))


class BaseMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warframe Info Hub")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Bal oldali menü
        menu_widget = QWidget()
        menu_widget.setFixedWidth(200)
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setAlignment(Qt.AlignTop)

        menu_buttons = [
            ("Kezdőlap", self.load_home_page),
            ("Keresés", lambda: self.load_page("search")),
            ("Ciklusok", lambda: self.load_page("cycles")),
            ("Események", lambda: self.load_page("events")),
            ("Void Fissures", lambda: self.load_page("fissures")),
            ("Sortie", lambda: self.load_page("sortie")),
            ("Nightwave", lambda: self.load_page("nightwave")),
            ("Arbitration", lambda: self.load_page("arbitration")),
            ("Baro Ki'Teer", lambda: self.load_page("baro")),
        ]

        for button_text, function in menu_buttons:
            button = QPushButton(button_text)
            button.clicked.connect(function)
            menu_layout.addWidget(button)

        menu_layout.addStretch()
        update_info_button = QPushButton("Update Info")
        update_info_button.clicked.connect(lambda: self.load_page("info_git"))
        menu_layout.addWidget(update_info_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(menu_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFixedWidth(220)

        main_layout.addWidget(scroll_area)

        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.web_bridge = WebBridge()
        self.channel = QWebChannel()
        self.channel.registerObject('pyotherside', self.web_bridge)
        self.web_view.page().setWebChannel(self.channel)

        main_layout.addWidget(self.web_view, 4)

        self.load_home_page()
        self.web_view.loadFinished.connect(self.onLoadFinished)

    def load_page(self, page_name):
        raise NotImplementedError("Subclasses must implement this method")

    def load_home_page(self):
        self.load_page("home")

    def onLoadFinished(self, ok):
        if ok:
            print(f"Page loaded successfully: {self.web_view.url().toString()}")
            self.web_view.page().runJavaScript("""
                console.log("JavaScript executed from Python");
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.pyotherside = channel.objects.pyotherside;
                    console.log("QWebChannel initialized from Python");
                });
            """)
        else:
            print(f"Page load failed: {self.web_view.url().toString()}")


class LocalMainWindow(BaseMainWindow):
    def load_page(self, page_name):
        base_path = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base_path, "gui", f"{page_name}.html")
        js_path = os.path.join(base_path, "gui", "Script", f"{page_name}.js")
        css_path = os.path.join(base_path, "gui", "styles", "search_styles.css")

        print(f"Attempting to load local files for {page_name}")

        try:
            with open(html_path, 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            with open(js_path, 'r', encoding='utf-8') as js_file:
                js_content = js_file.read()

            with open(css_path, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()

            full_html = f"""
            <html>
            <head>
                <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <style>{css_content}</style>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {{
                        new QWebChannel(qt.webChannelTransport, function (channel) {{
                            window.pyotherside = channel.objects.pyotherside;
                            console.log("QWebChannel initialized");
                        }});
                    }});
                </script>
                <script>{js_content}</script>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            self.web_view.setHtml(full_html, QUrl.fromLocalFile(base_path))
        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
            self.web_view.setHtml(
                f"<html><body><h1>Error: File not found</h1><p>Could not find {e.filename}</p></body></html>")
        except Exception as e:
            print(f"Error loading files: {e}")
            self.web_view.setHtml(f"<html><body><h1>Error loading page</h1><p>{str(e)}</p></body></html>")

class GitHubMainWindow(BaseMainWindow):
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/"

    def load_page(self, page_name):
        print(f"Loading page from GitHub: {page_name}")
        html_content = self.download_file(f"gui/{page_name}.html")
        js_content = self.download_file(f"gui/Script/{page_name}.js")
        css_content = self.download_file(f"gui/Styles/{page_name}_styles.css")

        full_html = f"""
        <html>
        <head>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <style>{css_content}</style>
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    new QWebChannel(qt.webChannelTransport, function (channel) {{
                        window.pyotherside = channel.objects.pyotherside;
                        console.log("QWebChannel initialized");
                    }});
                }});
            </script>
            <script>{js_content}</script>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        self.web_view.setHtml(full_html, QUrl(self.GITHUB_RAW_URL))

    @staticmethod
    def download_file(filename):
        url = GitHubMainWindow.GITHUB_RAW_URL + filename
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            return f"<p>Error loading {filename}</p>"


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Válassza ki a megfelelő verziót
    use_local = False  # Állítsa False-ra a GitHub verzióhoz

    if use_local:
        window = LocalMainWindow()
    else:
        window = GitHubMainWindow()

    window.show()
    sys.exit(app.exec_())