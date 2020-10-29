from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QGridLayout, QWidget, QApplication, QShortcut, QLabel, QSplitter
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import requests
import sys
class DevToolWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(DevToolWidget, self).__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.button = QPushButton("normal")
        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://moritz.sokoll.com"))
        self.headers = QLabel(self.getHeaders("https://moritz.sokoll.com"))
        self.source = QLabel(self.getSource("https://moritz.sokoll.com"))
        self.source.setTextFormat(Qt.PlainText)
        self.splitter = QSplitter()
        self.splitter.addWidget(self.webview)
        self.splitter.addWidget(self.headers)
        self.splitter.addWidget(self.source)
        self.layout.addWidget(self.button, 1, 2)
        self.layout.addWidget(self.splitter, 1, 1)
        self.setLayout(self.layout)
        self.show()
    def getHeaders(self, url:str):
        req = requests.get(url)
        headers  = f"Status: {req.status_code}\n"
        for elm in req.headers:
            headers += f"{elm}: {req.headers[elm]}\n" if len(req.headers[elm]) < 30 else ""
        return headers
    def getSource(self, url:str):
        req = requests.get(url)
        return req.text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DevToolWidget()
    app.exec_()
