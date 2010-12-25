# coding=UTF8
import sys
import pygtk
pygtk.require('2.0')
import gtk
from . import Template

class plugin(Template):
	name = "Sample Plugin"

	def dynamicCheck(self, query, additional={}):
		if query.startswith("a"):
			return [{"plugin": "sample", "feature": "agugugaga", "icon": "none.png", "text": "Aguggabagalugagigi", "accuracy": "99"}]
		return False

	def raw(self, query, additional={}):
		return("Just let me try to do: "+query+"... Ya, rly.")

	def text(self, query, additional={}):
		return("Binga, ponga\nUba, bonga\nPlimpa, plobmba!")

	def gtk(self, window, query, additional={}):
		box = gtk.MessageDialog(window, gtk.DIALOG_DESTROY_WITH_PARENT,
									gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
									"Query is: " + query)
		box.set_position(gtk.WIN_POS_CENTER)
		box.run()
		box.destroy()
