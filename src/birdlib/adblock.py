from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import *

class RequestManager(QWebEngineUrlRequestInterceptor):
    def __init__(self, blacklist:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blist = []
        with open(blacklist) as file:
            for line in file.readlines():
                if line.startswith("!") or "##" in line: #comment
                    pass
                else:
                    self.blist.append(line.strip())
    def interceptRequests(self, info):
        requrl = infu.requestUrl().toString()
        for host in self.blist:
            if "*" in host:
                opts = host.split["*"]
                if requrl.startswith(opts[0]) and requrl.endswith(opts[1]):
                    info.block(True)
                else:
                    continue
            elif requrl == host:
                info.block(True)
