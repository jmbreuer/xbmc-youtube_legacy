import xml.dom.minidom as minidom
import io, inspect

class xbmcSettings():
	
	def __init__(self):
		self.settingsString = {}
		self.path = ""
	
	def load_strings(self, path = "./resources/settings.xml"):
		print " *** *** loading settings strings *** ***"
		self.path = path
		file = io.open(path).read()
		dom = minidom.parseString(file);
		strings = dom.getElementsByTagName("setting")
		
		for string in strings:
			self.settingsString[string.getAttribute("id")] = string.getAttribute("value")		

	def __call__(self, id = "", value = ""):
		
		if not self.settingsString:
			self.load_strings()
		
		if value:
			if self.path.find("settings-logged-in") > -1:
				org = io.open(self.path).read()
				if org.find(id + "\" value=\"") > -1:
					start = org.find(id + "\" value=\"") + len("\" value=\"") + len(id)
					org_val = org[start:org.find("\"", start)]
					org = org.replace(org_val, value)
				else:
					org = org.replace("</settings>", "    <setting id=\"%s\" value=\"%s\" />\n</settings>" % ( id, value))
				test = io.open(self.path, "w")
				test.write(org)

			self.settingsString[id] = value
		
		elif id in self.settingsString:
			return self.settingsString[id]
		
		return ""

	def __getattr__(self, name):
		return self

if __name__ == "__main__":
	x1 = xbmcSettings()
	print "x1: " + x1.getSetting("downloads")
	print "setting x1 = funkytown"
	x1.setSetting("downloads", "funkytown" )
	x2 = xbmcSettings()
	print "x2: " + x2.getSetting("downloads")
	print "x1: " + x1.getSetting("downloads")
