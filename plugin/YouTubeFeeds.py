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

import sys, urllib

class YouTubeFeeds():
	
	# YouTube General Feeds
	urls = {}
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
	urls["recommended"] = "https://gdata.youtube.com/feeds/api/users/default/recommendations"
	urls['watch_later'] = "https://gdata.youtube.com/feeds/api/users/default/watch_later?v=2.1"
	
	# YouTube Standard feeds
	urls['feed_rated'] = "http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?time=%s"
	urls['feed_favorites'] = "http://gdata.youtube.com/feeds/api/standardfeeds/top_favorites?time=%s"
	urls['feed_viewed'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?time=%s"
	urls['feed_linked'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_popular?time=%s" 
	urls['feed_discussed'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_discussed?time=%s"
	urls['feed_responded'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_responded?time=%s"
	urls['feed_live'] = "http://gdata.youtube.com/feeds/api/charts/live/events/live_now"
	
	# Wont work with time parameter
	urls['feed_recent'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_recent" 
	urls['feed_featured'] = "http://gdata.youtube.com/feeds/api/standardfeeds/recently_featured"
	urls['feed_trending'] = "http://gdata.youtube.com/feeds/api/standardfeeds/on_the_web"
	urls['feed_shared'] = "http://gdata.youtube.com/feeds/api/standardfeeds/most_shared"
	
	def __init__(self):
		self.settings = sys.modules[ "__main__" ].settings
		self.language = sys.modules[ "__main__" ].language
		self.plugin = sys.modules[ "__main__" ].plugin
		self.dbg = sys.modules[ "__main__" ].dbg
		self.utils = sys.modules["__main__"].utils
		self.storage = sys.modules[ "__main__" ].storage
		self.core = sys.modules[ "__main__" ].core
		self.common = sys.modules ["__main__"].common
	
	def createUrl(self, params = {}):
		get = params.get
		time = "this_week"
		per_page = ( 10, 15, 20, 25, 30, 40, 50 )[ int( self.settings.getSetting( "perpage" ) ) ]
		region = ('', 'AU', 'BR', 'CA', 'CZ', 'FR', 'DE', 'GB', 'NL', 'HK', 'IN', 'IE', 'IL', 'IT', 'JP', 'MX', 'NZ', 'PL', 'RU', 'KR', 'ES','SE', 'TW', 'US', 'ZA' )[ int( self.settings.getSetting( "region_id" ) ) ]
		
		print "perpage " +repr(per_page)
		page = get("page","0")
		start_index = per_page * int(page) + 1
		url = ""
		
		if (get("feed")):
			url = self.urls[get("feed")]
		
		if (get("user_feed")):
			url = self.urls[get("user_feed")]
		
		if get("search"):
			url = self.urls["search"]
			query = urllib.unquote_plus(get("search"))
			safe_search = ("none", "moderate", "strict" ) [int( self.settings.getSetting( "safe_search" ) ) ]	
			url = url % (query, safe_search)  
			authors = self.settings.getSetting("stored_searches_author")
			if len(authors) > 0:
				try:
					authors = eval(authors)
					if query in authors:
						url += "&" + urllib.urlencode({'author': authors[query]})
				except:
					self.common.log("Search - eval failed")
		
		if (url.find("%s") > 0):
			if ( get("contact") and not (get("external") and get("channel"))):
				url = url % get("contact")
			elif ( get("channel") ):
				url = url % get("channel")
			elif ( get("playlist") ):
				url = url % get("playlist")
			elif ( get("videoid") and not get("action") == "add_to_playlist"):
				url = url % get("videoid")
			elif (url.find("time=") > 0 ): 
				url = url % time			
			else: 
				url = url % "default"
		
		if ( url.find("?") == -1 ):
			url += "?"
		else:
			url += "&"
			
		if not get("playlist") and not get("folder") and not get("action") == "play_all" and not get("action") == "add_to_playlist":
			url += "start-index=" + repr(start_index) + "&max-results=" + repr(per_page)
		
		if (url.find("standardfeeds") > 0 and region):
			url = url.replace("/standardfeeds/", "/standardfeeds/"+ region + "/")
						
		url = url.replace(" ", "+")
		return url
	
	def list(self, params = {}):
		self.common.log("", 4)
		get = params.get
		result = { "content": "", "status": 303 }
		
		if get("folder"):
			return self.listFolder(params)
		
		if get("playlist"):
			return self.listPlaylist(params)
		
		if get("login") == "true":
			if ( not self.core._getAuth() ):
				self.common.log("Login required but auth wasn't set!")
				return ( self.language(30609) , 303 )

		url = self.createUrl(params)
		
		if url:
			self.common.log(repr(url), 4)
			result = self.core._fetchPage({"link": url, "auth": get("login"), "api": "true"})
		
		if result["status"] != 200:
			return ( result["content"], result["status"] )
		
		if not get("folder"):
			videos = self.core.getVideoInfo(result["content"], params)
		
		if len(videos) == 0:
			return (videos, 303)
		
		thumbnail = videos[0].get('thumbnail', "")
		
		if thumbnail:
			self.storage.store(params, thumbnail, "thumbnail")
					
		self.common.log("Done", 4)
		return (videos, 200)
	
	def listPlaylist(self, params = {}):
		get = params.get
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50 )[ int( self.settings.getSetting( "perpage" ) ) ]
		next = 'false'
		
		videos = self.storage.retrieve(params)
		
		if page != 0 and videos:
			if ( per_page * ( page + 1 ) < len(videos) ):
				next = 'true'
			
			videos = videos[(per_page * page):(per_page * (page + 1))]

			(result, status) = self.core.getBatchDetailsOverride(videos, params)
		else:
			result = self.listAll(params)
			
			if len(result) == 0:
				return (result, 303)
			
			videos = []
			for video in result:
				vget = video.get
				item = {}
				item["playlist_entry_id"] = vget("playlist_entry_id")
				item["videoid"] = vget("videoid")
				videos.append(item)
			
			self.storage.store(params, videos)
			
			thumbnail = result[0].get('thumbnail', "")
			if (thumbnail):
				self.storage.store(params, thumbnail, "thumbnail")
			
			if (len(result) > 0):
				if ( per_page * ( page + 1 ) < len(result) ):
					next = 'true'
			
			result = result[(per_page * page):(per_page * (page + 1))]
		
		if next == "true":
			self.utils.addNextFolder(result, params)
		
		return (result, 200)
	
	def listFolder(self, params = {}):
		get = params.get
		result = []
		
		if get("store"): 
			if get("store") == "contact_options":
				return self.storage.getUserOptionFolder(params)
			else:
				return self.storage.getStoredSearches(params)
		
		page = int(get("page", "0"))
		per_page = ( 10, 15, 20, 25, 30, 40, 50 )[ int( self.settings.getSetting( "perpage" ) ) ]
		
		if ( page != 0):
			result = self.storage.retrieve(params)
		
		elif not get("page"):
			result = self.listAll(params)
			if len(result) == 0:
				return (result, 303)
			
			self.storage.store(params, result)
		
		next = 'false'
		
		if (len(result) > 0):
			if ( per_page * ( page + 1 ) < len(result) ):
				next = 'true'
		result = result[(per_page * page):(per_page * (page + 1))]
		
		if get("user_feed") == "subscriptions":
			for item in result:
				viewmode = self.storage.retrieve(params, "viewmode", item)
				
				if (get("external")):
					item["external"] = "true"
					item["contact"] = get("contact")	
				
				if (viewmode == "favorites"):
					item["user_feed"] = "favorites"
					item["view_mode"] = "subscriptions_uploads"
				elif(viewmode == "playlists"):
					item["user_feed"] = "playlists"
					item["folder"] = "true"
					item["view_mode"] = "subscriptions_playlists"
				else:
					item["user_feed"] = "uploads"  
					item["view_mode"] = "subscriptions_favorites"
		
		if next == "true":
			self.utils.addNextFolder(result, params)
		
		return (result, 200)
	
	def listAll(self, params ={}):
		self.common.log("")
		get = params.get
		result = { "content": "", "status": 303 }
		
		if get("login") == "true":
			if ( not self.core._getAuth() ):
				self.common.log("login required but auth wasn't set!")
				return ( self.language(30609) , 303 )
		
		feed = self.createUrl(params)
		index = 1
		url = feed + "v=2.1&start-index=" + str(index) + "&max-results=" + repr(50)
		url = url.replace(" ", "+")

		ytobjects = []
		
		result = self.core._fetchPage({"link":url, "auth":"true"})
		
		if result["status"] == 200:
			if get("folder") == "true":
				ytobjects = self.core.getFolderInfo(result["content"], params)
			else:
				ytobjects = self.core.getVideoInfo(result["content"], params)
		
		if len(ytobjects) == 0:
			return ytobjects
		
		next = ytobjects[len(ytobjects)-1].get("next","false")
		if next == "true": 
			ytobjects = ytobjects[:len(ytobjects)-1]
		
		while next == "true":
			index += 50
			url = feed + "start-index=" + str(index) + "&max-results=" + repr(50)
			url = url.replace(" ", "+")
			result = self.core._fetchPage({"link": url, "auth":"true"})
			
			if result["status"] != 200:
				break
			temp_objects = []
			if get("folder") == "true":
				temp_objects = self.core.getFolderInfo(result["content"], params)
			else:
				temp_objects = self.core.getVideoInfo(result["content"], params)
		
			next = temp_objects[len(temp_objects)-1].get("next","false")
			if next == "true":
				temp_objects = temp_objects[:len(temp_objects)-1]
			ytobjects += temp_objects
		
		if get("user_feed"):
			if get("user_feed") != "playlist" and get("action") != "play_all":
				ytobjects.sort(key=lambda item:item["Title"].lower(), reverse=False)
			else:
				if (self.storage.getReversePlaylistOrder(params)):
					ytobjects.reverse()
		
		return ytobjects
