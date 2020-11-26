#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QTabWidget, QMainWindow, QLineEdit, QGridLayout, QWidget, QApplication, QShortcut, QCompleter
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
#local imports
from birdlib import adblock, devtools, pwdmanager
from birdlib import bookmarks as bmk
#additional imports
import json
import sqlite3 as sql
import sys
from pathlib import Path


#setup
NetworkFilter = adblock.RequestManager()
NetworkFilter.setup()
try:
	with open(f"{Path.home()}/.config/bird/bird.config.json", "r") as file:
		config = json.load(file)
except FileNotFoundError:
	if not Path(f"{Path.home()}/.config/bird/").exists():
		Path(f"{Path.home()}/.config/bird").mkdir()
	with open(f"{Path.home()}/.config/bird/bird.config.json", "w+") as file:
		file.write(json.dumps(
			{
				"search-engine": "https://duckduckgo.com/?q={search}",
				"startup-url": "https://duckduckgo.com/",
				"key": 12345
			},
			indent=4))
		config = {"search-engine": "https://duckduckgo.com/?q={search}", "startup-url": "https://duckduckgo.com/", "key": 12345}

try:
	conn = sql.connect(f"{Path.home()}/.config/bird/database.db")
except:
	with open(f"{Path.home()}/.config/bird/database.db", "w+") as file:
		file.write("")
	conn = sql.connect(f"{Path.home()}/.config/bird/database.db")

cursor = conn.cursor()
try:
	bmk.setupDatabase(cursor)
except:
	pass
