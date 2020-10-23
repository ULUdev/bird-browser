from pathlib import Path
class Extender:
    def __init__(self, path:str):
        self._path = path
    def loadPlugins(self):
        if not Path(f"{Path.home()}/.config/bird/plugins.config.inf").exists():
            raise Exception("setup not satisfied")
        elif Path(f"{Path.home()}/.config/{self._path}").exists():
            with open(f"{Path.home()}/.config/bird/plugins.config.inf", "r") as file:
                plugindict = {}
                for line in file.readlines():
                    line = line.strip()
                    name, file = line.split(":", 1)
                    plugindict[name] = file
                return plugindict
