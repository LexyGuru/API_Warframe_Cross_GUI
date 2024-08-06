import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebChannel import QWebChannel

GITHUB_RAW_URL = "https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/"


class WebBridge(QObject):
    @pyqtSlot(str)
    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Warframe Info Hub")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Bal oldali menü
        menu_widget = QWidget()
        menu_widget.setFixedWidth(200)  # Fix szélesség beállítása
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setAlignment(Qt.AlignTop)  # Gombok igazítása felülre

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

        # Az "Update Info" gomb hozzáadása a menü aljára
        menu_layout.addStretch()
        update_info_button = QPushButton("Update Info")
        update_info_button.clicked.connect(lambda: self.load_page("info_git"))
        menu_layout.addWidget(update_info_button)

        # Görgetősáv hozzáadása a menühöz
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(menu_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFixedWidth(220)  # Fix szélesség a görgetősávval együtt

        main_layout.addWidget(scroll_area)

        # Web nézet
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        # WebBridge beállítása
        self.web_bridge = WebBridge()
        self.channel = QWebChannel()
        self.channel.registerObject('pyotherside', self.web_bridge)
        self.web_view.page().setWebChannel(self.channel)

        main_layout.addWidget(self.web_view, 4)

        # Kezdő oldal betöltése
        self.load_home_page()

        # Kapcsoljuk össze a loadFinished szignált az onLoadFinished slottal
        self.web_view.loadFinished.connect(self.onLoadFinished)

    def load_page(self, page_name):
        print(f"Loading page: {page_name}")
        html_content = self.download_file(f"gui/{page_name}.html")
        js_content = self.download_file(f"gui/Script/{page_name}.js")

        full_html = f"""
        <html>
        <head>
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                // Várunk, amíg a QWebChannel elérhetővé válik
                function initWebChannel() {{
                    if (typeof QWebChannel === "undefined") {{
                        setTimeout(initWebChannel, 100);
                        return;
                    }}
                    new QWebChannel(qt.webChannelTransport, function (channel) {{
                        window.pyotherside = channel.objects.pyotherside;
                        console.log("QWebChannel initialized");
                    }});
                }}
                initWebChannel();
            </script>
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

    @staticmethod
    def download_file(filename):
        url = GITHUB_RAW_URL + filename
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: Could not download {filename}"

    def onLoadFinished(self, ok):
        if ok:
            print("Page loaded successfully")
            self.web_view.page().runJavaScript("""
                console.log("JavaScript executed from Python");
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.pyotherside = channel.objects.pyotherside;
                    console.log("QWebChannel initialized from Python");
                });
            """)
        else:
            print("Page load failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
