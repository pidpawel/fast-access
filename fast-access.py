#!/usr/bin/env python2
# coding=UTF-8

import pygtk
pygtk.require('2.0')
import gtk
import os, sys
import ConfigParser
import gettext
from math import ceil

from libs.Plugins import *
from libs.Misc import *

gettext.bindtextdomain('messages', os.path.abspath(os.path.dirname(sys.argv[0]))+"/languages")
gettext.textdomain('messages')
_ = gettext.gettext

class FastAccess:
	plugins = Plugins()
	config = ConfigParser.ConfigParser()
	pluginButtons = {}

	def parseInput(self, widget, data=None):
		query = widget.get_text()
		slices = query.split(" ")
		ll = len(slices[0])

		self.pluginStore.clear()

		if ll > 0:
			found = []
			found.extend(self.plugins.listFeatures())

			for nam in self.plugins.loaded():
				found.append({	"plugin": nam,
								"feature": nam,
								"icon": self.plugins.plugins[nam].icon,
								"text": self.plugins.plugins[nam].name})

			for feature in found:
				dist = levenshtein(feature["feature"][:ll].lower(), slices[0].lower()) + 0.0
				feature["accuracy"] = ( ( (ll-dist)/ll )*90.0 ) - len(feature["feature"]) + dist

			found.extend(self.plugins.checkAll(query))
			found = self.plugins.sortFeatures(found)

			for feature in found:
				if feature["accuracy"] > 50:
					self.pluginStore.append(
											[self.getPixbufFromImage(feature["icon"]),
											feature["text"]+" ("+str(feature["accuracy"])+")",
											feature["plugin"],
											feature["feature"]])

			self.pluginView.get_selection().select_path(0)

	def executeInput(self, widget, data=None, data2=None):
		query = self.searchEntry.get_text()
		slices = query.split(" ")
		if len(query) > 0:
			if data != None:
				self.plugins.use(	"gtk",
									widget.get_model()[data][2],
									query, {"feature": widget.get_model()[data][3]})
		else:
			self.error(_("Just enter something. It will be easier for me to guess what do you want. Ya, rly."))

	def executeInputDefault(self, widget, data=None):
		query = self.searchEntry.get_text()
		self.executeInput(self.pluginView, 0)

	def about(self, widget, event):
		about = gtk.AboutDialog()
		about.set_position(gtk.WIN_POS_CENTER)
		about.set_icon(self.getPixbufFromImage("system-run.png", 12))
		about.set_program_name("Fast-access")
		about.set_version("v0.2")
		about.set_authors(["PidPawel - "+_("author")])
		about.set_license("Creative Commons BY-NC-SA http://creativecommons.org/licenses/by-nc-sa/2.5/pl/")
		about.set_copyright("© by PidPawel "+_("on license")+" Creative Commons BY-NC-SA")
		about.set_comments(_("Fast access to various websearch engines"))
		about.set_website("https://github.com/pidpawel/fast-access")
		about.set_logo(self.getPixbufFromImage("system-run.png", 48))
		about.run()
		about.destroy()

	def error(self, text):
		print(_("Error")+": " + text)
		box = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, text)
		box.set_title("Error")
		box.run()
		box.destroy()
		#sys.exit()

	def deleteEvent(self, widget, event, data=None):
		return False

	def destroy(self, widget, data=None, abc=None, bcd=None):
		self.plugins.unloadAll()
		print(_("Application closed."))
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.deleteEvent)
		self.window.connect("destroy", self.destroy)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_title("Fast-access")
		self.window.set_icon(self.getPixbufFromImage("system-run.png", 12))
		self.window.set_default_size(572, 83)
		self.window.set_border_width(10)

		self.searchEntry = gtk.Entry()
		self.searchEntry.set_size_request(0, 40)
		self.searchEntry.connect("changed", self.parseInput, None)
		self.searchEntry.connect("activate", self.executeInputDefault, None)

		self.searchImage = gtk.Image()
		self.searchImage.set_from_pixbuf(self.getPixbufFromImage("system-run.png", 48))
		self.searchImage.set_size_request(60,0)

		self.searchLine = gtk.HBox(False, 2)
		self.searchLine.set_size_request(0, 50)
		self.searchLine.pack_start(self.searchImage, False, False, 2)
		self.searchLine.pack_start(self.searchEntry, True, True)

		self.buttonSearch = gtk.Button(_("Search"))
		self.buttonHelp = gtk.Button(_("Help"))
		self.buttonCancel = gtk.Button(_("Cancel"))
		self.buttonFiller = gtk.Label()

		self.buttonSearch.connect("clicked", self.executeInputDefault, None)
		self.buttonHelp.connect("clicked", self.about, None)
		self.buttonCancel.connect("clicked", self.destroy, None)

		self.buttonsLine = gtk.HBox(True, 8)
		self.buttonsLine.pack_start(self.buttonHelp, True, True)
		self.buttonsLine.pack_start(self.buttonFiller, True, True)
		self.buttonsLine.pack_start(self.buttonCancel, True, True)
		self.buttonsLine.pack_start(self.buttonSearch, True, True)

		self.fileIcon = self.getSystemIcon(gtk.STOCK_FILE)

		self.pluginStore = gtk.ListStore(gtk.gdk.Pixbuf, str, str, str)

		self.pluginView = gtk.TreeView(self.pluginStore)
		self.pluginView.set_headers_visible(False)
		self.pluginView.connect("row-activated", self.executeInput)


		column = gtk.TreeViewColumn(_("Icon"), gtk.CellRendererPixbuf(), pixbuf=0)
		column.set_sort_column_id(0)
		self.pluginView.append_column(column)
		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=1)
		column.set_sort_column_id(1)
		self.pluginView.append_column(column)

		self.pluginWindow = gtk.ScrolledWindow()
		self.pluginWindow.set_size_request(0, 160)
		self.pluginWindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.pluginWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.pluginWindow.add(self.pluginView)

		self.layout = gtk.VBox(False, 6)
		self.layout.pack_start(self.searchLine, False, False)
		self.layout.pack_start(self.pluginWindow, True, True)
		self.layout.pack_start(self.buttonsLine, False, False)
		self.window.add(self.layout)

		self.accelgroup = gtk.AccelGroup()
		key, modifier = gtk.accelerator_parse('Escape')
		self.accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, self.destroy)
		self.window.add_accel_group(self.accelgroup)

		self.config.optionxform = str
		self.config.read([	os.path.expanduser('~/.fast-access.cfg'),
							'config.cfg',
							os.path.abspath(os.path.dirname(sys.argv[0]))+"/config.cfg",
							os.path.abspath(os.path.dirname(sys.argv[0]))+"/example.cfg"
							])
		self.plugins.setGtk(self.window)
		self.plugins.setConfig(self.config)

		blacklist = self.config.get('plugins', 'blacklist').split(" ")
		for filename in os.listdir(os.path.abspath(os.path.dirname(sys.argv[0]))+"/plugins"):
			slices = filename.split('.')
			if slices[-1] == "py" and slices[0] != "__init__" and not slices[0] in blacklist:
				self.plugins.load(slices[0])

		for nam in self.plugins.loaded():
			self.pluginStore.append([
										self.getPixbufFromImage(self.plugins.plugins[nam].icon),
										self.plugins.plugins[nam].name,
										nam,
										nam])


		print(" >>> Interface loaded <<< ")
		self.window.show_all()

	def getSystemIcon(self, name, size=24):
		theme = gtk.icon_theme_get_default()
		return theme.load_icon(name, size, 0)
	def getPixbufFromImage(self, name, size=24):
		img = gtk.Image()
		img.set_from_file(os.path.abspath(os.path.dirname(sys.argv[0]))+"/icons/"+name)
		try:
			return img.get_pixbuf().scale_simple(size, size, gtk.gdk.INTERP_BILINEAR)
		except:
			return None

	def main(self):
		gtk.main()

if __name__ == "__main__":
	truapp = FastAccess()
	truapp.main()