#Window
class MainWindow(QMainWindow):
	"""
	the main render proccess of the browser including all updating methods and the webview
	"""
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.url = {}
		self.setWindowTitle("Bird-Browser")
		self.wordlist = ["dev://", "bookmark://", "bookmarks://", "search://", "http://", "https://", "pwd://"]
		self.tabs = QTabWidget()
		self.tabcreate = QPushButton("+")
		self.shortcreatetab = QShortcut(self)
		self.shortcreatetab.setKey("Ctrl+T")
		self.pwdman = pwdmanager.PwdManager(config["key"], f"{Path.home()}/.config/bird/database.db")
		

		if "style" in config:
			innerstyle = f"""
					color: {config['style']['color']};
					background-color: {config['style']['background-color']};
			"""
			self.setStyleSheet(f"""
				QMainWindow{
					{innerstyle}
				}
					""")
			self.tabs.setStyleSheet(f"""
				QTabWidget{
					{innerstyle}
				}
			""")
		else:
			self.setStyleSheet("""
				background-color: rgb(50, 50, 50);
				color: rgb(255, 255, 255);
			""")
			self.tabs.setStyleSheet("""
				background-color: rgb(50, 50, 50);
				color: rgb(255, 255, 255);
			""")
		self.tabs.clear()

		self.tabs.setTabsClosable(True)

		self.createtab()

		#connections
		self.shortcreatetab.activated.connect(self.createtab)
		self.tabcreate.clicked.connect(self.createtab)
		self.tabs.tabCloseRequested.connect(self.closetab)
		self.tabs.setCornerWidget(self.tabcreate)

		#show window
		self.setCentralWidget(self.tabs)
		self.show()

	def updatewin(self, browser:QWebEngineView, boolean=True):
		"""
		This Method updates the shown browser window to the current url of the search bar
		it also contains the search engine-integration, and bookmarking
		"""
		url = self.url[str(self.tabs.currentIndex)]
		if url.startswith("search://"):
			search = url.split("search://", 1)[1]
			url = config["search-engine"].format(search=search)
		elif url.startswith("bookmarks://"):
			try:
				name = url.split("bookmarks://", 1)[1]
				url = bmk.getBookmark(cursor, name)[name]
			except ValueError:
				url = "about:blank"
		elif url.startswith("bookmark://"):
			if not "|" in url.split("bookmark://", 1)[1]:
				url = "about:blank"
			else:
				parts = url.split("bookmark://", 1)[1].split("|")
				if parts[1] == "-":
					parts[1] = browser.url().toString()
				try:
					bmk.getBookmark(cursor, parts[0])
					bmk.modifyBookmark(cursor, parts[0], parts[0], parts[1])
					conn.commit()
				except:
					bmk.addBookmark(cursor, parts[0], parts[1])
					conn.commit()
		elif url.startswith("file://"):
			path = url.split("file://", 1)[1]
			if path.startswith("~/"):
				path = f"{Path.home()}/{path.split('~/', 1)[1]}"
			try:
				with open(path, "r") as reqfile:
					reqcontent = reqfile.read()
				browser.page().setHtml(reqcontent)
				return
			except:
				print(f"Error on requested page: Path '{path}' doesn't exist")
				browser.page().loadUrl(QUrl("about:blank"))
		elif url.startswith("dev://"):
			url = url.split("dev://", 1)[1]
			if not url.startswith("https://") and not url.startswith("http://"):
				url = "http://" + url
			self.tabs.addTab(devtools.DevToolWidget(url), "dev-tools")
		elif url.startswith("pwd://"):
			self.tabs.addTab(pwdmanager.PwdManagerWidget(self.pwdman), "Passwords")
			return
		elif "additional-search-engines" in config:
			for source in config["additional-search-engines"]:
				if url.startswith(source):
					search = url.split(source, 1)[1]
					url = config["additional-search-engines"][source].format(search=search)
					break
				else:
					pass
			else:
				if not url.startswith("https://") and not url.startswith("http://"):
					url = "http://" + url
		elif not url.startswith("https://") and not url.startswith("http://"):
			url = "http://" + url
		browser.page().load(QUrl(url))
		self.wordlist.append(url)
	def updatetext(self, text:str):
		"""
		This Method updates the internal text of the search bar
		"""
		self.url[str(self.tabs.currentIndex)] = text
	def updateurl(self, url, bar):
		"""
		This method updates the url bar to the currently displayed url.
		It gets triggered if the displayed page directs you to a different page
		"""
		bar.setText(url.toString())
 
	def updatetab(self, arg_1, index, browser):
		if len(browser.page().title()) > 20:
			self.tabs.setTabText(index , browser.page().title()[0:17] + "...")
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
	
	@pyqtSlot()
	def createtab(self, url:str=config["startup-url"]):
		layout = QGridLayout()
		widget = QWidget()
		widget.setLayout(layout)
		bar = QLineEdit()
		completer = QCompleter(self.wordlist)
		browser = QWebEngineView()
		backbtn = QPushButton("←")
		reloadbtn = QPushButton("reload")
		gotocurrenturlbutton = QPushButton("go!")
		reloadshort = QShortcut(self)
		reloadshort.setKey("Ctrl+R")
		bar.setCompleter(completer)
		reloadshort.activated.connect(browser.reload)
		gotocurrenturlbutton.clicked.connect(lambda clicked, browser = browser: self.updatewin(browser, clicked))
		reloadbtn.clicked.connect(browser.reload)
		bar.returnPressed.connect(lambda  browser = browser: self.updatewin(browser, True))
		bar.textChanged.connect(self.updatetext)
		browser.load(QUrl(url))
		browser.page().urlChanged.connect(lambda qurl, bar = bar: self.updateurl(qurl, bar))
		browser.page().loadFinished.connect(lambda arg__1 ,index = self.tabs.indexOf(browser), browser = browser: self.updatetab(arg__1, index, browser))
		browser.page().iconChanged.connect(lambda qicon, index = self.tabs.count(): self.updateicon(index, qicon))
		browser.page().setUrlRequestInterceptor(NetworkFilter)
		browser.page().titleChanged.connect(lambda title = browser.page().title(): self.updatetitle(title))
		backbtn.clicked.connect(browser.back)
		layout.addWidget(bar, 1, 3)
		layout.addWidget(reloadbtn, 1, 2)
		layout.addWidget(browser, 2, 1, 1, 5)
		layout.addWidget(backbtn, 1, 1)
		layout.addWidget(gotocurrenturlbutton, 1, 4)
		self.tabs.addTab(widget, browser.icon(), browser.title())
		self.tabs.setCurrentIndex(self.tabs.count() -1)
	def renderDevToolsView(self, webview):
		return self.tabs.setCurrentWidget(devtools.DevToolWidget(webview.page().url().toString()))

#main process
if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	app.exec_()
	conn.close()
