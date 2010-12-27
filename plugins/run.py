# coding=UTF8
import sys, os
import ConfigParser
from . import Template
import ConfigParser

class plugin(Template):
	name = "Run"
	icon = "system-run.png"
	config = False

	def parseFile(self, name):
		cp = ConfigParser.RawConfigParser()
		cp.read("/usr/share/applications/"+name)
		print name
		stop = False
		try:
			if cp.getboolean("Desktop Entry", "NoDisplay") == "true":
				stop = True
		except:
			stop = False

		if stop == False:
			text = ""
			try:
				text = cp.get("Desktop Entry", "GenericName[pl]")
			except:
				try:
					text = cp.get("Desktop Entry", "GenericName")
				except:
					try:
						text = cp.get("Desktop Entry", "Name")
					except:
						return None
			try:
				icon = cp.get("Desktop Entry", "Icon")
			except:
				print " >>> Brak ikony "+name
				icon = ""
			return {
					"plugin": "run",
					"feature": cp.get("Desktop Entry", "Exec"),
					"icon": icon,
					"text": text
					}
		else:
			return None

	def __init__(self, config):
		self.config = config

	def featuresList(self):
		ret = []
		apps = []
		try:
			apps.extend(os.listdir("/usr/share/applications/"))
		except:
			pass
		try:
			apps.extend(os.listdir("/usr/local/share/applications/"))
		except:
			pass

		for app in apps:
			if app.split(".")[-1] == "desktop":
				res = self.parseFile(app)
				if res != None:
					ret.append(res)
		return ret

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
