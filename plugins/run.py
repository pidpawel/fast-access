# coding=UTF8
import sys, os
import ConfigParser
from . import Template
import gmenu

class plugin(Template):
	name = "Run"
	icon = "system-run.png"
	config = False

	def parseTree(self, tree):
		rt = []
		for a in tree.contents:
			if isinstance(a, gmenu.Directory):
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
			found.extend(self.parseFile(menu_file))
		return found

	def gtk(self, window, query, additional={}):
		slices = query.split(" ")
		try:
			app = additional["feature"].split(" ")[0]
			query = " ".join(slices[1:])
		except:
			box = gtk.MessageDialog(window, gtk.DIALOG_DESTROY_WITH_PARENT,
							gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
							"I don't know such app.")
			box.set_position(gtk.WIN_POS_CENTER)
			box.run()
			box.destroy()
			return False

		print app + " " + query
		os.system(app + " " + query + " &")
		if self.config.getboolean('Global', 'wmctrl'):
			os.system("wmctrl -a" + app)
		window.destroy()

