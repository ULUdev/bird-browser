class Extension:
    def __init__(self, name:str, version:str):
        self._name = name
        self._version = version
    def __repr__(self):
        return f"Extension {self._name} version {self._version}"
    @property
    def name(self):
        return self._name
    @name.setter
    def setname(self, name:str):
        self._name = name
    
    @property
    def version(self):
        return self._version
    @version
    def setversion(self, version:str):
        self._version = version
    
    def main(self):
        raise Exception("This Extension is doing nothig!")
