import re, types, sys, traceback, imp, time

levels = ["raw", "text", "gtk"]

class Plugins():
	plugins = {}
	files = {}
	features = []
	useGtk = False
	useConfig = False

	def load(self, name):
		try:
			start = time.time()
			self.unload(name)
			self.files[name] = __import__("plugins." + name, globals(), locals(), [name], -1)
			self.plugins[name] = self.files[name].plugin(self.useConfig)
			self.files[name] = imp.reload(self.files[name])
			self.features.extend(self.plugins[name].featuresList())
		except:
			print(" >>> ERROR in plugin: " + name)
			print('-'*60)
			traceback.print_exc(file=sys.stdout)
			print('-'*60)
			self.unload(name)
			return("ERROR in plugin: " + name)
		if self.plugins.has_key(name):
			delta = time.time() - start
			print(" >>> Plugin " + name + " loaded (Loaded in "+str(delta)+" seconds)")
			return("Plugin " + name + " loaded.")

	def unload(self, name):
		if self.plugins.has_key(name):
			del self.plugins[name]
			del self.files[name]
			print(" >>> Plugin " + name + " unloaded.")
			return("Plugin " + name + " unloaded.")

	def unloadAll(self):
		for name in self.plugins.keys():
			self.unload(name)

	def loaded(self):
		return self.plugins.keys()

	def setGtk(self, window):
		self.useGtk = window

	def setConfig(self, config):
		self.useConfig = config

	def checkAll(self, query, additional={}):
		rt = []
		for name, callback in self.plugins.iteritems():
			ret = callback.dynamicCheck(query, additional)
			if ret != False :
				rt.extend(ret)
		return self.sortFeatures(rt)

	def sortFeatures(self, inp):
		return sorted(inp, key=lambda (v): (float(v["accuracy"])), reverse=True)

	def listFeatures(self):
		return self.features

	def findName(self, name):
		if name in self.plugins:
			return name
		elif name in self.listAliases():
			return self.aliases[name]
		else:
			return False

	def use(self, maxlevel, name, query, additional={}):
		try:
			lvl = levels.index(maxlevel)
		except:
			return false
		success = False
		name = self.findName(name)
		print(" >>> Using plugin: " + name)
		try:
			if lvl >= 2 and success == False and self.useGtk != False:
				if hasattr(self.plugins[name], 'gtk'):
					ret = self.plugins[name].gtk(self.useGtk, query, additional)
					return {"level": "gtk", "status": ret}
			if lvl >= 1 and success == False:
				if hasattr(self.plugins[name], 'text'):
					ret = self.plugins[name].text(query, additional)
					return {"level": "text", "status": ret}
			if lvl >= 0 and success == False:
				if hasattr(self.plugins[name], 'raw'):
					ret = self.plugins[name].raw(query, additional)
					return {"level": "raw", "status": ret}
		except:
			print("ERROR in plugin: " + name)
			print('-'*60)
			traceback.print_exc(file=sys.stdout)
			print('-'*60)
			self.unload(name)
		return success
