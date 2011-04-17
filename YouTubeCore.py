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

import sys, urllib, urllib2, re, string, os.path
from xml.dom.minidom import parseString

# ERRORCODES:
# 0 = Ignore
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class YouTubeCore(object):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	__dbgv__ = False
	
	APIKEY = "AI39si6hWF7uOkKh4B9OEAX-gK337xbwR9Vax-cdeF9CF9iNAcQftT8NVhEXaORRLHAmHxj6GjM-Prw04odK4FxACFfKkiH9lg";
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
	VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
	#===============================================================================
	#
	# External functions called by YouTubeNavigation.py
	#
	# return MUST be a tupple of ( result[string or dict], status[int] )
	# 
	#===============================================================================
	
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
	urls['list_playlist'] = "http://gdata.youtube.com/feeds/api/playlists/%s"
	urls['list_related'] = "http://gdata.youtube.com/feeds/api/videos/%s/related"
	urls['search'] = "http://gdata.youtube.com/feeds/api/videos?q=%s&safeSearch=%s&start-index=%s&max-results=%s"
	
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
	
	def __init__(self):
		timeout = self.__settings__.getSetting( "timeout" )
		if not timeout:
			timeout = "5"
		return None
		
	def interrogate(self, item):
		"""Print useful information about item."""
		if hasattr(item, '__name__'):
			print "NAME:    ", item.__name__
		if hasattr(item, '__class__'):
			print "CLASS:   ", item.__class__.__name__
		print "ID:      ", id(item)
		print "TYPE:    ", type(item)
		print "VALUE:   ", repr(item)
		print "CALLABLE:",
		if callable(item):
			print "Yes"
		else:
			print "No"
		
		if hasattr(item, '__doc__'):
			doc = getattr(item, '__doc__')
			if doc:
				doc = doc.strip()
				firstline = doc.split('\n')[0]
				print "DOC:     ", firstline		
	
	def createUrl(self, params = {}):
		get = params.get
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		page = get("page","0")
		start_index = per_page * int(page) + 1
		
		if (get("action") == "search"): 
			query = urllib.unquote_plus(get("query"))
			safe_search = ("none", "moderate", "strict" ) [int( self.__settings__.getSetting( "safe_search" ) ) ]	
			url = self.urls["search"] % ( query, safe_search, start_index, per_page)
			authors = self.__settings__.getSetting("stored_searches_author")
			if len(authors) > 0:
				try:
					authors = eval(authors)
					if query in authors:
						url += "&" + urllib.urlencode({'author': authors[query]})
				except:
					print self.__plugin__ + " search - eval failed "
			return url
		
		if (get("feed")):
			url = self.urls[get("feed")]
			
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
			return url
		
	def search(self, params = {}):
		get = params.get
		url = self.createUrl(params)
		
		( result, status ) = self._fetchPage(url, api = True)

		if status != 200:
			return ( result, status )

		result = self._getvideoinfo(result)
		
		if len(result) > 0:
			if self.__dbg__:
				print self.__plugin__ + " search done :" + str(len(result))
			return (result, 200)
		else:
			if self.__dbg__:
				print self.__plugin__ + " search done with no results"
			return (self.__language__(30601), 303)

	def feeds(self, feed, params ={} ):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " feeds : " + repr(feed) + " page: " + repr(get("page","0"))
		result = ""
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		
		if (feed.find("%s") > 0 ):
			time = ( "all_time", "today", "this_week", "this_month") [ int(self.__settings__.getSetting( "feed_time" ) ) ]
			feed = feed % time
		
		if ( feed.find("?") == -1 ):
			feed += "?"
		else:
			feed += "&"
			
		feed += "start-index=" + str( per_page * int(get("page","0")) + 1) + "&max-results=" + repr(per_page)
			
		if (feed.find("standardfeeds") > 0):
			region = ('', 'AU', 'BR', 'CA', 'CZ', 'FR', 'DE', 'GB', 'NL', 'HK', 'IN', 'IE', 'IL', 'IT', 'JP', 'MX', 'NZ', 'PL', 'RU', 'KR', 'ES','SE', 'TW', 'US', 'ZA' )[ int( self.__settings__.getSetting( "region_id" ) ) ]
			if (region):
				feed = feed.replace("/standardfeeds/", "/standardfeeds/"+ region + "/")

		( result, status ) = self._fetchPage(feed, api = True)

		if status != 200:
			return ( result, status )

		result = self._getvideoinfo(result)
					
		if len(result) > 0:
			if self.__dbg__:
				print self.__plugin__ + " feeds done : " + str(len(result))
			return ( result, 200 )
		else:
			if self.__dbg__:
				print self.__plugin__ + " feeds done with no results"
			return (self.__language__(30602), 303)
	
	def listAll(self, feed, params ={}):
		get = params.get
		result = ""
		auth = self._getAuth()
		
		if ( not auth ):
			if self.__dbg__:
				print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
				
		index = 1
		url = feed + "start-index=" + str(index) + "&max-results=" + repr(50)
		url = url.replace(" ", "+")
		
		( result, status ) = self._fetchPage(url, auth = False)
				
		ytobjects = self._getvideoinfo(result)
		
		if len(ytobjects) == 0:
			return ([], 303)
		
		next = ytobjects[len(ytobjects)-1].get("next","false") 
		
		while next == "true":
			index += 50
			url = feed + "start-index=" + str(index) + "&max-results=" + repr(50)
			url = url.replace(" ", "+")
			(result, status) = self._fetchPage(url, auth = False)
			if status != 200:
				break
			temp_objects = self._getvideoinfo(result)
			next = temp_objects[len(temp_objects)-1].get("next","false")
			ytobjects += temp_objects
				
		if len(ytobjects) > 0:
			if self.__dbg__:
				print self.__plugin__ + " list done :" + str(len(ytobjects))
			return (ytobjects, 200)
		else:
			if self.__dbg__:
				print self.__plugin__ + " list done with no results"
			return (self.__language__(30602), 303)
		
	def list(self, params ={}):
		get = params.get
		page = get("page","0")
		if self.__dbg__:
			print self.__plugin__ + " list: " + repr(feed) + " - page: " + repr(page)
		result = ""
		auth = self._getAuth()
		if ( not auth ):
			if self.__dbg__:
				print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
		
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
	
		if ( feed.find("?") == -1 ):
			feed += "?"
		else:
			feed += "&"

		feed += "start-index=" + str( per_page * int(page) + 1) + "&max-results=" + repr(per_page)
		feed = feed.replace(" ", "+")
		
		( result, status ) = self._fetchPage(feed, auth = True)

		if status != 200:
			return ( result, status)

		result = self._getvideoinfo(result)

		if len(result) > 0:
			if self.__dbg__:
				print self.__plugin__ + " list done :" + str(len(result))
			return (result, 200)
		else:
			if self.__dbg__:
				print self.__plugin__ + " list done with no results"
			return (self.__language__(30602), 303)

	def delete_favorite(self, params = {}):
		get = params.get
		delete_url = self.urls["favorites"] % self.__settings__.getSetting( "nick" )
		delete_url += "/" + get('editid') 
		return self._youTubeDel(delete_url)
	
	def remove_contact(self, params = {}):
		get = params.get
		delete_url = self.urls["contacts"] 
		delete_url += "/" + get("contact")
		return self._youTubeDel(delete_url)

	def remove_subscription(self, params = {}):
		get = params.get
		delete_url = self.urls["subscriptions"] % self.__settings__.getSetting( "nick" )
		delete_url += "/" + get("contact")
		return self._youTubeDel(delete_url)

	def add_contact(self, params = {}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/contacts"
		add_request = '<?xml version="1.0" encoding="UTF-8"?> <entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><yt:username>%s</yt:username></entry>' % get("contact")
		return self._youTubeAdd(url, add_request)
		
	def add_favorite(self, params = {}):
		get = params.get 
		url = "http://gdata.youtube.com/feeds/api/users/default/favorites"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom"><id>%s</id></entry>' % get("videoid")
		return self._youTubeAdd(url, add_request)

	def add_subscription(self, params = {}):
		get = params.get
		url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions"
		add_request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"> <category scheme="http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat" term="user"/><yt:username>%s</yt:username></entry>' % get("contact")
		return self._youTubeAdd(url, add_request)

	def playlists(self, link, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " playlists " + repr(link) + " - page: " + repr(get("page","0"))
		result = ""

		auth = self._getAuth()
		if ( not auth ):
			if self.__dbg__:
				print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
		
		per_page = ( 10, 15, 20, 25, 30, 40, 50, )[ int( self.__settings__.getSetting( "perpage" ) ) ]
		if ( link.find("?") == -1 ):
			link += "?"
		else:
			link += "&"
		link += "start-index=" + str( per_page * int(get("page","0")) + 1) + "&max-results=" + repr(per_page)
		
		if get("feed") == "playlists" or get("feed") == "subscriptions":
			link += "&orderby=published"


		( result, status ) = self._fetchPage(link, auth = True)

		if status != 200:
			return ( result, status )
		
		dom = parseString(result);
		links = dom.getElementsByTagName("link");
		entries = dom.getElementsByTagName("entry");
		next = "false"

		#find out if there are more pages
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = "true"
					break
		
		playobjects = [];
		for node in entries:
			video = {};
			video['Title'] = node.getElementsByTagName("title").item(0).firstChild.nodeValue.replace('Activity of : ', '').replace('Videos published by : ', '').encode( "utf-8" );
			
			video['published'] = self._getNodeValue(node, "published", "2008-07-05T19:56:35.000-07:00")
			video['summary'] = self._getNodeValue(node, 'summary', 'Unknown')
			video['content'] = self._getNodeAttribute(node, 'content', 'src', 'FAIL')
			video['playlistId'] = self._getNodeValue(node, 'yt:playlistId', '')
			
			if node.getElementsByTagName("link"):
				link = node.getElementsByTagName("link")
				for i in range(len(link)):
					if link.item(i).getAttribute('rel') == 'edit':
						obj = link.item(i).getAttribute('href')
						video['editid'] = obj[obj.rfind('/')+1:]
			
			playobjects.append(video);
			
		if len(playobjects) > 0:
			playobjects[len(playobjects) - 1]['next'] = next
			
		if self.__dbg__:
			print self.__plugin__ + " playlist done"
				
		return ( playobjects, 200 );

	def _get_batch_details_thumbnails(self, items):
		ytobjects = []
		videoids = []
		
		for (videoid, thumb) in items:
			videoids.append(videoid)
		
		(tempobjects, status) = self._get_batch_details(videoids)
		
		for i in range(0, len(items)):
			( videoid, thumbnail ) = items[i]
			for item in tempobjects:
				if item['videoid'] == videoid:
					item['thumbnail'] = thumbnail
					ytobjects.append(item)					

		while len(items) > len(ytobjects):
			ytobjects.append({'videoid': 'false'});
		
		return ( ytobjects, 200)
	
	def _get_batch_details(self, items):
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
					(temp, status) = self._getVideoInfoBatch(result)
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
				
		(temp, status) = self._getVideoInfoBatch(result)
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

	def _fetchPage(self, link, api = False, auth=False, login=False, error = 0):
		if self.__dbg__:
			print self.__plugin__ + " fetching page : " + link

		request = urllib2.Request(link)

		if api:
			request.add_header('GData-Version', '2')
		else:
			request.add_header('User-Agent', self.USERAGENT)

		if ( login ):
			if ( self.__settings__.getSetting( "username" ) == "" or self.__settings__.getSetting( "user_password" ) == "" ):
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage, login required but no credentials provided"
				return ( self.__language__( 30608 ) , 303 )

			if self.__dbg__:
				print self.__plugin__ +  " _fetchPage adding cookie"
			request.add_header('Cookie', 'LOGIN_INFO=' + self._httpLogin() )

		if auth:
			authkey = self._getAuth()
			if ( not authkey ):
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage couldn't set auth "
				
			request.add_header('Authorization', 'GoogleLogin auth=' + authkey)
			request.add_header('X-GData-Key', 'key=' + self.APIKEY)
		
		try:
			con = urllib2.urlopen(request)
			result = con.read()
			new_url = con.geturl()
			con.close()

			# Return result if it isn't age restricted
			if ( result.find("verify-age-actions") == -1):
				return ( result, 200 )
			
			# review this before 2.0 final
			elif ( error < 10 ):
				
				# We need login to verify age.	     
				if not login:
					if self.__dbg__:
						print self.__plugin__ + " _fetchPage age verification required, retrying with login"
					error = error + 0
					return self._fetchPage(link, api, auth, login = True, error = error)

				if self.__dbg__:
					print self.__plugin__ + " _fetchPage Video age restricted, trying to verify for url: " + new_url

				# Fallback for missing confirm form.
				if result.find("confirm-age-form") == -1:
					if self.__dbg__:
						print self.__plugin__ + " _fetchPage: Sorry - you must be 18 or over to view this video or group"
					return ( self.__language__( 30608 ) , 303 )
								
				request = urllib2.Request(new_url)
				request.add_header('User-Agent', self.USERAGENT)
				request.add_header('Cookie', 'LOGIN_INFO=' + self._httpLogin(True) )

				# This really should be a regex, but the regex kept failing.
				temp = result[result.find("verify-age-actions"):(result.find("verify-age-actions") + 600)]
				next_url = temp[( temp.find('"next_url" value="') + len('"next_url" value="')):]
				next_url = next_url[:next_url.find('"')] 
					
				if self.__settings__.getSetting( "safe_search" ) == "0":
					confirmed = 1
				else:
					confirmed = 0
			
				values = { "next_url": next_url, "action_confirm": confirmed }

				con = urllib2.urlopen(request, urllib.urlencode(values))
				result = con.read()
				con.close()
				
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage. Age should now be verified, calling _fetchPage again"
					
				return self._fetchPage(link, api, auth, login = True, error = error + 1)

			if self.__dbg__:
				print self.__plugin__ + " _fetchPage. Too many errors"
			return ( "", 500 )
		
		except urllib2.HTTPError, e:
			err = str(e)
			if self.__dbg__:
				print self.__plugin__ + " _fetchPage HTTPError : " + err

			# 400 (Bad request) - A 400 response code indicates that a request was poorly formed or contained invalid data. The API response content will explain the reason wny the API returned a 400 response code.
			if ( err.find("400") > -1 ):
				return ( err, 303 )
			# 401 (Not authorized) - A 401 response code indicates that a request did not contain an Authorization header, that the format of the Authorization header was invalid, or that the authentication token supplied in the header was invalid.
			elif ( err.find("401") > -1 ):
				# If login credentials are given, try again.
				if ( self.__settings__.getSetting( "username" ) != "" and self.__settings__.getSetting( "user_password" ) != "" ):
					if self.__dbg__:
						print self.__plugin__ + " _fetchPage trying again with login "

					self.login()
					return self._fetchPage(link, api, auth, login, error +1)
				else:
					if self.__dbg__:
						print self.__plugin__ + " _fetchPage 401 Not Authorized and no login credentials written in settings"
					return ( self.__language__(30622), 303)
			# 403 (Forbidden) - A 403 response code indicates that you have submitted a request that is not properly authenticated for the requested operation.
			# Test all cases that cause 403 before 2.0, and verify the above statement.
			elif ( err.find("403") > -1 ):
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage got empty results back "
				return (self.__language__(30601), 303)
			# 501 (Not implemented) - A 501 response code indicates that you have tried to execute an unsupported operation.
			elif ( err.find("501") > -1):
				return ( err, 303 )
			#500 (Internal error) - A 500 response code indicates that YouTube experienced an error handling a request. You could retry the request at a later time.
			#503 (Service unavailable) - A 503 response code indicates that the YouTube Data API service can not be reached. You could retry your request at a later time.
			elif ( err.find("500") > -1 or err.find("503") > -1 ):
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage retry: " + error
				return self._fetchPage(link, api, auth, login, error +1)
			else:
				if self.__dbg__:
					print self.__plugin__ + " _fetchPage unknown error"
				return ( err, 303 )
							
		except:
			if self.__dbg__:
				print self.__plugin__ + ' _fetchPage ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
												 , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				
			return ( "", 500 )
		
	def _getAuth(self):
		if self.__dbg__:
			print self.__plugin__ + " _getAuth"

		auth = self.__settings__.getSetting( "auth" )

		if ( auth ):
			if self.__dbg__:
				print self.__plugin__ + " _getAuth returning stored auth"
			return auth
		else:
			(result, status ) =  self.login()
			if status == 200:
				if self.__dbg__:
					print self.__plugin__ + " _getAuth returning new auth"
					
				return self.__settings__.getSetting( "auth" )
			else:
				if self.__dbg__:
					print self.__plugin__ + " _getAuth failed because login failed"
				return False
	
	def _youTubeAdd(self, url, add_request, retry = True):
		if self.__dbg__:
			print self.__plugin__ + " _youTubeAdd: " + repr(url) + " add_request " + repr(add_request)
		auth = self._getAuth()
		if ( not auth ):
			if self.__dbg__:
				print self.__plugin__ + " playlists auth wasn't set "
			return ( self.__language__(30609) , 303 )
		
		try:
			request = urllib2.Request(url, add_request)
			request.add_header('Authorization', 'GoogleLogin auth=%s' % auth)
			request.add_header('X-GData-Client', "")
			request.add_header('X-GData-Key', 'key=%s' % self.APIKEY)
			request.add_header('Content-Type', 'application/atom+xml')
			request.add_header('Content-Length', str(len(add_request)))
			request.add_header('GData-Version', '2')
			usock = urllib2.urlopen(request)
		except urllib2.HTTPError, e:
			error = str(e)
			if self.__dbg__:
				print self.__plugin__ + " _youTubeAdd exception: " + error
				
			if ( error.find("201") > -1):
				if self.__dbg__:
					print self.__plugin__ + " _youTubeAdd: Done"
				return ( "", 200)
			elif (error.find("503") > -1):
				if self.__dbg__:
					print self.__plugin__ + " _youTubeAdd: " + self.__language__(30615)
				return ( self.__language__(30615), 303 )
			elif ( error.find("401") > -1 and retry):
				# If login credentials are given, try again.
				if ( self.__settings__.getSetting( "username" ) == "" or self.__settings__.getSetting( "user_password" ) == "" ):
					if self.__dbg__:
						print self.__plugin__ + " _youTubeAdd trying again with login "
						
					self.login()
					#def _fetchPage(self, link, api = False, auth=False, login=False, error = 0):
					return self._youTubeAdd(url, add_request, False)
					#return self._fetchPage(link, api, auth, login, error + 1)
				else:
					if self.__dbg__:
						print self.__plugin__ + " _youTubeAdd 401 Not Authorized and no login credentials written in settings"
					return ( self.__language__(30622), 303)
			else:
				if self.__dbg__:
					print self.__plugin__ + " _youTubeAdd error not caught " 
				return ( error, 303 )
	
	def _youTubeDel(self, delete_url, retry = True):
		if self.__dbg__:
			print self.__plugin__ + " _youTubeDel: " + delete_url

		auth = self._getAuth()
		if ( not auth ):
			if self.__dbg__:
				print self.__plugin__ + " _youTubeDel auth wasn't set "
			return ( self.__language__(30609) , 303 )

		try:
			headers = {}
			headers['Authorization'] = 'GoogleLogin auth=%s' % (auth)
			headers['X-GData-Client'] = ""
			headers['X-GData-Key'] = 'key=%s' % self.APIKEY
			headers['Content-Type'] = 'application/atom+xml'
			headers['Host'] = 'gdata.youtube.com'
			headers['GData-Version'] = '2'
			import httplib
			conn = httplib.HTTPConnection('gdata.youtube.com')
			conn.request('DELETE', delete_url, headers=headers)
			response = conn.getresponse()
			if (response.status == 200):
				if self.__dbg__:
					print self.__plugin__ + " _youTubeDel: done"
				return ( "", 200 )
			elif (response.status == 401 and retry):
				# If login credentials are given, try again.
				if ( self.__settings__.getSetting( "username" ) == "" or self.__settings__.getSetting( "user_password" ) == "" ):
					if self.__dbg__:
						print self.__plugin__ + " _youTubeDel trying again with login "
						
					self.login()
					return self._youTubeDel(delete_url, False);
					#return self._fetchPage(link, api, auth, login, error +1)
				else:
					if self.__dbg__:
						print self.__plugin__ + " _youTubeDel 401 Not Authorized and no login credentials written in settings"
					return ( self.__language__(30622), 303)
			else:
				resp = str(response.read())
				if self.__dbg__:
					print self.__plugin__ + " _youTubeDel: [%s] %s" % ( response.status, resp )
				return ( resp, 303 )
		except urllib2.HTTPError, e:
			if self.__dbg__:
				print self.__plugin__ + " _youTubeDel except: " + str(e)
			return ( str(e), 303 )
		except:
			if self.__dbg__:
				print self.__plugin__ + " _youTubeDel uncaught exception"
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
								   , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				
			return ( "", 500 )
	
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

	def _getVideoInfoBatch(self, value):
		if self.__dbg__:
			print self.__plugin__ + " _getvideoinfo: " + str(len(value))
		
		dom = parseString(value);
		links = dom.getElementsByTagName("atom:link");
		entries = dom.getElementsByTagName("atom:entry");
		next = "false"
			
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = "true"
					break
		
		ytobjects = [];
		for node in entries:
			video = {};
			videoid = self._getNodeValue(node, "atom:id", "")
			
			#redo this shit
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
						value = self._getNodeValue(node, "yt:state", "Unknown reasonValue").encode('utf-8')
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
				
				video['next'] = next
				ytobjects.append(video);
		
		if (ytobjects):
			return (ytobjects, 200);
		
		return ( "", 500 )
	
	def _getvideoinfo(self, value):
		if self.__dbg__:
			print self.__plugin__ + " _getvideoinfo: " + str(len(value))
		
		dom = parseString(value);
		links = dom.getElementsByTagName("link");
		entries = dom.getElementsByTagName("entry");
		if (not entries):
			entries = dom.getElementsByTagName("atom:entry");
		next = "false"

		#find out if there are more pages
		
		if (len(links)):
			for link in links:
				lget = link.attributes.get
				if (lget("rel").value == "next"):
					next = "true"
					break

		#construct list of video objects					
		ytobjects = [];
		for node in entries:
			video = {};

			video['videoid'] = self._getNodeValue(node, "yt:videoid", "missing")
			
			# http://code.google.com/intl/en/apis/youtube/2.0/reference.html#youtube_data_api_tag_yt:state <- more reason codes
			# requesterRegion - This video is not available in your region. <- fails
			# limitedSyndication - Syndication of this video was restricted by its owner. <- works

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
							print self.__plugin__ + " _getvideoinfo hit else : %s - %s" % ( reason, value)
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
			
			# media:credit is not set for favorites, playlists or inbox
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
			print "plot updated"
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
			
			video['next'] = next
			
			if video['videoid'] == "false":
				if self.__dbg__:
					print self.__plugin__ + " _getvideoinfo videoid set to false"
													
			
			ytobjects.append(video);

		if self.__dbg__:
			print self.__plugin__ + " _getvideoinfo done : " + str(len(ytobjects))
		return ytobjects;

	def _getAlert(self, videoid):
		if self.__dbg__:
			print self.__plugin__ + " _getAlert begin"
		
		http_result = self._fetchPage('http://www.youtube.com/watch?v=' +videoid + "&safeSearch=none", login = True)
		
		start = http_result.find('class="yt-alert-content">')
		if start == -1:
			return self.__language__(30622)
		
		start += len('class="yt-alert-content">')
		result = http_result[start: http_result.find('</div>', start)].strip()
		
		if self.__dbg__:
			print self.__plugin__ + " _getAlert done: " + repr(start)
		
		return result