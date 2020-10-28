from PyQt5.QtCore import *
from PyQt5.QtWidgets import QPushButton, QLineEdit, QGridLayout, QWidget, QApplication, QShortcut
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
class DevToolWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(DevToolWidget, self).__init__(*args, **kwargs)

