# coding=UTF8
import sys, os
import ConfigParser
from . import Template
import gmenu

class plugin(Template):
	name = "Run"
	icon = "web.png"
	config = False

	def parseTree(self, tree):
		rt = []
		#print tree.contents
		for a in tree.contents:
			if isinstance(a, gmenu.Directory):
				#print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
				rt.extend(self.parseTree(a))
			else:
				rt.append({"plugin": "run",
						"feature": a.get_exec(),
						"icon": a.get_icon(),
						"text": a.get_display_name()})
		return rt

	def parseFile(self, fil):
		return self.parseTree(gmenu.lookup_tree (fil, gmenu.FLAGS_INCLUDE_EXCLUDED).root)

	def __init__(self, config):
		self.config = config

	def featuresList(self):
		menu_files = ["applications.menu", "settings.menu"]

		found = []
		for menu_file in menu_files:
			if menu_file == "applications.menu" and os.environ.has_key ("XDG_MENU_PREFIX"):
				menu_file = os.environ["XDG_MENU_PREFIX"] + menu_file
			print menu_file
			found.extend(self.parseFile(menu_file))
#		print found
		return found

	def gtk(self, window, query, additional={}):
		print "lulz"
