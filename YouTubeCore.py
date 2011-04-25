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

import sys, urllib, urllib2, re
from xml.dom.minidom import parseString

# ERRORCODES:
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class url2request(urllib2.Request):
	"""Workaround for using DELETE with urllib2"""
	def __init__(self, url, method, data=None, headers={},origin_req_host=None, unverifiable=False):
		self._method = method
		urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)

	def get_method(self):
		if self._method:
			return self._method
		else:
			return urllib2.Request.get_method(self) 

class YouTubeCore(object):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__storage__ = sys.modules[ "__main__" ].__storage__
	__utils__ = sys.modules[ "__main__" ].__utils__
	__login__ = sys.modules[ "__main__" ].__login__

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
	# YouTube General Feeds
	urls['playlist'] = "http://gdata.youtube.com/feeds/api/playlists/%s"
	urls['related'] = "http://gdata.youtube.com/feeds/api/videos/%s/related"
	urls['search'] = "http://gdata.youtube.com/feeds/api/videos?q=%s&safeSearch=%s"
	
	# YouTube User specific Feeds
	urls['uploads'] = "http://gdata.youtube.com/feeds/api/users/%s/uploads"
	urls['favorites'] = "http://gdata.youtube.com/feeds/api/users/%s/favorites"
	urls['playlists'] = "http://gdata.youtube.com/feeds/api/users/%s/playlists"
	urls['contacts'] = "http://gdata.youtube.com/feeds/api/users/default/contacts"
	urls['subscriptions'] = "http://gdata.youtube.com/feeds/api/users/%s/subscriptions"
	urls['newsubscriptions'] = "http://gdata.youtube.com/feeds/api/users/%s/newsubscriptionvideos"
	
	# YouTube Standard feeds
	urls['feed_rated'] = "http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?time=%s"
	urls['feed_favorites'] = "http://gdata.youtube.com/feeds/api/standardfeeds/top_favorites?time=%s"
	urls['feed_viewed'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?time=%s"
	urls['feed_linked'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_popular?time=%s" 
	urls['feed_discussed'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_discussed?time=%s"
	urls['feed_responded'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_responded?time=%s"
	
	# Wont work with time parameter
	urls['feed_recent'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_recent" 
	urls['feed_featured'] = "http://gdata.youtube.com/feeds/api/standardfeeds/recently_featured"
	urls['feed_trending'] = "http://gdata.youtube.com/feeds/api/standardfeeds/on_the_web"
	urls['feed_shared'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_shared"	
		
	def createUrl(self, params = {}):
		get = params.get
		time = ( "all_time", "today", "this_week", "this_month") [ int(self.__settings__.getSetting( "feed_time" ) ) ]
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		region = ('', 'AU', 'BR', 'CA', 'CZ', 'FR', 'DE', 'GB', 'NL', 'HK', 'IN', 'IE', 'IL', 'IT', 'JP', 'MX', 'NZ', 'PL', 'RU', 'KR', 'ES','SE', 'TW', 'US', 'ZA' )[ int( self.__settings__.getSetting( "region_id" ) ) ]
		
		page = get("page","0")
		start_index = per_page * int(page) + 1
		url = ""
		
		if (get("feed")):
			url = self.urls[get("feed")]
			
			if get("search"):
				query = urllib.unquote_plus(get("search"))
				safe_search = ("none", "moderate", "strict" ) [int( self.__settings__.getSetting( "safe_search" ) ) ]	
				url = url % (query, safe_search)  
				authors = self.__settings__.getSetting("stored_searches_author")
				if len(authors) > 0:
					try:
						authors = eval(authors)
						if query in authors:
							url += "&" + urllib.urlencode({'author': authors[query]})
					except:
						print self.__plugin__ + " search - eval failed "	
			
			if (url.find("time") > 0 ):
				url = url % time
				
			if ( url.find("?") == -1 ):
				url += "?"
			else:
				url += "&"
			
			url += "start-index=" + repr(start_index) + "&max-results=" + repr(per_page)
			
			if (url.find("standardfeeds") > 0 and region):
				url = url.replace("/standardfeeds/", "/standardfeeds/"+ region + "/")
		
		if (get("user_feed")):
			url = self.urls[get("user_feed")]
			
			if (url.find("%s") > 0):
				if ( get("contact") and not (get("external") and get("channel"))):
					url = url % get("contact")
				elif ( get("videoid")):
					url = url % get("videoid")
				elif ( get("channel")):
					url = url % get("channel")
				elif ( get("playlist")):
					url = url % get("playlist")
				elif ( get("feed") == "uploads" or get("feed") == "favorites" or  get("feed") == "playlists" or get("feed") == "subscriptions" or get("feed") == "newsubscriptions"):
					url = url % self.__settings__.getSetting( "nick" )
				else: 
					url = url % "default"
			
			if ( url.find("?") == -1 ):
				url += "?"
			else:
				url += "&"
			
			url += "start-index=" + repr(start_index) + "&max-results=" + repr(per_page)
			
			if get("feed") == "playlists" or get("feed") == "subscriptions":
				url += "&orderby=published"
		
		url = url.replace(" ", "+")
		return url
	
	def list(self, params = {}):
		get = params.get
		result = []
		status = 303
				
		if get("store"): 
			if get("store") == "contact_options":
				return self.__storage__.getUserOptionFolder(params)
			else:
				return self.__storage__.getStoredSearches(params)

		if get("login") == "true":
			if ( not self._getAuth() ):
				if self.__dbg__:
					print self.__plugin__ + " login required but auth wasn't set!"
				return ( self.__language__(30609) , 303 )

		url = self.createUrl(params)
		
		if url:
			( response, status ) = self._fetchPage({"link": url, "auth": get("login"), "api": "true"})
		
		if status != 200:
			return ( result, status )
		
		if get("folder"):
			result = self.getFolderInfo(response, params)
		else:
			result = self.getVideoInfo(response, params)
		
		if len(result) == 0:
			return (result, 303)
		
		if (get("search")):
			thumbnail = result[0].get('thumbnail', "")
			
			if (thumbnail):
				self.__settings__.setSetting("search_" + urllib.unquote_plus(get("search")) + "_thumb", thumbnail)
			
		return (result, 200)
	
	def delete_favorite(self, params = {}):
		get = params.get
		delete_url = self.urls["favorites"] % self.__settings__.getSetting( "nick" )
		delete_url += "/" + get('editid') 
		return self._fetchPage({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})
	
	def remove_contact(self, params = {}):
		get = params.get
		delete_url = self.urls["contacts"] 
		delete_url += "/" + get("contact")
		return self._fetchPage({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

	def remove_subscription(self, params = {}):
		get = params.get
		delete_url = self.urls["subscriptions"] % self.__settings__.getSetting( "nick" )
		delete_url += "/" + get("editid")
		return self._fetchPage({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

	def add_contact(self, params = {}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/contacts"
		add_request = '<?xml version="1.0" encoding="UTF-8"?> <entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><yt:username>%s</yt:username></entry>' % get("contact")
		return self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		
	def add_favorite(self, params = {}):
		get = params.get 
		url = "http://gdata.youtube.com/feeds/api/users/default/favorites"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom"><id>%s</id></entry>' % get("videoid")
		return self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true", "request": add_request})
		
	def add_subscription(self, params = {}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"> <category scheme="http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat" term="user"/><yt:username>%s</yt:username></entry>' % get("channel")
		return self._fetchPage({"link": url, "api": "true", "login": "true", "auth": "true","request": add_request})
		
	def getFolderInfo(self, xml, params = {}):
		get = params.get
		result = ""
		
		dom = parseString(xml);
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
			folder['Title'] = node.getElementsByTagName("title").item(0).firstChild.nodeValue.replace('Activity of : ', '').replace('Videos published by : ', '').encode( "utf-8" );
			folder['published'] = self._getNodeValue(node, "published", "2008-07-05T19:56:35.000-07:00")
			folder['playlist'] = self._getNodeValue(node, 'yt:playlistId', '')
			
			if get("user_feed") == "contacts":
				folder["thumbnail"] = "user"
				folder["contact"] = folder["Title"]
				folder["store"] = "contact_options"
				folder["folder"] = "true"

			if get("user_feed") == "subscriptions":
				folder["channel"] = folder["Title"]
				if (self.__settings__.getSetting(get("user_feed") + "_" + folder["channel"] + "_thumb")):
					folder["thumbnail"] = self.__settings__.getSetting(get("user_feed") + "_" + folder["channel"] + "_thumb")
					
				viewmode = ""
				if (get("external")):
					viewmode += "external_" + get("contact") + "_"
					folder["external"] = "true"
					folder["contact"] = get("contact")
				viewmode += "view_mode_" + folder["Title"]
				
				if (self.__settings__.getSetting(viewmode) == "subscriptions_favorites"):
					folder["user_feed"] = "favorites"
					folder["view_mode"] = "subscriptions_uploads"
				elif(self.__settings__.getSetting(viewmode) == "subscriptions_playlists"):
					folder["user_feed"] = "playlists"
					folder["view_mode"] = "subscriptions_playlists"
				else:
					folder["user_feed"] = "uploads"  
					folder["view_mode"] = "subscriptions_favorites"
			
			if get("user_feed") == "playlists":
				folder["user_feed"] = "playlist"
				if (self.__settings__.getSetting(get("user_feed") + "_" + folder["playlist"] + "_thumb")):
					folder["thumbnail"] = self.__settings__.getSetting(get("user_feed") + "_" + folder["playlist"] + "_thumb")
				
			if node.getElementsByTagName("link"):
				link = node.getElementsByTagName("link")
				for i in range(len(link)):
					if link.item(i).getAttribute('rel') == 'edit':
						obj = link.item(i).getAttribute('href')
						folder['editid'] = obj[obj.rfind('/')+1:]
			
			folders.append(folder);
		
		if (get("user_feed")):
			print "Sorting " 
			folders.sort(key=lambda item:item["Title"].lower(), reverse=False)
			
		if next:
			item = {"Title":self.__language__( 30509 ), "thumbnail":"next", "next":"true", "page":str(int(get("page", "0")) + 1)} 
			for k, v in params.items():
				if (k != "thumbnail" and k != "Title" and k != "page"):
					item[k] = v
			folders.append(item)
		
		return folders;

	def getBatchDetailsThumbnails(self, items, params = {}):
		ytobjects = []
		videoids = []
		
		for (videoid, thumb) in items:
			videoids.append(videoid)
		
		(tempobjects, status) = self.getBatchDetails(videoids, params = {})
		
		for i in range(0, len(items)):
			( videoid, thumbnail ) = items[i]
			for item in tempobjects:
				if item['videoid'] == videoid:
					item['thumbnail'] = thumbnail
					ytobjects.append(item)					

		while len(items) > len(ytobjects):
			ytobjects.append({'videoid': 'false'});
		
		return ( ytobjects, 200)
	
	def getBatchDetails(self, items, params = {}):
		request_start = "<feed xmlns='http://www.w3.org/2005/Atom'\n xmlns:media='http://search.yahoo.com/mrss/'\n xmlns:batch='http://schemas.google.com/gdata/batch'\n xmlns:yt='http://gdata.youtube.com/schemas/2007'>\n <batch:operation type='query'/> \n"
		request_end = "</feed>"
		
		video_request = ""
		
		ytobjects = []
		i = 1
		for videoid in items:
			if videoid:
				video_request +=	"<entry> \n <id>http://gdata.youtube.com/feeds/api/videos/" + videoid+ "</id>\n</entry> \n"
				if i == 50:
					final_request = request_start + video_request + request_end
					request = urllib2.Request("http://gdata.youtube.com/feeds/api/videos/batch")
					request.add_data(final_request)
					con = urllib2.urlopen(request)
					result = con.read()
					(temp, status) = self.getVideoInfoBatch(result, params)
					ytobjects += temp
					if status != 200:
						return (ytobjects, status)
					video_request = ""
					i = 1
				i+=1
		
		final_request = request_start + video_request + request_end
		request = urllib2.Request("http://gdata.youtube.com/feeds/api/videos/batch")
		request.add_data(final_request)
		con = urllib2.urlopen(request)
		result = con.read()
				
		(temp, status) = self.getVideoInfoBatch(result, params)
		ytobjects += temp
				
		return ( ytobjects, 200)
		
	#===============================================================================
	#
	# Internal functions to YouTubeCore.py
	#
	# Return should be value(True for bool functions), or False if failed.
	#
	# False MUST be handled properly in External functions
	#
	#===============================================================================

	def _fetchPage(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " fetching page : " + repr(params)
		
		if not get("link") or int(get("error", "0")) > 3 :
			if self.__dbg__:
				print self.__plugin__ + " fetching page giving up "
			return ( "", 500 )

		if get("request", "false") == "false":
			request = url2request(get("link"), get("method", "GET"));
		else:
			if self.__dbg__:
				print self.__plugin__ + " got request"
			request = urllib2.Request(get("link"), get("request"))
			request.add_header('X-GData-Client', "")
			request.add_header('Content-Type', 'application/atom+xml')
			request.add_header('Content-Length', str(len(get("request"))))

		if get("api", "false") == "true":
			request.add_header('GData-Version', '2')
			request.add_header('X-GData-Key', 'key=' + self.APIKEY)
		else:
			request.add_header('User-Agent', self.__utils__.USERAGENT)
		
		if get("login", "false") == "true":
			if ( self.__settings__.getSetting( "username" ) == "" or self.__settings__.getSetting( "user_password" ) == "" ):
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage, login required but no credentials provided"
				return ( self.__language__( 30608 ) , 303 )
			
			request.add_header('Cookie', 'LOGIN_INFO=' + self.__login__._httpLogin() )
		
		if get("auth", "false") == "true":
			if self._getAuth():
				request.add_header('Authorization', 'GoogleLogin auth=' + self.__settings__.getSetting("auth"))
			else:
				print self.__plugin__ + " _fetchPage couldn't get login token"
		
		try:
			con = urllib2.urlopen(request)
			result = con.read()
			new_url = con.geturl()
			con.close()

			# Return result if it isn't age restricted
			if ( result.find("verify-age-actions") == -1):
				return ( result, 200 )
			
			else:
				# We need login to verify age
				if not get("login"):
					params["error"] = get("error", "0")
					params["login"] = "true"
					return self._fetchPage(params)

				if self.__dbg__:
					print self.__plugin__ + " _fetchPage Video age restricted, trying to verify for url: " + new_url + " saf_search " + self.__settings__.getSetting( "safe_search" )

				if self.__settings__.getSetting( "safe_search" ) != "2" :
					confirmed = 1
				else:
					confirmed = 0
				
				# Fallback for missing confirm form.
				if result.find("confirm-age-form") == -1:
					if self.__dbg__:
						print self.__plugin__ + " _fetchPage: Sorry - you must be 18 or over to view this video or group"
					return ( self.__language__( 30608 ) , 303 )
								
				request = urllib2.Request(new_url)
				request.add_header('User-Agent', self.__utils__.USERAGENT)
				request.add_header('Cookie', 'LOGIN_INFO=' + self.__login__._httpLogin(True) )

				# This really should be a regex, but the regex kept failing.
				temp = result[result.find("verify-age-actions"):(result.find("verify-age-actions") + 600)]
				next_url = temp[( temp.find('"next_url" value="') + len('"next_url" value="')):]
				next_url = next_url[:next_url.find('"')] 

				values = { "next_url": next_url, "action_confirm": confirmed }
				
				con = urllib2.urlopen(request, urllib.urlencode(values))
				
				result = con.read()
				if get("get_redirect"):	
					result = con.geturl()
				con.close()
				
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage. Age should now be verified, calling _fetchPage again"
					
				params["error"] = str(int(get("error", "0")) + 1)
				params["login"] = "true"
				return self._fetchPage(params)
		
		except urllib2.HTTPError, e:
			err = str(e)
			if self.__dbg__:
				print self.__plugin__ + " _fetchPage HTTPError : " + err


			if ( err.find("201") > -1):
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage request: Done"
				return ( "", 200)
			
			else:
				if int(get("error", "0")) < 2:
					if self.__dbg__:
						print self.__plugin__ + " _fetchPage retry: " + err

					if ( self.__settings__.getSetting( "username" ) != "" and self.__settings__.getSetting( "user_password" ) != "" ):
						params["login"] = "true"
						self.__login__.login();

					params["error"] = str(int(get("error", "0")) + 1)
					return self._fetchPage(params)
				else:
					if ( err.find("401") > -1 ):
						if self.__dbg__:
							print self.__plugin__ + " _fetchPage 401 Not Authorized and no login credentials written in settings"
							return ( self.__language__(30622), 303)
					else:
						if self.__dbg__:
							print self.__plugin__ + " _fetchPage got empty results back"
						return (self.__language__(30601), 303)
							
		except:
			if self.__dbg__:
				print self.__plugin__ + ' _fetchPage ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
												 , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				
			return ( "", 500 )
		
	def _getAuth(self):
		if self.__dbg__:
			print self.__plugin__ + " _getAuth"

		auth = self.__settings__.getSetting( "auth" )

		if ( not auth ):
			(result, status ) =  self.__login__.login()
			if status != 200:
				if self.__dbg__:
					print self.__plugin__ + " _getAuth failed because login failed"
				return False
		return True
	
	
	def _getNodeAttribute(self, node, tag, attribute, default = ""):
		if node.getElementsByTagName(tag).item(0):
			if node.getElementsByTagName(tag).item(0).hasAttribute(attribute):
				return node.getElementsByTagName(tag).item(0).getAttribute(attribute)

		return default;
	
	def _getNodeValue(self, node, tag, default = ""):
		if node.getElementsByTagName(tag).item(0):
			if node.getElementsByTagName(tag).item(0).firstChild:
				return node.getElementsByTagName(tag).item(0).firstChild.nodeValue
		
		return default;

	def getVideoInfoBatch(self, xml, params = {}):
		get = params.get
		dom = parseString(xml);
		entries = dom.getElementsByTagName("atom:entry");
				
		ytobjects = [];
		for node in entries:
			video = {};
			videoid = self._getNodeValue(node, "atom:id", "")
			
			if (not videoid):
				if node.getElementsByTagName("link").item(0):
					videoid = node.getElementsByTagName("link").item(0).getAttribute('href')
					match = re.match('.*?v=(.*)\&.*', videoid)
					if match:
						videoid = match.group(1)
			
			if (videoid):
				if (videoid.rfind("/") != -1):
					video['videoid'] = videoid[videoid.rfind("/") + 1:]
					
				if node.getElementsByTagName("yt:state").item(0):
					state = self._getNodeAttribute(node, "yt:state", 'name', 'Unknown Name')
	
					if ( state == 'deleted' or state == 'rejected'):
						video['videoid'] = "false"
						
					# Get reason for why we can't playback the file.		
					if node.getElementsByTagName("yt:state").item(0).hasAttribute('reasonCode'):
						reason = self._getNodeAttribute(node, "yt:state", 'reasonCode', 'Unknown reasonCode')
						if reason == "private" or reason == 'requesterRegion':
							video['videoid'] = "false"
						elif reason != 'limitedSyndication':
							video['videoid'] = "false";
				
				video['Title'] = self._getNodeValue(node, "media:title", "Unknown Title").encode('utf-8')
				video['Plot'] = self._getNodeValue(node, "media:description", "Unknown Plot").encode( "utf-8" )
				video['Date'] = self._getNodeValue(node, "atom:published", "Unknown Date").encode( "utf-8" )
				video['user'] = self._getNodeValue(node, "atom:name", "Unknown Name").encode( "utf-8" )
				
				# media:credit is not set for favorites, playlists or inbox
				video['Studio'] = self._getNodeValue(node, "media:credit", "").encode( "utf-8" )
				if video['Studio'] == "":
					video['Studio'] = self._getNodeValue(node, "atom:name", "Unknown Uploader").encode( "utf-8" )
					
				duration = int(self._getNodeAttribute(node, "yt:duration", 'seconds', '0'))
				video['Duration'] = "%02d:%02d" % ( duration / 60, duration % 60 )
				video['Rating'] = float(self._getNodeAttribute(node,"gd:rating", 'average', "0.0"))
				video['count'] = int(self._getNodeAttribute(node, "yt:statistics", 'viewCount', "0"))
				video['Genre'] = self._getNodeAttribute(node, "media:category", "label", "Unknown Genre").encode( "utf-8" )
				infoString =""
				if video['Date'] != "Unknown Date":
					infoString += "Date Uploaded: " + video['Date'][:video['Date'].find("T")] + ", "				
				infoString += "View count: " + str(video['count'])
				
				if node.getElementsByTagName("atom:link"):
					link = node.getElementsByTagName("atom:link")
					for i in range(len(link)):
						if link.item(i).getAttribute('rel') == 'edit':
							obj = link.item(i).getAttribute('href')
							video['editid'] = obj[obj.rfind('/')+1:]
				
				video['thumbnail'] = "http://i.ytimg.com/vi/" + video['videoid'] + "/0.jpg"
				
				overlay = self.__settings__.getSetting( "vidstatus-" + video['videoid'] )
				if overlay:
					video['Overlay'] = int(overlay)
				
				ytobjects.append(video);
							
		if (ytobjects):
			return (ytobjects, 200);
		
		return ( "", 500 )
	
	def getVideoInfo(self, xml, params):
		get = params.get
		dom = parseString(xml);
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

			video['videoid'] = self._getNodeValue(node, "yt:videoid", "missing")
			
			if node.getElementsByTagName("yt:state").item(0):			
				state = self._getNodeAttribute(node, "yt:state", 'name', 'Unknown Name')

				# Ignore unplayable items.
				if ( state == 'deleted' or state == 'rejected'):
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
						if self.__dbg__:
							print self.__plugin__ + " _getvideoinfo removing video, reason: %s value: %s" % ( reason, value)
						video['videoid'] = "false";
						
			if ( video['videoid'] == "missing" ):
				video['videolink'] = node.getElementsByTagName("link").item(0).getAttribute('href')
				match = re.match('.*?v=(.*)\&.*', video['videolink'])
				if match:
					video['videoid'] = match.group(1)
				else:
					video['videoid'] = "false"
			
			video['Title'] = self._getNodeValue(node, "media:title", "Unknown Title").encode('utf-8') # Convert from utf-16 to combat breakage
			video['Plot'] = self._getNodeValue(node, "media:description", "Unknown Plot").encode( "utf-8" )
			video['Date'] = self._getNodeValue(node, "published", "Unknown Date").encode( "utf-8" )
			video['user'] = self._getNodeValue(node, "name", "Unknown Name").encode( "utf-8" )
			
			# media:credit is not set for favorites, playlists
			video['Studio'] = self._getNodeValue(node, "media:credit", "").encode( "utf-8" )
			if video['Studio'] == "":
				video['Studio'] = self._getNodeValue(node, "name", "Unknown Uploader").encode( "utf-8" )
			
			duration = int(self._getNodeAttribute(node, "yt:duration", 'seconds', '0'))
			video['Duration'] = "%02d:%02d" % ( duration / 60, duration % 60 )
			video['Rating'] = float(self._getNodeAttribute(node,"gd:rating", 'average', "0.0"))
			video['count'] = int(self._getNodeAttribute(node, "yt:statistics", 'viewCount', "0"))
			infoString =""
			if video['Date'] != "Unknown Date":
				infoString += "Date Uploaded: " + video['Date'][:video['Date'].find("T")] + ", "				
			infoString += "View count: " + str(video['count'])
			video['Plot'] = infoString + "\n" + video['Plot']
			video['Genre'] = self._getNodeAttribute(node, "media:category", "label", "Unknown Genre").encode( "utf-8" )

			if node.getElementsByTagName("link"):
				link = node.getElementsByTagName("link")
				for i in range(len(link)):
					if link.item(i).getAttribute('rel') == 'edit':
						obj = link.item(i).getAttribute('href')
						video['editid'] = obj[obj.rfind('/')+1:]

			video['thumbnail'] = "http://i.ytimg.com/vi/" + video['videoid'] + "/0.jpg"
		
			overlay = self.__settings__.getSetting( "vidstatus-" + video['videoid'] )

			if overlay:
				video['Overlay'] = int(overlay)
			
			if video['videoid'] == "false":
				if self.__dbg__:
					print self.__plugin__ + " _getvideoinfo videoid set to false"
						
			ytobjects.append(video);
		
		if next:
			item = {"Title":self.__language__( 30509 ), "thumbnail":"next", "next":"true", "page":str(int(get("page", "0")) + 1)} 
			for k, v in params.items():
				if (k != "thumbnail" and k != "Title" and k != "page"):
					item[k] = v
			ytobjects.append(item)
		
		return ytobjects;
