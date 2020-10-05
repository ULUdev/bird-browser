from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import *

class RequestManager(QWebEngineUrlRequestInterceptor):
    """
    This subclass works as a gate. As far as I understand the functionality, the WebView instances are sending their requests to this class.
    He then decides either that a request is valid and doesn't contain any ads (look at interceptRequest) or a request is an ad and he blocks it.'
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def setup(self, blacklistfile:str):
        self.blist = []
        with open(blacklistfile) as file:
            for line in file.readlines():
                line = line.strip()
                if line.startswith("!") or line.startswith("##") or line.startswith("["):
                    continue
                else:
                    self.blist.append(line)

    def interceptRequest(self, info):
        requrl = info.requestUrl().toString()
        for host in self.blist:
            if "*" in host:
                host = host.replace("*", "")
            if host in requrl:
                info.block(True)
                print(f"blocking {requrl}")
            else:
                pass
