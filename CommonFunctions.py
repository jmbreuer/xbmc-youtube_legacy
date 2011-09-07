'''
   YouTube plugin for XBMC
   Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys, urllib2, re, os, socket, inspect
import xbmc

class CommonFunctions():
	__settings__ = sys.modules[ "__main__"].__settings__ 
	__plugin__ = sys.modules[ "__main__"].__plugin__
	__language__ = sys.modules[ "__main__" ].__language__
	__dbglevel__ = sys.modules[ "__main__" ].__dbglevel__

	if sys.platform == "win32":
		port = 59994
		__socket__ = (socket.gethostname(), port)
	else:
		__socket__ = os.path.join( xbmc.translatePath( "special://temp" ), 'commoncache.socket')

	def stripTags(self, html):
		sub_start = html.find("<")
		sub_end = html.find(">")
		while sub_start < sub_end and sub_start > -1:
			html = html.replace(html[sub_start:sub_end + 1], "").strip()
			sub_start = html.find("<")
			sub_end = html.find(">")

		return html

	def getDOMContent(self, html, name, match): # convert to log.
		self.log("match:" + match, 2)
		start = html.find(match)
		if name == "img":
			endstr = ">"
		else:
			endstr = "</" + name + ">"
		end = html.find(endstr, start)

		pos = html.find("<" + name, start + 1 )

		self.log(str(start) + " < " + str(end) + " pos = " + str(pos), 2)

		while pos < end and pos != -1:
			pos = html.find("<" + name, pos + 1)
			if pos > -1:
				tend = html.find(endstr, end + len(endstr))
				if tend != -1:
					end = tend
			self.log("loop: " + str(start) + " < " + str(end) + " pos = " + str(pos), 3)

		html = html[start:end + len(endstr)]
		self.log("done html length: " + str(len(html)) + repr(html), 2)
		return html

	def parseDOM(self, html, name = "", attrs = {}, ret = False):
		# html <- text to scan.
		# name <- Element name
		# attrs <- { "id": "my-div", "class": "oneclass.*anotherclass", "attribute": "a random tag" }
		# ret <- Return content of element
		# Default return <- Returns a list with the content
		self.log(repr(name) + " - " + repr(attrs) + " - " + repr(ret) + " - " + str(type(html)), 1)

		if type(html) != type([]):
			html = [html]
		
		if not name.strip():
			self.log("Missing tag name")
			return ""

		ret_lst = []

		# Find all elements with the tag
			
		i = 0
		for item in html:
			item = item.replace("\n", "")
			lst = []

			for key in attrs:
				scripts = [ '(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"][^>]*?>))', # Hit often.
					    '(<' + name + ' (?:' + key + '=[\'"]' + attrs[key] + '[\'"])[^>]*?>)', # Hit twice
					    '(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"])[^>]*?>)'] # 

				lst2 = []
				for script in scripts:
					if len(lst2) == 0:
						#self.log("scanning " + str(i) + " " + str(len(lst)) + " Running :" + script, 2)
						lst2 = re.compile(script).findall(item)
						i += 1
				if len(lst2) > 0:
					if len(lst) == 0:
						lst = lst2;
						lst2 = []
					else:
						test = range(len(lst))
						test.reverse()
						for i in test: # Delete anything missing from the next list.
							if not lst[i] in lst2:
								self.log("Purging mismatch " + str(len(lst)) + " - " + repr(lst[i]), 1)
								del(lst[i])
	
			if len(lst) == 0 and attrs == {}:
				self.log("no list found, making one on just the element name", 1)
				lst = re.compile('(<' + name + '[^>]*?>)').findall(item)
	
			if ret != False:
				self.log("Getting attribute %s content for %s matches " % ( ret, len(lst) ), 2)
				lst2 = []
				for match in lst:
					lst2 += re.compile('<' + name + '.*' + ret + '=[\'"]([^>]*?)[\'"].*>').findall(match)
				lst = lst2
			else:
				self.log("Getting element content for %s matches " % len(lst), 2)
				lst2 = []
				for match in lst:
					temp = self.getDOMContent(item, name, match)
					item = item.replace(temp, "")
					lst2.append(temp[temp.find(">")+1:temp.rfind("</" + name + ">")])
				lst = lst2
			ret_lst += lst

		self.log("Done", 1)
		return ret_lst

	def _fetchPage(self, params = {}):
		get = params.get
		link = get("link")
		ret_obj = {}
		self.log("called for : " + repr(params))

		if not link or int(get("error", "0")) > 2 :
			self.log("giving up")
			ret_obj["status"] = 500
			return ret_obj

		request = urllib2.Request(link)
		request.add_header('User-Agent', self.USERAGENT)

		try:
			self.log("connecting to server...", 1)

			con = urllib2.urlopen(request)
			
			ret_obj["content"] = con.read()
			ret_obj["new_url"] = con.geturl()
			ret_obj["header"] = str(con.info())
			con.close()

			# Return result if it isn't age restricted
			self.log("Done")
			ret_obj["status"] = 200
			return ret_obj
		
		except urllib2.HTTPError, e:
			err = str(e)
			self.log("HTTPError : " + err)
			self.log("HTTPError - Headers: " + str(e.headers) + " - Content: " + e.fp.read())
			
			params["error"] = str(int(get("error", "0")) + 1)
			ret = self._fetchPage(params)
			if not ret.has_key("content") and e.fp:
				ret["content"] = e.fp.read()
			return ret

			ret_obj["status"] = 505
			return ret_obj

	def log(self, description, level = 0):
		if self.__dbg__ and self.__dbglevel__ > level:
			xbmc.log("[%s] %s : '%s'" % (self.__plugin__, inspect.stack()[2][3], description), xbmc.LOGNOTICE)
