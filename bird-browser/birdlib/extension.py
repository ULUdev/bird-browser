class Extension:
    def __init__(self, name:str, version:str):
        self._name = name
        self._version = version

    def __repr__(self):
        return f"Extension {self._name} version {self._version}"

    #name
    @property
    def name(self):
        return self._name
    @name.setter
    def setname(self, name:str):
        if name.lower().startswith("bird") and name.lower().endswith("browser"):
            render = name.lower().split("bird")[1].split("browser")[0]
            if len(render) <= 1:
                raise ValueError("Name not allowed")
        self._name = name
    
    #version
    @property
    def version(self):
        return self._version
    @version.setter
    def setversion(self, version:str):
        self._version = version
   
   #widget
   @property
   def widget(self):
       try:
           return self._widget
       except:
           return None
    @widget.setter
    def setwidget(self, widget):
        self._widget = widget
