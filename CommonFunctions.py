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

import sys, urllib, re, os, socket, time, hashlib
import xbmc
import StorageServer		
try: import xbmcvfs
except ImportError: import xbmcvfsdummy as xbmcvfs

class CommonFunctions():
	__settings__ = sys.modules[ "__main__"].__settings__ 
	__plugin__ = sys.modules[ "__main__"].__plugin__
	__language__ = sys.modules[ "__main__" ].__language__
	if sys.platform == "win32":
		port = 59994
		__socket__ = (socket.gethostname(), port)
	else:
		__socket__ = os.path.join( xbmc.translatePath( "special://temp" ), 'commoncache.socket')
	__store_in_settings__ = False
	__disable_cache__ = False
	__soccon__ = False
	__table_name__ = False

	def cacheFunction(self, funct = False, *args):
		if self.__disable_cache__:
			return funct(*args)
		elif funct and self.__table_name__:
			name = repr(funct)
			name = name[name.find("method") + 7 :name.find(" of ")]
			print self.__plugin__ + " _cacheFunction: " + name  + " - " + str(repr(args))[0:50]

			ret_val = False

			# Build unique name
			keyhash = hashlib.md5()
			for params in args:
				if type(params) == type({}):
					for key in sorted(params.iterkeys()):
						if key not in [ "new_results_function" ]:
							keyhash.update("'%s'='%s'" % (key, params[key]))
				elif type(params) == type([]):
					keyhash.update(",".join(["%s" % el for el in params]))
				else:
					keyhash.update(params)

			name += "|" + keyhash.hexdigest() + "|"

			cache = self.sqlGet("cache" + name)
			if cache.strip() == "":
				cache = {}
			else:
				cache = eval(cache)

			if name in cache:
				#print self.__plugin__ + " _cacheFunction returning cache for : " + name
				if cache[name]["timestamp"] > time.time() - (3600 * 24):
					ret_val = cache[name]["res"]
				else:
					print self.__plugin__ + " _cacheFunction Deleting old cache"
					del(cache[name])

			if not ret_val: 
				print self.__plugin__ + " _cacheFunction Sending request " + str(len(args)) + " - " + str(repr(args))[0:50]
				ret_val = funct(*args)
				if ret_val[1] == 200:
					cache[name] = { "timestamp": time.time(),
							"res": ret_val}
					print self.__plugin__ + " _cacheFunction saving: " + name  + str(repr(cache[name]["res"]))[0:50]
					self.sqlSet("cache" + name, repr(cache))

			if ret_val:
				print self.__plugin__ + " _cacheFunction returning : " + name # + repr(ret_val)
				return ret_val

		print self.__plugin__ + " _cacheFunction Error " 
		return ( "", 500 )

	def getOldCache(self):
		return True

	def cleanCache(self):
		cache = {}
		return False
		if self.sqlGet("cache"):
			cache = eval(self.sqlGet("cache"))

		if cache:
			for item in cache:
				if cache[item]["timestamp"] < time.time() - (3600 * 24):
					del(cache[item])
				## Expand this to refresh content instead of deleting it if the item is acced over a certain threshold.

			self.sqlSet("cache", repr(cache))
			return True
		return False

	def lock(self, name):
		if self.__dbg__:
			print self.__plugin__ + " lock " + name

		if self.sqlConnect():
			data = repr({ "action": "lock", "table": self.__table_name__, "name": name})
			storage_server = StorageServer.StorageServer()
			storage_server.send(self.__soccon__, data)
			res = storage_server.recv(self.__soccon__)
			if res:
				if eval(res.strip()) == "true":
					if self.__dbg__:
						print self.__plugin__ + " lock done : " + res.strip()
					return True

		if self.__dbg__:
			print self.__plugin__ + " lock failed"
			return False

	def unlock(self, name):
		if self.__dbg__:
			print self.__plugin__ + " unlock " + name

		if self.sqlConnect():
			data = repr({ "action": "unlock", "table": self.__table_name__, "name": name})
			storage_server = StorageServer.StorageServer()
			storage_server.send(self.__soccon__, data)
			res = storage_server.recv(self.__soccon__)
			if res:
				if eval(res.strip()) == "true":
					if self.__dbg__:
						print self.__plugin__ + " unlock done : " + res.strip()
					return True
		if self.__dbg__:
			print self.__plugin__ + " unlock failed : "
		return False

	def sqlConnect(self):
		if sys.platform == "win32":
			self.__soccon__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.__soccon__ = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		start = time.time()
		connected = False
		try:
			self.__soccon__.connect(self.__socket__)
			connected= True
		except socket.error, e:
			print self.__plugin__ + " sqlConnect exception : " + repr(e)
			if e.errno in [ 111 ]:
				print self.__plugin__ + " sqlConnect StorageServer isn't running"

		return connected

	def sqlSet(self, name, data):
		if self.__store_in_settings__:
			print self.__plugin__ + " sqlSet ( in settings ) " + name
			self.__settings__.setSetting(name, data)
		else:
			print self.__plugin__ + " sqlSet " + name
			if self.sqlConnect():
				temp = repr({ "action": "set", "table": self.__table_name__, "name": name, "data": data})
				storage_server = StorageServer.StorageServer()
				res = storage_server.send(self.__soccon__, temp)
				print self.__plugin__ + " sqlset GOT " + repr(res)

	def sqlGet(self, name):
		if self.__store_in_settings__:
			print self.__plugin__ + " sqlGet ( from settings ) " + name + repr(self.__store_in_settings__)
			return self.__settings__.getSetting(name)
		else:
			print self.__plugin__ + " sqlGet " + name
			if self.sqlConnect():
				storage_server = StorageServer.StorageServer()
				print self.__plugin__ + " sqlGet " + name 
				storage_server.send(self.__soccon__, repr({ "action": "get", "table": self.__table_name__, "name": name}))
				print self.__plugin__ + " sqlGet - receive "
				res = storage_server.recv(self.__soccon__)

				print self.__plugin__ + " sqlGet res : " + str(len(res))
				if res:
					res = eval(res.strip())
					return res.strip() # We return " " as nothing. Strip it out.

		return ""



	def stripTags(self, html):
		sub_start = html.find("<")
		sub_end = html.find(">")
		while sub_start < sub_end and sub_start > -1:
			html = html.replace(html[sub_start:sub_end + 1], "").strip()
			sub_start = html.find("<")
			sub_end = html.find(">")

		return html

	def getDOMContent(self, html, name, match):
		#print self.__plugin__ + " getDOMContent match: " + match
		start = html.find(match)
		if name == "img":
			endstr = ">"
		else:
			endstr = "</" + name + ">"
		end = html.find(endstr, start)

		pos = html.find("<" + name, start + 1 )

		#print self.__plugin__ + " getDOMContent " + str(start) + " < " + str(end) + " pos = " + str(pos)

		while pos < end and pos != -1:
			pos = html.find("<" + name, pos + 1)
			if pos > -1:
				tend = html.find(endstr, end + len(endstr))
				if tend != -1:
					end = tend
			#print self.__plugin__ + " getDOMContent2 loop: " + str(start) + " < " + str(end) + " pos = " + str(pos)

		#print self.__plugin__ + " getDOMContent XXX: " + str(start) + " < " + str(end) + " pos = " + str(pos)
		html = html[start:end + len(endstr)]
		#print self.__plugin__ + " getDOMContent done html length: " + str(len(html)) + repr(html)
		return html

	def parseDOM(self, html, name = "", attrs = {}, ret = False):
		# html <- text to scan.
		# name <- Element name
		# attrs <- { "id": "my-div", "class": "oneclass.*anotherclass", "attribute": "a random tag" }
		# ret <- Return content of element
		# Default return <- Returns a list with the content
		
		if self.__dbg__:
			print self.__plugin__ + " parseDOM : " + repr(name) + " - " + repr(attrs) + " - " + repr(ret) + " - " + str(type(html))
		if type(html) == type([]):
			html = "".join(html)
		html = html.replace("\n", "")
		if not name.strip():
			if self.__dbg__:
				print self.__plugin__ + " parseDOM - Missing tag name "
			return ""

		lst = []

		# Find all elements with the tag
			
		i = 0
		for key in attrs:
			scripts = [ '(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"][^>]*?>))', # Hit often.
				    '(<' + name + ' (?:' + key + '=[\'"]' + attrs[key] + '[\'"])[^>]*?>)', # Hit twice
				    '(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"])[^>]*?>)'] # 

			lst2 = []
			for script in scripts:
				if len(lst2) == 0:
					#print self.__plugin__ + " parseDOM scanning " + str(i) + " " + str(len(lst)) + " Running :" + script
					lst2 = re.compile(script).findall(html)
					#print self.__plugin__ + " parseDOM scanning " + str(i) + " " + str(len(lst2)) + " Result : " #+ repr(lst2[:2])
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
							if self.__dbg__:
								print self.__plugin__ + " parseDOM Purging mismatch " + str(len(lst)) + " - " + repr(lst[i])
							del(lst[i])

		if len(lst) == 0 and attrs == {}:
			#print self.__plugin__ + " parseDOM no list found, making one on just the element name"
			lst = re.compile('(<' + name + '[^>]*?>)').findall(html)

		if ret != False:
			#print self.__plugin__ + " parseDOM Getting attribute %s content for %s matches " % ( ret, len(lst) )
			lst2 = []
			for match in lst:
				lst2 += re.compile('<' + name + '.*' + ret + '=[\'"]([^>]*?)[\'"].*>').findall(match)
			lst = lst2
		else:
			#print self.__plugin__ + " parseDOM Getting element content for %s matches " % len(lst)
			lst2 = []
			for match in lst:
				temp = self.getDOMContent(html, name, match)
				html = html.replace(temp, "")
				lst2.append(temp[temp.find(">")+1:temp.rfind("</" + name + ">")])
			lst = lst2

		if self.__dbg__:
			print self.__plugin__ + " parseDOM Done " + str(len(lst))
		return lst

	def _fetchPage(self, params = {}):
		get = params.get
		link = get("link")
		ret_obj = {}
		if self.__dbg__:
			print self.__plugin__ + " _fetchPage called for : " + repr(params)

		if not link or int(get("error", "0")) > 2 :
			if self.__dbg__:
				print self.__plugin__ + " _fetchPage giving up "
			ret_obj["status"] = 500
			return ret_obj

		request = urllib2.Request(link)
		request.add_header('User-Agent', self.USERAGENT)

		try:
			if self.__dbg__:
				print self.__plugin__ + " _fetchPage connecting to server... "

			con = urllib2.urlopen(request)
			
			ret_obj["content"] = con.read()
			ret_obj["new_url"] = con.geturl()
			ret_obj["header"] = str(con.info())
			con.close()

			# Return result if it isn't age restricted
			if self.__dbg__:
				print self.__plugin__ + " _fetchPage done"
			ret_obj["status"] = 200
			return ret_obj
		
		except urllib2.HTTPError, e:
			err = str(e)
			if self.__dbg__:
				print self.__plugin__ + " _fetchPage HTTPError : " + err
				print self.__plugin__ + " _fetchPage HTTPError - Headers: " + str(e.headers) + " - Content: " + e.fp.read()
			
			params["error"] = str(int(get("error", "0")) + 1)
			ret = self._fetchPage(params)
			if not ret.has_key("content") and e.fp:
				ret["content"] = e.fp.read()
			return ret

			ret_obj["status"] = 505
			return ret_obj

