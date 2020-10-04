from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import json
import os
try:
    with open(f"/home/{os.getlogin()}/.config/bird/bird.config.json") as file:
        config = json.load(file)
except:
    with open(f"/home/{os.getlogin()}/.config/bird/bird.config.json", "w+") as file:
        file.write(json.dumps(
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
        uic.loadUi('browser.ui', self)
        self.tabs = self.findChild(QTabWidget, "tabs")
        self.tabcreate = self.findChild(QPushButton, "tabcreate")

        self.tabs.clear()

        self.tabs.setTabsClosable(True)

        self.createtab()

        #connections
        self.tabcreate.clicked.connect(self.createtab)
        self.tabs.tabCloseRequested.connect(self.closetab)

        self.show()

    def updatewin(self, browser):
        url = self.url[str(self.tabs.currentIndex)]
        if url.startswith("search://"):
            search = url.split("search://", 1)[1]
            url = config["search-engine"].format(search=search)
        elif not url.startswith("https://") or url.startswith("http://"):
            url = "https://" + url
        browser.load(QUrl(url))
    def updatetext(self, text:str):
        self.url[str(self.tabs.currentIndex)] = text
    def updateurl(self, url, bar):
        bar.setText(url.toString())

    def updatetab(self, arg_1, index, browser):
        if len(browser.page().title()) > 20:
            self.tabs.setTabText(index , browser.page().title()[0:20] + "...")
        else:
            self.tabs.setTabText(index, browser.page().title())
        self.tabs.setTabIcon(index, browser.page().icon())

    def updatetitle(self, title:str):
        self.tabs.setTabText(self.tabs.currentIndex(), title)
    def updateicon(self, index, icon):
        self.tabs.setTabIcon(index, icon)
    def closetab(self, index):
        if index == self.tabs.currentIndex():
            self.tabs.setCurrentIndex(index -1 if index != 0 else index +1)
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            sys.exit(0)
    def createtab(self):
        layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(layout)
        bar = QLineEdit()
        browser = QWebEngineView()
        backbtn = QPushButton("←")
        bar.returnPressed.connect(lambda browser = browser: self.updatewin(browser))
        bar.textChanged.connect(self.updatetext)
        browser.load(QUrl(config["startup-url"]))
        browser.page().urlChanged.connect(lambda qurl, bar = bar: self.updateurl(qurl, bar))
        browser.page().loadFinished.connect(lambda arg__1 ,index = self.tabs.count(), browser = browser: self.updatetab(arg__1, index, browser))
        browser.page().iconChanged.connect(lambda qicon, index = self.tabs.count(): self.updateicon(index, qicon))
        backbtn.clicked.connect(browser.back)
        layout.addWidget(bar, 1, 2)
        layout.addWidget(browser, 2, 1, 1, 3)
        layout.addWidget(backbtn, 1, 1)
        self.tabs.addTab(widget, browser.icon(), browser.title())
        self.tabs.setCurrentIndex(self.tabs.count() -1)

app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
