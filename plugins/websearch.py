# coding=UTF8
import sys, os
import ConfigParser
import urllib2
from . import Template

class plugin(Template):
	name = "Wyszukiwarki internetowe"
	icon = "web.png"
	config = False

	def __init__(self, config):
		self.config = config
		self.engines = self.config.items('websearch')

	def featuresList(self):
		res = []
		for engine, url in self.engines:
			res.append({"plugin": "websearch",
						"feature": engine.lower(),
						"icon": engine+".ico",
						"text": engine})
		return res

	def parse(self, engine, query):
		url = None
		for eng in self.engines:
			if eng[0].lower() == engine:
				url = eng[1]
				break
		if url == None:
			url = self.config.get('browser', 'default_search')

		url = url.replace("{query}", urllib2.quote(query), 1)
		return url

	def gtk(self, window, query, additional={}):
		slices = query.split(" ")
		try:
			engine = additional["feature"]
			query = " ".join(slices[1:])
		except:
			if slices[0] in self.engines:
				engine = slices[0]
				query = " ".join(slices[1:])
			else:
				engine = ""
		print("Query: " + query)
		url = self.parse(engine, query)
		print("Redirecting to: " + url)
		os.system(self.config.get('browser', 'command').replace('{url}', url, 1))
		if self.config.getboolean('Global', 'wmctrl'):
			os.system("wmctrl -a" + self.config.get('browser', 'name'))
		window.destroy()
