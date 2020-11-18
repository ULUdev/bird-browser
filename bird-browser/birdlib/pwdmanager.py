from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFormLayout, QWidget, QApplication, QShortcut, QPlainTextEdit, QSplitter, QTabWidget
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sqlite3 as sql
import sys
#import pyperclip

class PwdManager:
	def __init__(self, key:int, store_path:str):
		pass
		#self.conn = sql.connect(store_path)
		#self.cursor = self.conn.cursor()
	
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

	def getPwdKeys(self):
		return ["twitter", "reddit"]
		self.cursor.execute("select key from pwdstore")
		res = self.cursor.fetchall()
		if len(res) < 1:
			return None
		outres = []
		for i in res:
			outres.append(i[0])
		return outres
	
	def delPwd(self, key:str):
		self.cursor.execute("delete from pwdstore where key=?", key)
		self.conn.commit()


class PwdManagerWidget(QWidget):
	def __init__(self, manager, *args, **kwargs):
		super(PwdManagerWidget, self).__init__(*args, **kwargs)
		self.manager = manager
		self.layout = QFormLayout()
		for key in self.manager.getPwdKeys():
			self.layout.addRow("pwd:", QPushButton(key))
		self.addpwdwidget = QWidget()
		self.addpwdlayout = QFormLayout()
		passwordedit = QLineEdit()
		passwordedit.setEchoMode(QLineEdit.Password)
		self.addpwdlayout.addRow("website:", QLineEdit())
		self.addpwdlayout.addRow("password:", passwordedit)
		self.addpwdlayout.addRow(QPushButton("submit"))
		self.addpwdwidget.setLayout(self.addpwdlayout)
		self.layout.addRow("add pwd:", self.addpwdwidget)
		self.setLayout(self.layout)
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = PwdManagerWidget(PwdManager(1, "1"))
	app.exec_()
