class Template():
	name = "Noname plugin"
	icon = "none.png"
	config = False

	def __init__(self, config):
		self.config = config

	def dynamicCheck(self, query, additional={}):
		return False

	def featuresList(self):
		return []
