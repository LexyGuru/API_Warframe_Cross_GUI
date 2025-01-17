# Copyright (c) 2024 LexyGuru
# This file is part of the API_Warframe_Cross_GUI project, licensed under the MIT License.
# For the full license text, see the LICENSE file in the project root.


import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
''' QSizePolicy '''
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class WebBridge(QObject):
    @pyqtSlot(str)
    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))


class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        print(f"Request: {info.requestUrl().toString()}")
        print(f"Resource Type: {info.resourceType()}")


class BaseMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warframe Info Hub")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        self.request_interceptor = RequestInterceptor()
        self.web_bridge = WebBridge()
        self.channel = QWebChannel()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

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
            ("Arcon Hunt", lambda: self.load_page("archon")),
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
        self.web_view.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.page().setWebChannel(self.channel)
        self.channel.registerObject('pyotherside', self.web_bridge)

        self.web_view.page().javaScriptConsoleMessage = self.log_javascript

        self.web_bridge = WebBridge()
        self.channel = QWebChannel()
        self.channel.registerObject('pyotherside', self.web_bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.web_view.page().profile().setUrlRequestInterceptor(self.request_interceptor)
        self.web_view.page().setProperty("loadTimeout", 30000)

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
                if (typeof QWebChannel !== 'undefined') {
                    new QWebChannel(qt.webChannelTransport, function (channel) {
                        window.pyotherside = channel.objects.pyotherside;
                        console.log("QWebChannel initialized from Python");
                        if (typeof initSearch === 'function') {
                            initSearch();
                        }
                    });
                } else {
                    console.error("QWebChannel is not defined");
                }
            """)
        else:
            print(f"Page load failed: {self.web_view.url().toString()}")

    def js_console_message(self, level, message, line, source_id):
        print(f"JavaScript: {message}")

    def log_javascript(level, message, line, source):
        print(f"JavaScript [{level}] {message} at line {line} in {source}")

    @staticmethod
    def create_full_html(html_content, js_content, css_content):
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Warframe Info Hub</title>
                <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <style>{css_content}</style>
                <script>
                console.log("HTML content loaded");
                {js_content}
                function initWebChannel() {{
                    if (typeof QWebChannel === "undefined") {{
                        console.log("QWebChannel not available yet, retrying...");
                        setTimeout(initWebChannel, 100);
                        return;
                    }}
                    new QWebChannel(qt.webChannelTransport, function (channel) {{
                        window.pyotherside = channel.objects.pyotherside;
                        console.log("QWebChannel initialized");
                        if (typeof initSearch === "function") {{
                            initSearch();
                        }}
                    }});
                }}
                document.addEventListener("DOMContentLoaded", function() {{
                    console.log("DOM fully loaded");
                    initWebChannel();
                }});
                </script>
            </head>
            <body>
                {html_content}
                <script>
                console.log("Body content loaded");
                </script>
            </body>
            </html>
            """


class LocalMainWindow(BaseMainWindow):
    def load_page(self, page_name):
        base_path = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(base_path, "gui", f"{page_name}.html")
        js_path = os.path.join(base_path, "gui", "Script", f"{page_name}.js")
        css_path = os.path.join(base_path, "gui", "styles", f"{page_name}_styles.css")

        try:
            html_content = self.read_file(html_path)
            js_content = self.read_file(js_path)

            css_content = ""
            try:
                css_content = self.read_file(css_path)
            except FileNotFoundError:
                print(f"CSS file not found for {page_name}, using empty CSS")

            full_html = self.create_full_html(html_content, js_content, css_content)
            self.web_view.setHtml(full_html, QUrl.fromLocalFile(base_path))
        except FileNotFoundError as e:
            error_html = f"<html><body><h1>File not found</h1><p>{str(e)}</p></body></html>"
            self.web_view.setHtml(error_html)
        except Exception as e:
            error_html = f"<html><body><h1>Error loading page</h1><p>{str(e)}</p></body></html>"
            self.web_view.setHtml(error_html)

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


class GitHubMainWindow(BaseMainWindow):
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/"

    def load_page(self, page_name):
        print(f"Loading page from GitHub: {page_name}")
        try:
            html_content = self.download_file(f"gui/{page_name}.html")
            js_content = self.download_file(f"gui/Script/{page_name}.js")

            css_content = ""
            try:
                css_content = self.download_file(f"gui/Styles/{page_name}_styles.css")
            except requests.RequestException:
                print(f"CSS file not found for {page_name}, using empty CSS")

            full_html = self.create_full_html(html_content, js_content, css_content)
            self.web_view.setHtml(full_html)
        except Exception as e:
            error_html = f"<html><body><h1>Error loading page</h1><p>{str(e)}</p></body></html>"
            self.web_view.setHtml(error_html)
            print(f"Error loading page {page_name}: {str(e)}")

    @staticmethod
    def download_file(filename):
        url = GitHubMainWindow.GITHUB_RAW_URL + filename
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            return f"Error loading {filename}: {str(e)}"


if __name__ == "__main__":
    app = QApplication(sys.argv)

    use_local = True  # Állítsa True-ra a helyi verzióhoz, False-ra a GitHub verzióhoz

    if use_local:
        window = LocalMainWindow()
    else:
        window = GitHubMainWindow()

    window.show()
    sys.exit(app.exec_())