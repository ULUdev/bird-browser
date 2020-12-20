from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QFormLayout, QWidget, QApplication, QShortcut, QPlainTextEdit, QSplitter, QTabWidget
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from . import errors
from . import crypt
import sqlite3 as sql
import sys
import pyperclip

class PwdManager:
	def __init__(self, key:int, store_path:str):
		self.conn = sql.connect(store_path)
		self.cursor = self.conn.cursor()
		self.enckey = key
	
	def setupDb(self):
		self.cursor.execute("create table if not exists pwdstore (key, value)")


	def getPwd(self, pwdkey:str):
		self.cursor.execute("select value from pwdstore where key='%s'"% str(pwdkey))
		try:
			return crypt.decrypt(self.enckey, self.cursor.fetchone()[0])
		except:
			return None
	
	def setPwd(self, pwdkey:str, value:str):
		self.cursor.execute("update pwdstore set value=? where key=?", [value, pwdkey])

	def addPwd(self, key:str, value:str):
		pwd = crypt.encrypt(self.enckey, value)
		if self.getPwd(key) == pwd:
			raise errors.DatabaseError("record exists")
		else:
			self.cursor.execute("insert into pwdstore values (?, ?)", [key, pwd])
			self.conn.commit()

	def getPwdKeys(self):
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
	def __init__(self, manager:PwdManager, *args, **kwargs):
		super(PwdManagerWidget, self).__init__(*args, **kwargs)
		self.manager = manager
		self.manager.setupDb()
		self.layout = QFormLayout()
		if not self.manager.getPwdKeys() == None:
			for key in self.manager.getPwdKeys():
				button = QPushButton(key)
				button.clicked.connect(lambda clicked, key=key: self.copyPwd(str(key)))
				self.layout.addRow("pwd:", button)
		self.addpwdwidget = QWidget()
		self.addpwdlayout = QFormLayout()
		self.passwordedit = QLineEdit()
		self.passwordedit.setEchoMode(QLineEdit.Password)
		self.keyedit = QLineEdit()
		self.addpwdlayout.addRow("website:", self.keyedit)
		self.addpwdlayout.addRow("password:", self.passwordedit)
		addbtn = QPushButton("submit")
		addbtn.clicked.connect(lambda clicked: self.addPwd())
		self.addpwdlayout.addRow(addbtn)
		self.addpwdwidget.setLayout(self.addpwdlayout)
		self.layout.addRow("add pwd:", self.addpwdwidget)
		self.setLayout(self.layout)
		self.show()
	
	def copyPwd(self, key:str):
		pyperclip.copy(self.manager.getPwd(key))


	def addPwd(self):
		self.manager.addPwd(self.keyedit.text(), self.passwordedit.text())


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = PwdManagerWidget(PwdManager(1, "/home/moritz/Code/Python/browser/test/test.db"))
	app.exec_()
