from pathlib import Path
class Theme:
    def __init__(self, color:str, background-color:str):
        self._color = color
        self._background-color = background-color
    
    @property
    def path(self):
        try:
            return self._path
        except:
            self._path = "example.theme"
            return self._path
    @property.setter
    def setpath(self, path:str):
        if path.startswith("themes/"):
            raise ValueError("unsupported folder")
        elif not path.endswith(".theme"):
            raise ValueError("filename must end with .theme")
        else:
            self._path = path
    
    @staticmethod
    def themeFolder():
        return f"{Path.home()}/.config/bird/themes/"

#This Class loads themes
class ThemeLoader:
    def __init__(self, path:str):
        self.path = path
    
    def loadThemes(self):
        if Path(f"{self.path}/themes.config.inf").exists():
            with open(f"{self.path}/themes.config.inf", "r") as file:
                themedict = {}
                for line in file.readlines():
                    line = line.strip()
                    name, path = line.split(":", 1)
                    with open(f"{self.path}/themes/{path}", "r") as file:
                        themedict[name] = {
                                file.read().split("\n")[0].strip().split(":")[0]: file.read().split("\n")[0].strip().split(":")[1],
                                file.read().split("\n")[1].strip().split(":")[0]: file.read().split("\n")[1].strip().split(":")[1]
                                }
                self.themes = themedict
                return themedict
        else:
            raise Exception("no theme configuration file found")

    def loadTheme(self, name:str):
        try:
            return self.themes[name]
        except:
            raise Exception("error on showing theme info")
