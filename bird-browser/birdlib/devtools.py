from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QGridLayout, QWidget, QApplication, QShortcut, QPlainTextEdit, QSplitter, QTabWidget
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import requests
import sys
class DevToolWidget(QWidget):
	def __init__(self, url:str, *args, **kwargs):
		super(DevToolWidget, self).__init__(*args, **kwargs)
		self.layout = QGridLayout()
		self.tabs = QTabWidget()
		self.webview = QWebEngineView()
		self.webview.load(QUrl(url))
		self.headers = QPlainTextEdit(self.getHeaders(url))
		self.headers.setReadOnly(True)
		self.source = QPlainTextEdit(self.getSource(url))
		self.source.setReadOnly(True)
		self.splitter = QSplitter()
		self.splitter.addWidget(self.webview)
		self.splitter.addWidget(self.tabs)
		self.tabs.addTab(self.headers, "header")
		self.tabs.addTab(self.source, "source")
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
	window = DevToolWidget("https://moritz.sokoll.com")
	app.exec_()
