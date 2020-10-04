from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import json
import os
try:
    with open(f"/home/{os.getlogin()}/.config/bird.config.json") as file:
        config = json.load(file)
except:
    with open(f"/home/{os.getlogin()}/.config/bird.config.json", "w+") as file:
        file.write(json.dump(
            {
                "search-engine": "https://duckduckgo.com/?q={search}",
                "startup-url": "https://duckduckgo.com/"
            },
            indent=4))
        config = {"search-engine": "https://duckduckgo.com/?q={search}", "startup-url": "https://duckduckgo.com/"}
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.url = {}
        self.setWindowTitle("Bird-Browser")
        self.layout = QVBoxLayout()
        self.mainlayout = QGridLayout()
        self.browser = QWebEngineView()
        self.bar = QLineEdit()
        self.browser.setUrl(QUrl(config["startup-url"]))
        self.browser.page().urlChanged.connect(lambda qurl, bar = self.bar: self.updateurl(qurl, bar))
        self.browser.page().titleChanged.connect(self.updatetitle)
        self.browser.page().iconChanged.connect(self.updateicon)
        self.bar.returnPressed.connect(lambda browser = self.browser: self.updatewin(browser))
        self.bar.textChanged.connect(self.updatetext)
        self.tabcreate = QPushButton("+")
        self.tabcreate.clicked.connect(self.createtab)
        self.layout.addWidget(self.bar)
        self.layout.addWidget(self.browser)
        self.tabs = QTabWidget()
        mainwinwidget = QWidget()
        mainwinwidget.setLayout(self.mainlayout)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.tabs.addTab(self.widget, self.browser.icon(), self.browser.title())
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closetab)
        self.mainlayout.addWidget(self.tabs, 1, 1, 2, 1)
        self.mainlayout.addWidget(self.tabcreate, 1, 2)
        self.setCentralWidget(mainwinwidget)
    def updatewin(self, browser):
        url = self.url[str(self.tabs.currentIndex)]
        if url.startswith("search://"):
            search = url.split("search://", 1)[1]
            url = config["search-engine"].format(search=search)
        elif not url.startswith("https://") or url.startswith("http://"):
            url = "https://" + url
        browser.setUrl(QUrl(url))
    def updatetext(self, text:str):
        self.url[str(self.tabs.currentIndex)] = text
    def updateurl(self, url, bar):
        bar.setText(url.toString())
    def updatetitle(self, title:str):
        self.tabs.setTabText(self.tabs.currentIndex(), title)
    def updateicon(self, icon):
        self.tabs.setTabIcon(self.tabs.currentIndex(), icon)
    def closetab(self, index):
        if index == self.tabs.currentIndex():
            self.tabs.setCurrentIndex = index -1 if index != 0 else index +1
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            sys.exit(0)
    def createtab(self):
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        bar = QLineEdit()
        browser = QWebEngineView()
        bar.returnPressed.connect(lambda browser = browser: self.updatewin(browser))
        bar.textChanged.connect(self.updatetext)
        browser.setUrl(QUrl(config["startup-url"]))
        browser.page().urlChanged.connect(lambda qurl, bar = bar: self.updateurl(qurl, bar))
        browser.page().titleChanged.connect(self.updatetitle)
        browser.page().iconChanged.connect(self.updateicon)
        layout.addWidget(bar)
        layout.addWidget(browser)
        self.tabs.addTab(widget, self.browser.icon(), self.browser.title())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
