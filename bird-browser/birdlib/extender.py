from pathlib import Path
from importlib import util
class Extender:
	def __init__(self, path:str, pathtoconfig:str):
		self._path = path
		self._confpath = pathtoconfig
	def __repr__(self):
		return f"Extender at {self.path}"
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
				self.plugins = plugindict
				return plugindict
	def loadPlugin(self, name:str):
		try:
			spec = util.spec_from_file_location(f"{name}.ext", f"{Path.home()}/{self._path}")
			extension = util.module_from_spec(spec)
			spec.loader.exec_module(extension)
			return extension
		except:
			raise Exception("error on loading plugin")
