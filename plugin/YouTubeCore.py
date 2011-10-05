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

import sys, urllib, urllib2, re, time, socket
import xml.dom.minidom as minidom
try: import simplejson as json
except ImportError: import json
#from xml.dom.minidom import parseString

# ERRORCODES:
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class url2request(urllib2.Request):
	"""Workaround for using DELETE with urllib2"""
	def __init__(self, url, method, data=None, headers={}, origin_req_host=None, unverifiable=False):
		self._method = method
		urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)

	def get_method(self):
		if self._method:
			return self._method
		else:
			return urllib2.Request.get_method(self) 

class YouTubeCore():
	
	APIKEY = "AI39si6hWF7uOkKh4B9OEAX-gK337xbwR9Vax-cdeF9CF9iNAcQftT8NVhEXaORRLHAmHxj6GjM-Prw04odK4FxACFfKkiH9lg";
	
	#===============================================================================
	# The time parameter restricts the search to videos uploaded within the specified time. 
	# Valid values for this parameter are today (1 day), this_week (7 days), this_month (1 month) and all_time. 
	# The default value for this parameter is all_time.
	# 
	# This parameter is supported for search feeds as well as for the top_rated, top_favorites, most_viewed, 
	# most_popular, most_discussed and most_responded standard feeds.
	#===============================================================================

	urls = {};
	urls['batch'] = "http://gdata.youtube.com/feeds/api/videos/batch"
	urls['thumbnail'] = "http://i.ytimg.com/vi/%s/0.jpg"
	urls['remove_watch_later'] = "http://www.youtube.com/addto_ajax?action_delete_from_playlist=1"	


	def __init__(self):
		self.settings = sys.modules[ "__main__" ].settings
		self.language = sys.modules[ "__main__" ].language
		self.plugin = sys.modules[ "__main__" ].plugin
		self.dbg = sys.modules[ "__main__" ].dbg
		self.storage = sys.modules[ "__main__" ].storage
		self.cache = sys.modules[ "__main__" ].cache
		self.login = sys.modules[ "__main__" ].login
		self.utils = sys.modules[ "__main__" ].utils
		self.common = sys.modules[ "__main__" ].common
		
		#urllib2.install_opener(sys.modules[ "__main__" ].opener)

		timeout = [5, 10, 15, 20, 25][int(self.settings.getSetting("timeout"))]
		if not timeout:
			timeout = "15"
		socket.setdefaulttimeout(float(timeout))
		return None
	
	def delete_favorite(self, params={}):
		get = params.get
		
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/favorites"
		delete_url += "/" + get('editid') 
		result = self._fetchPage({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})
		return (result["content"], result["status"])
	
	def remove_contact(self, params={}):
		get = params.get
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/contacts" 
		delete_url += "/" + get("contact")
		result = self._fetchPage({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})
		return (result["content"], result["status"])

	def remove_subscription(self, params={}):
		get = params.get
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions"
		delete_url += "/" + get("editid")
		result = self._fetchPage({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})
		return (result["content"], result["status"])
			
	def add_contact(self, params={}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/contacts"
		add_request = '<?xml version="1.0" encoding="UTF-8"?> <entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><yt:username>%s</yt:username></entry>' % get("contact")
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		return (result["content"], result["status"])
		
	def add_favorite(self, params={}):
		get = params.get 
		url = "http://gdata.youtube.com/feeds/api/users/default/favorites"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom"><id>%s</id></entry>' % get("videoid")
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		return (result["content"], result["status"])
		
	def add_subscription(self, params={}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"> <category scheme="http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat" term="user"/><yt:username>%s</yt:username></entry>' % get("channel")
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		return (result["content"], result["status"])
	
	def add_playlist(self, params={}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/playlists"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><title type="text">%s</title><summary>%s</summary></entry>' % (get("title"), get("summary"))
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		return (result["content"], result["status"])
		
	def del_playlist(self, params={}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/playlists/%s" % (get("playlist"))
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})
		return (result["content"], result["status"])

	def add_to_playlist(self, params={}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/playlists/%s" % get("playlist")
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><id>%s</id></entry>' % get("videoid")
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		return (result["content"], result["status"])
	
	def remove_from_playlist(self, params={}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/playlists/%s/%s" % (get("playlist"), get("playlist_entry_id"))
		result = self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})
		return (result["content"], result["status"])
	
	def getFolderInfo(self, xml, params={}):
		get = params.get
		result = ""
		
		dom = minidom.parseString(xml);
		links = dom.getElementsByTagName("link");
		entries = dom.getElementsByTagName("entry");
		next = False
		
		#find out if there are more pages
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = True
					break
		
		folders = [];
		for node in entries:
			folder = {};
			
			folder["login"] = "true"
			folder['Title'] = node.getElementsByTagName("title").item(0).firstChild.nodeValue.replace('Activity of : ', '').replace('Videos published by : ', '').encode("utf-8");
			folder['published'] = self._getNodeValue(node, "published", "2008-07-05T19:56:35.000-07:00")
			
			if node.getElementsByTagName("id"):
				entryid = self._getNodeValue(node, "id", "")
				entryid = entryid[entryid.rfind(":") + 1:]
				folder["editid"] = entryid
			
			thumb = ""
			if get("user_feed") == "contacts":
				folder["thumbnail"] = "user"
				folder["contact"] = folder["Title"]
				folder["store"] = "contact_options"
				folder["folder"] = "true"
			
			if get("user_feed") == "subscriptions":
				folder["channel"] = folder["Title"]
			
			if get("user_feed") == "playlists":
				folder['playlist'] = self._getNodeValue(node, 'yt:playlistId', '')
				folder["user_feed"] = "playlist"

			params["thumb"] = "true"
			thumb = self.storage.retrieve(params, "thumbnail", folder)
			if thumb:
				folder["thumbnail"] = thumb 
						
			folders.append(folder);
		
		if next:
			self.utils.addNextFolder(folders, params)
		
		return folders;
	
	def getBatchDetailsOverride(self, items, params={}):
		ytobjects = []
		videoids = []
		
		for video in items:
			for k, v in video.items():
				if k == "videoid":
					videoids.append(v)
		
		(ytobjects, status) = self.getBatchDetails(videoids, params)
		
		for video in items:
			videoid = video["videoid"]
			for item in ytobjects:
				if item['videoid'] == videoid:
					for k, v in video.items():
						item[k] = v
		
		while len(items) > len(ytobjects):
			ytobjects.append({'videoid': 'false'});
		
		return (ytobjects, 200)
	
	def getBatchDetailsThumbnails(self, items, params={}):
		ytobjects = []
		videoids = []
		
		for (videoid, thumb) in items:
			videoids.append(videoid)
		
		(tempobjects, status) = self.getBatchDetails(videoids, params)
		
		for i in range(0, len(items)):
			(videoid, thumbnail) = items[i]
			for item in tempobjects:
				if item['videoid'] == videoid:
					item['thumbnail'] = thumbnail
					ytobjects.append(item)					

		while len(items) > len(ytobjects):
			ytobjects.append({'videoid': 'false'});
		
		return (ytobjects, 200)

	def getBatchDetails(self, items, params={}):
		request_start = "<feed xmlns='http://www.w3.org/2005/Atom'\n xmlns:media='http://search.yahoo.com/mrss/'\n xmlns:batch='http://schemas.google.com/gdata/batch'\n xmlns:yt='http://gdata.youtube.com/schemas/2007'>\n <batch:operation type='query'/> \n"
		request_end = "</feed>"
		
		video_request = ""
		
		ytobjects = []
		status = 500
		i = 1
		## Call to cache
		# Filter matches.
		# Run the following for the missing.
		# Update cache in the end.

		temp_objs = self.cache.sqlGetMulti("videoidcache", items)
		#status = 200
		#return ( ytobjects, status)
		for index, videoid in enumerate(items):
			if index < len(temp_objs):
				if temp_objs[index]:
					ytobjects.append(eval(temp_objs[index]))
					continue
			if videoid:
				video_request += 	"<entry> \n <id>http://gdata.youtube.com/feeds/api/videos/" + videoid + "</id>\n</entry> \n"
				if i == 50:
					final_request = request_start + video_request + request_end
					rstat = 403
					while rstat == 403:
						result = self._fetchPage({"link": "http://gdata.youtube.com/feeds/api/videos/batch", "api": "true", "request": final_request})
						rstat = self.common.parseDOM(result["content"], "batch:status", ret="code")
						if len(rstat) > 0:
							if int(rstat[len(rstat) - 1]) == 403:
								self.common.log("quota exceeded. Waiting 5 seconds. " + repr(rstat))
								rstat = 403
								time.sleep(5)

					temp = self.getVideoInfo(result["content"], params)
					ytobjects += temp
					video_request = ""
					i = 1
				i += 1
		
		if i > 1:
			final_request = request_start + video_request + request_end
			result = self._fetchPage({"link": "http://gdata.youtube.com/feeds/api/videos/batch", "api": "true", "request": final_request})
				
			temp = self.getVideoInfo(result["content"], params)
			ytobjects += temp

			save_data = {}
			for item in ytobjects:
				save_data[item["videoid"]] = repr(item)
			self.cache.sqlSetMulti("videoidcache", save_data)

		if len(ytobjects) > 0:
			status = 200

		return (ytobjects, status)
		
	#===============================================================================
	#
	# Internal functions to YouTubeCore.py
	#
	# Return should be value(True for bool functions), or False if failed.
	#
	# False MUST be handled properly in External functions
	#
	#===============================================================================

	def _fetchPage(self, params={}): # This does not handle cookie timeout for _httpLogin
		get = params.get
		link = get("link")
		ret_obj = { "status": 500, "content": ""}

		if (get("url_data") or get("request")):
			self.common.log("called for : " + repr(params['link']))
		else:
			self.common.log("called for : " + repr(params))

		if get("auth", "false") == "true":
			self.common.log("got auth")
			if self._getAuth():
				if link.find("?") > -1:
					link += "&oauth_token=" + self.settings.getSetting("oauth2_access_token")
				else:
					link += "?oauth_token=" + self.settings.getSetting("oauth2_access_token")

				self.common.log("updated link: " + link)
			else:
				self.common.log("couldn't get login token")

		if not link or int(get("error", "0")) > 2 :
			self.common.log("giving up ")
			return ret_obj

		if get("url_data"):
			request = urllib2.Request(link, urllib.urlencode(get("url_data")))
			request.add_header('Content-Type', 'application/x-www-form-urlencoded')
		elif get("request", "false") == "false":
			request = url2request(link, get("method", "GET"));
		else:
			self.common.log("got request")
			request = urllib2.Request(link, get("request"))
			request.add_header('X-GData-Client', "")
			request.add_header('Content-Type', 'application/atom+xml') 
			request.add_header('Content-Length', str(len(get("request")))) 

		if get("api", "false") == "true":
			self.common.log("got api")
			request.add_header('GData-Version', '2') #confirmed
			request.add_header('X-GData-Key', 'key=' + self.APIKEY)

		else:
			request.add_header('User-Agent', self.common.USERAGENT)

			if get("no-language-cookie", "false") == "false":
				request.add_header('Cookie', 'PREF=f1=50000000&hl=en')
		
		if get("login", "false") == "true":
			self.common.log("got login")
			if (self.settings.getSetting("username") == "" or self.settings.getSetting("user_password") == ""):
				self.common.log("_fetchPage, login required but no credentials provided")
				ret_obj["status"] = 303
				ret_obj["content"] = self.language(30622)
				return ret_obj
			# This should be a call to self.login._httpLogin()
			if self.settings.getSetting("login_info") != "":
				self.common.log("returning existing login info: " + self.settings.getSetting("login_info"))
				info = self.settings.getSetting("login_info")
				request.add_header('Cookie', 'LOGIN_INFO=' + info)
		
		if get("auth", "false") == "true":
			self.common.log("got auth")
			if self._getAuth():
				request.add_header('Authorization', 'GoogleLogin auth=' + self.settings.getSetting("auth"))
			else:
				self.common.log("couldn't get login token")
		
		try:
			self.common.log("connecting to server... ")

			con = urllib2.urlopen(request)
			
			ret_obj["content"] = con.read()
			ret_obj["new_url"] = con.geturl()
			ret_obj["header"] = str(con.info())
			con.close()

			self.common.log("Result: %s " % repr(ret_obj), 5)
			# Return result if it isn't age restricted
			if (ret_obj["content"].find("verify-actions") == -1 and ret_obj["content"].find("verify-age-actions") == -1):
				self.common.log("done")
				ret_obj["status"] = 200
				return ret_obj
			else:
				self.common.log("found verify age request: " + repr(params))
				# We need login to verify age
				if not get("login"):
					params["error"] = get("error", "0")
					params["login"] = "true"
					return self._fetchPage(params)
				else:
					ret_obj["status"] = 303
					ret_obj["content"] = self.language(30606)
					return ret_obj
					#return self._verifyAge(ret_obj["content"], ret_obj["new_url"], params)
		
		except urllib2.HTTPError, e:
			cont = False
			err = str(e)
			self.common.log("HTTPError : " + err)

			if err.find("Token invalid") > -1:
				self.common.log("refreshing token")
				self._oRefreshToken()
			else:
				if e.fp:
					cont = e.fp.read()
				self.common.log("HTTPError - Headers: " + str(e.headers) + " - Content: " + cont)

			params["error"] = str(int(get("error", "0")) + 1)
			ret_obj = self._fetchPage(params)

			if cont and ret_obj["content"] == "":
				ret_obj["content"] = cont
				ret_obj["status"] = 303

			return ret_obj

		except urllib2.URLError, e:
			err = str(e)
			self.common.log("URLError : " + err)
			
			time.sleep(3)
			params["error"] = str(int(get("error", "0")) + 1)
			ret_obj = self._fetchPage(params)
			return ret_obj
		
	def _findErrors(self, ret):
		self.common.log("")

		## Couldn't find 2 factor or normal login
		error = self.common.parseDOM(ret['content'], "div", attrs={ "class": "errormsg" })
		if len(error) == 0:   
		# An error in 2-factor
			error = self.common.parseDOM(ret['content'], "div", attrs={ "class": "error smaller"})
		if len(error) == 0:
			error = self.common.parseDOM(ret['content'], "div", attrs={ "id": "unavailable-message"})
		if len(error) == 0 and ret['content'].find("yt:quota") > -1:
			# Api quota
			html = self.common.parseDOM(ret['content'], "error")
			error = self.common.parseDOM(html, "code")
		if len(error) > 0:
			error = error[0]
			error = urllib.unquote(error[0:error.find("[")]).replace("&#39;", "'")
			self.common.log("returning error :" + error.strip())
			return error.strip()

		self.common.log("couldn't find any errors: " + repr(ret))
		return False

	def _verifyAge(self, result, new_url, params={}):
		get = params.get
		login_info = self.login._httpLogin({ "new": "true" })
		confirmed = "0"
		if self.settings.getSetting("safe_search") != "2":
			confirmed = "1"
		
		# Convert to fetchpage
		request = urllib2.Request(new_url)
		request.add_header('User-Agent', self.common.USERAGENT)
		request.add_header('Cookie', 'LOGIN_INFO=' + login_info)
		con = urllib2.urlopen(request)
		result = con.read()
		
		# Fallback for missing confirm form.
		if result.find("confirm-age-form") == -1:
			self.common.log("Failed trying to verify-age could find confirm age form.")
			self.common.log("html page given: " + repr(result))
			return (self.language(30606) , 303)
						
		# get next_url
		next_url_start = result.find('"next_url" value="') + len('"next_url" value="')
		next_url_stop = result.find('">', next_url_start)
		next_url = result[next_url_start:next_url_stop]
		
		self.common.log("next_url=" + next_url)
		
		# get session token to get around the cross site scripting prevetion
		session_token_start = result.find("'XSRF_TOKEN': '") + len("'XSRF_TOKEN': '")
		session_token_stop = result.find("',", session_token_start) 
		session_token = result[session_token_start:session_token_stop]
		
		self.common.log("session_token=" + session_token)
		
		# post collected information to age the verifiaction page
		request = urllib2.Request(new_url)
		request.add_header('User-Agent', self.common.USERAGENT)
		request.add_header('Cookie', 'LOGIN_INFO=' + login_info)
		request.add_header("Content-Type", "application/x-www-form-urlencoded")
		values = urllib.urlencode({ "next_url": next_url, "action_confirm": confirmed, "session_token":session_token })
		
		self.common.log("post page content: " + values)
		
		con = urllib2.urlopen(request, values)
		new_url = con.geturl()
		result = con.read()
		con.close()
		
		#If verification is success full new url must look like: 'http://www.youtube.com/index?has_verified=1'
		if new_url.find("has_verified=1"):
			params["error"] = str(int(get("error", "0")) + 1)
			params["login"] = "true"
			return self._fetchPage(params)
		
		# If verification failed we dump a shit load of info to the logs
		self.common.log("result url: " + repr(new_url))
		
		self.common.log("age verification failed with result: " + repr(result))
		return (self.language(30606), 303)

	def _oRefreshToken(self):
		# Refresh token
		if self.settings.getSetting("oauth2_refresh_token"):
			url = "https://accounts.google.com/o/oauth2/token"
			data = { "client_id": "208795275779.apps.googleusercontent.com",
				"client_secret": "sZn1pllhAfyonULAWfoGKCfp",
				"refresh_token": self.settings.getSetting("oauth2_refresh_token"),
				"grant_type": "refresh_token"}
			self.settings.setSetting("oauth2_access_token", "")
			ret = self._fetchPage({ "link": url, "no-language-cookie": "true", "url_data": data})
			if ret["status"] == 200:
				oauth = ""
				try:
					oauth = json.loads(ret["content"])
				except:
					self.common.log(repr(ret))
					return False
			
				self.common.log("- returning, got result a: " + repr(oauth))
			
				self.settings.setSetting("oauth2_access_token", oauth["access_token"])
				return True

			return False

		self.common.log("didn't even try")

		return False

	def _getAuth(self):
		self.common.log("")
		
		if float(self.settings.getSetting("oauth2_expires_at")) < time.time():
			self._oRefreshToken()

		auth = self.settings.getSetting("oauth2_access_token")

		if (auth):
			self.common.log("returning stored auth")
			return auth
		else:
			if isinstance(self.login, str):
				(result, status) = self.login.login()
			else:
				import YouTubeLogin as temp_YTLogin
				temp_login = temp_YTLogin.YouTubeLogin()
				(result, status) = temp_login._httpLogin()

			if status == 200:
				self.common.log("returning new auth")
				return self.settings.getSetting("oauth2_access_token")
			
		self.common.log("failed because login failed")
		
		return False
	
	def _getNodeAttribute(self, node, tag, attribute, default=""):
		if node.getElementsByTagName(tag).item(0):
			if node.getElementsByTagName(tag).item(0).hasAttribute(attribute):
				return node.getElementsByTagName(tag).item(0).getAttribute(attribute)

		return default;
	
	def _getNodeValue(self, node, tag, default=""):
		if node.getElementsByTagName(tag).item(0):
			if node.getElementsByTagName(tag).item(0).firstChild:
				return node.getElementsByTagName(tag).item(0).firstChild.nodeValue
		
		return default;
	
	def getVideoInfo(self, xml, params={}):
		get = params.get
		dom = minidom.parseString(xml);
		self.common.log(str(len(xml)))
		links = dom.getElementsByTagName("link");
		entries = dom.getElementsByTagName("entry");
		if (not entries):
			entries = dom.getElementsByTagName("atom:entry");
		next = False

		# find out if there are more pages
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = True
					break

		ytobjects = [];
		for node in entries:
			video = {};

			video['videoid'] = self._getNodeValue(node, "yt:videoid", "false")
			if video['videoid'] == "false":
				video['videoid'] = self._getNodeAttribute(node, "content", "src", "false")
				video['videoid'] = video['videoid'][video['videoid'].rfind("/") + 1:]

			if video['videoid'] == "false" and node.getElementsByTagName("link").item(0):
				video['videolink'] = node.getElementsByTagName("link").item(0).getAttribute('href')
				match = re.match('.*?v=(.*)\&.*', video['videolink'])
				if match:
					video['videoid'] = match.group(1)

			if node.getElementsByTagName("id"):
				entryid = self._getNodeValue(node, "id", "")
				entryid = entryid[entryid.rfind(":") + 1:]
				video["playlist_entry_id"] = entryid

			if node.getElementsByTagName("yt:state").item(0):			
				state = self._getNodeAttribute(node, "yt:state", 'name', 'Unknown Name')

				# Ignore unplayable items.
				if (state == 'deleted' or state == 'rejected'):
					video['videoid'] = "false"
								
				# Get reason for why we can't playback the file.		
				if node.getElementsByTagName("yt:state").item(0).hasAttribute('reasonCode'):
					reason = self._getNodeAttribute(node, "yt:state", 'reasonCode', 'Unknown reasonCode')
					value = self._getNodeValue(node, "yt:state", "Unknown reasonValue").encode('utf-8')
					if reason == "private":
						video['videoid'] = "false"
					elif reason == 'requesterRegion':
						video['videoid'] = "false"
					elif reason != 'limitedSyndication':
						self.common.log("removing video, reason: %s value: %s" % (reason, value))
						video['videoid'] = "false";
									
			video['Title'] = self._getNodeValue(node, "media:title", "Unknown Title").encode('utf-8') # Convert from utf-16 to combat breakage
			video['Plot'] = self._getNodeValue(node, "media:description", "Unknown Plot").encode("utf-8")
			video['Date'] = self._getNodeValue(node, "published", "Unknown Date").encode("utf-8")
			video['user'] = self._getNodeValue(node, "name", "Unknown Name").encode("utf-8")
			
			# media:credit is not set for favorites, playlists
			video['Studio'] = self._getNodeValue(node, "media:credit", "").encode("utf-8")
			if video['Studio'] == "":
				video['Studio'] = self._getNodeValue(node, "name", "Unknown Uploader").encode("utf-8")
			
			duration = int(self._getNodeAttribute(node, "yt:duration", 'seconds', '0'))
			video['Duration'] = "%02d:%02d" % (duration / 60, duration % 60)
			video['Rating'] = float(self._getNodeAttribute(node, "gd:rating", 'average', "0.0"))
			video['count'] = int(self._getNodeAttribute(node, "yt:statistics", 'viewCount', "0"))
			infoString = ""
			if video['Date'] != "Unknown Date":
				c = time.strptime(video['Date'][:video['Date'].find(".000Z")], "%Y-%m-%dT%H:%M:%S")
				video['Date'] = time.strftime("%d-%m-%Y", c)
				infoString += "Date Uploaded: " + time.strftime("%Y-%m-%d %H:%M:%S", c) + ", "
			infoString += "View count: " + str(video['count'])
			video['Plot'] = infoString + "\n" + video['Plot']
			video['Genre'] = self._getNodeAttribute(node, "media:category", "label", "Unknown Genre").encode("utf-8")

			edit_links = node.getElementsByTagName("link")
			if edit_links:
				for edit_link in edit_links:
					if edit_link.getAttribute('rel') == 'edit':
						obj = edit_link.getAttribute('href')
						video['editid'] = obj[obj.rfind('/') + 1:]

			video['thumbnail'] = self.urls["thumbnail"] % video['videoid']
			
			overlay = self.storage.retrieveValue("vidstatus-" + video['videoid'])
			if overlay:
				video['Overlay'] = int(overlay)
			
			if video['videoid'] == "false":
				self.common.log("videoid set to false : " + repr(video))

			ytobjects.append(video);
		if next:
			self.utils.addNextFolder(ytobjects, params)
				
		self.common.log("Done: " + str(len(ytobjects)))
		save_data = {}
		for item in ytobjects:
			if item.has_key("videoid"):
				save_data[item["videoid"]] = repr(item)
		self.cache.sqlSetMulti("videoidcache", save_data)
		return ytobjects;

