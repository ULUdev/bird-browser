from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QGridLayout, QWidget, QApplication, QShortcut, QPlainTextEdit, QSplitter, QTabWidget
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sqlite3 as sql

class PwdManager:
	def __init__(self, key:int. store-path:str):
		self.conn = sql.connect(store-path)
		self.cursor = self.conn.cursor()
	
	def setupDb(self):
		self.cursor.execute("create table if not exists pwdstore (key, value)")


	def getPwd(self, pwdkey:str):
		self.cursor.execute("select value from pwdstore where key=?", pwdkey)
		return cursor.fetchone()[0]
	
	def setPwd(self, pwdkey:str, value:str):
		self.cursor.execute("update pwdstore set value=? where key=?", value, pwdkey)

	def addPwd(self, key:str, value:str):
		self.cursor.execute("insert into pwdstore (?, ?)", key, value)
		self.conn.commit()


class PwdManagerWidget(QWidget):
	def __init__(self, manager:PwdManager, *args, **kwargs):
		super(PwdManagerWidget, self).__init__(*args, **kwargs)
		self.manager = manager

