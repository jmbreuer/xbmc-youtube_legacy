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

import sys, urllib, os, socket, time
import xbmc
import YouTubeUtils
	
class YouTubeStorage(YouTubeUtils.YouTubeUtils):
	__settings__ = sys.modules[ "__main__"].__settings__ 
	__plugin__ = sys.modules[ "__main__"].__plugin__
	__language__ = sys.modules[ "__main__" ].__language__
	__socket__ = (socket.gethostname(), 51999)
	
	# This list contains the list options a user sees when indexing a contact 
	#				label					  , external		 , login		 ,	thumbnail					, feed
	user_options = (
				{'Title':__language__( 30020 ), 'external':"true", 'login':"true", 'thumbnail':"favorites", 	'user_feed':"favorites"},
				{'Title':__language__( 30023 ), 'external':"true", 'login':"true", 'thumbnail':"playlists", 	'user_feed':"playlists", 'folder':"true"},
				{'Title':__language__( 30021 ), 'external':"true", 'login':"true", 'thumbnail':"subscriptions", 'user_feed':"subscriptions", 'folder':"true"},
				{'Title':__language__( 30022 ), 'external':"true", 'login':"true", 'thumbnail':"uploads", 		'user_feed':"uploads"},
				)
	
	def list(self, params = {}):
		get = params.get
		if get("store") == "contact_options":
			return self.getUserOptionFolder(params)
		elif get("store") == "artists":
			return self.getStoredArtists(params)
		elif get("store"):
			return self.getStoredSearches(params)
	
	def getStoredArtists(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " getStoredArtists"
		
		artists = self.retrieve(params)
				
		result = []
		for title, artist in artists:
			item = {}
			item["path"] = get("path")
			item["Title"] = urllib.unquote_plus(title)
			item["artist"] = artist
			item["scraper"] = "music_artist"
			item["icon"] = "music" 
			item["thumbnail"] = "music"
			thumbnail = self.retrieve(params, "thumbnail", item)
			
			if thumbnail:
				item["thumbnail"] = thumbnail	
			
			result.append(item)
				
		return (result, 200)
	
	def deleteStoredArtist(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " deleteStoredArtist"

		artist = get("artist")
		artists = self.retrieve(params)
		
		for count, (title, artist_id) in enumerate(artists):
			if (artist == artist_id):
				del(artists[count])
				break
		
		self.store(params, artists)
		
		xbmc.executebuiltin( "Container.Refresh" )
		
	def saveStoredArtist(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " saveStoredArtist"

		
		if get("artist") and get("artist_name"):
			params["store"] = "artists"
			artists = self.retrieve(params)
			searchCount = ( 10, 20, 30, 40, )[ int( self.__settings__.getSetting( "saved_searches" ) ) ]
			artists = [(get("artist_name"), get("artist"))] + artists[:searchCount]
			self.store(params, artists)
			del params["store"]
		
	def getStoredSearches(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " getStoredSearches"
		
		searches = self.retrieve(params)
				
		result = []
		for search in searches:
			item = {}
			item["path"] = get("path")
			item["Title"] = search
			item["search"] = urllib.quote_plus(search)
			
			if (get("store") == "searches"):
				item["feed"] = "search"
				item["icon"] = "search" 
			elif get("store") == "disco_searches":
				item["scraper"] = "search_disco"
				item["icon"] = "discoball"
			
			thumbnail = self.retrieve(params, "thumbnail", item)
			if thumbnail:
				item["thumbnail"] = thumbnail
			else: 
				item["thumbnail"] = item["icon"] 
			result.append(item)
				
		return (result, 200)
			
	def deleteStoredSearch(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " deleteStoredSearch"

		
		query = urllib.unquote_plus(get("delete"))		
		searches = self.retrieve(params)
		
		for count, search in enumerate(searches):
			if (search.lower() == query.lower()):
				del(searches[count])
				break
		
		self.store(params, searches)
		
		xbmc.executebuiltin( "Container.Refresh" )
	
	def saveStoredSearch(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " saveStoredSearch"
		
		if get("search"):
			searches = self.retrieve(params)
			
			new_query = urllib.unquote_plus(get("search"))
			old_query = new_query
			
			if get("old_search"):
				old_query = urllib.unquote_plus(get("old_search"))
			
			for count, search in enumerate(searches):
				if (search.lower() == old_query.lower()):
					del(searches[count])
					break
			
			searchCount = ( 10, 20, 30, 40, )[ int( self.__settings__.getSetting( "saved_searches" ) ) ]
			searches = [new_query] + searches[:searchCount]
			self.store(params, searches)
	
	def editStoredSearch(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " editStoredSearch"


		if (get("search")):
			old_query = urllib.unquote_plus(get("search"))
			new_query = self.getUserInput(self.__language__(30515), old_query)
			params["search"] = new_query
			params["old_search"] = old_query
			
			if get("action") == "edit_disco":
				params["scraper"] = "search_disco"
				params["store"] = "disco_searches"
			else:
				params["store"] = "searches"
				params["feed"] = "search"
			
			self.saveStoredSearch(params)

			params["search"] = urllib.quote_plus(new_query)
			del params["old_search"]
		
		del params["action"]
		del params["store"]
		
	def getUserOptionFolder(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " getUserOptionsFolder"

		result = []
		for item in self.user_options:
			item["path"] = get("path")
			item["contact"] = get("contact")
			result.append(item)
		
		return (result, 200)
	
	def changeSubscriptionView(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " changeSubscriptionsView"

		
		if (get("view_mode")):  
			key = self.getStorageKey(params, "viewmode")
			
			self.storeValue(key, get("view_mode"))
			
			params['user_feed'] = get("view_mode")
			if get("viewmode") == "playlists":
				params["folder"] = "true"
	
	def reversePlaylistOrder(self, params = {}):
		get = params.get
		if self.__dbg__:
			print self.__plugin__ + " reversePlaylistOrder"
		
		if (get("playlist")):			
			value = "true"
			existing = self.retrieve(params, "value")
			if existing == "true":
				value = "false"
			
			self.store(params, value, "value")
		
		xbmc.executebuiltin( "Container.Refresh" )
		
	def getReversePlaylistOrder(self, params = {}):
		get = params.get 
		if self.__dbg__:
			print self.__plugin__ + " getReversePlaylistOrder"
		
		result = False
		if (get("playlist")):
			existing = self.retrieve(params, "value")
			if existing == "true":
				result = True
		
		return result
	
	#=================================== Storage Key ========================================
	def getStorageKey(self, params = {}, type = "", item = {}):
		get = params.get
		
		if type == "value":
			return self._getValueStorageKey(params, item)
		elif type == "viewmode":
			return self._getViewModeStorageKey(params, item)
		elif type == "thumbnail":
			return self._getThumbnailStorageKey(params, item)
		
		return self._getResultSetStorageKey(params)
		
	def _getThumbnailStorageKey(self, params = {}, item = {}):
		get = params.get
		iget = item.get
		key = ""
		
		if get("search") or iget("search"):
			key = "disco_search_"
			if get("feed"):
				key = "search_"
			
			if get("store") == "searches":
				key = "search_"
			
			if get("search"):
				key += urllib.unquote_plus(get("search",""))
			
			if iget("search"):
				key += urllib.unquote_plus(iget("search",""))
		
		if get("artist") or iget("artist"):
			key = "artist_"
			
			if get("artist"):
				key += get("artist")
			
			if iget("artist"):
				key += iget("artist")
			
		if get("user_feed"):
			key = get("user_feed")
			
			if get("channel"):
				key = "subscriptions_" + get("channel")

			if iget("channel"):
				key += "_" + iget("channel")
		
			if get("playlist"):
				key += "_" + get("playlist")
			
			if iget("playlist"):
				key = "playlist_" + iget("playlist")
			
		if key:
			key += "_thumb"
		
		return key
	
	def _getValueStorageKey(self, params = {}, item = {}):
		get = params.get
		iget = item.get
		key = ""
		
		if ((get("action") == "reverse_order" or get("user_feed") == "playlist") and (iget("playlist") or get("playlist"))):
			
			key = "reverse_playlist_" 
			if iget("playlist"):
				key += iget("playlist")
			
			if get("playlist"):
				key += get("playlist")
				
			if (get("external")):
				key += "_external_" + get("contact")
		
		return key 
	
	def _getViewModeStorageKey(self, params = {}, item = {}):
		get = params.get
		iget = item.get
		key = ""
				
		if (get("external")):
			key = "external_" + get("contact") + "_"
		elif (iget("external")):
			key = "external_" + iget("contact") + "_"
					
		if get("channel"):
			key += "view_mode_" + get("channel")
		elif (iget("channel")):  
			key += "view_mode_" + iget("channel")
		
		return key
		
	def _getResultSetStorageKey(self, params = {}):
		get = params.get
		
		key = ""
		
		if get("scraper"):
			key = "s_" + get("scraper")
			
			if get("scraper") == "music_hits" and get("category"):
				key += "_" + get("category")
			
			if get("scraper") == "music_artist" and get("artist"):
				key += "_" + get("artist")
			
			if get("scraper") == "disco_search":
				key = "store_disco_searches"
			
			if get("category"):
				key += "_category_" + get("category")
			
			if get("show"):
				key += "_season_" + get("season","0")
		
		if get("user_feed"):
			key = "result_" + get("user_feed")
			
			if get("playlist"):
				key += "_" + get("playlist")
			
			if get("channel"):
				key += "_" + get("channel")
			
			if get("external") and not get("thumb"):
				key += "_external_" + get("contact")
		
		if get("feed") == "search":
			key = "store_searches"
		
		if get("store"):
			key = "store_"+ get("store")
		
		return key
	
	#============================= Storage Functions =================================
	def store(self, params = {}, results = [], type = "", item = {}):
		key = self.getStorageKey(params, type, item)
		
		print self.__plugin__ + " Got key " + repr(key)
		
		if type == "thumbnail" or type == "viewmode" or type == "value":
			self.storeValue(key, results)
		else:
			self.storeResultSet(key, results)

	def storeValue(self, key, value):
		if value:
			self.sqlSet(key, value)

	def storeResultSet(self, key, results = [], params = {}):
		get = params.get
		
		if results:
			if get("prepend"):
				searchCount = ( 10, 20, 30, 40, )[ int( self.__settings__.getSetting( "saved_searches" ) ) ]
				existing = self.retrieveResultSet(key)  
				existing = [results] + existing[:searchCount]
				self.sqlSet(key, repr(existing))
			elif get("append"):
				existing = self.retrieveResultSet(key)  
				existing = existing.append(results)
				self.sqlSet(key, repr(existing))
			else:
				value = repr(results)
				self.sqlSet(key,value)
	
	#============================= Retrieval Functions =================================
	def retrieve(self, params = {}, type = "", item = {}):
		key = self.getStorageKey(params, type, item)
		
		print self.__plugin__ + " Got key " + repr(key)
		
		if type == "thumbnail" or type == "viewmode" or type == "value":
			return self.retrieveValue(key)
		else:
			return self.retrieveResultSet(key)

	def retrieveValue(self, key):
		value = ""
		if key:
			value = self.sqlGet(key)
		
		return value
	
	def retrieveResultSet(self, key):
		results = []
		
		value = self.sqlGet(key)		
		if value: 
			try:
				results = eval(value)
			except:
				results = []
		
		return results
		
	#============================= Download Queue =================================
	def getNextVideoFromDownloadQueue(self):
		if self.lock("YouTubeQueueLock"):
			videos = []
			
			queue = self.sqlGet("YouTubeDownloadQueue")
			print self.__plugin__ + " queue loaded : " + repr(queue)

			if queue:
				try:
					videos = eval(queue)
				except: 
					videos = []
		
			videoid = ""
			if videos:
				videoid = videos[0]

			self.unlock("YouTubeQueueLock")
			print self.__plugin__ + " getNextVideoFromDownloadQueue released. returning : " + videoid
			return videoid
		else:
			print self.__plugin__ + " getNextVideoFromDownloadQueue Exception "

	def addVideoToDownloadQeueu(self, params = {}):
		if self.lock("YouTubeQueueLock"):
			get = params.get

			videos = []
			if get("videoid"):
				queue = self.sqlGet("YouTubeDownloadQueue")
				print self.__plugin__ + " queue loaded : " + repr(queue)

				if queue:
					try:
						videos = eval(queue)
					except:
						videos = []
		
				if get("videoid") not in videos:
					videos.append(get("videoid"))
					
					self.sqlSet("YouTubeDownloadQueue", repr(videos))
					print self.__plugin__ + " Added: " + get("videoid") + " to: " + repr(videos)

			self.unlock("YouTubeQueueLock")
			print self.__plugin__ + " addVideoToDownloadQeueu released"
		else:
			print self.__plugin__ + " addVideoToDownloadQeueu Exception "
		
	def removeVideoFromDownloadQueue(self, videoid):
		if self.lock("YouTubeQueueLock"):
			videos = []
			
			queue = self.sqlGet("YouTubeDownloadQueue")
			print self.__plugin__ + " queue loaded : " + repr(queue)
			if queue:
				try:
					videos = eval(queue)
				except:
					videos = []
		
			if videoid in videos:
				videos.remove(videoid)

				self.sqlSet("YouTubeDownloadQueue", repr(videos))
				print self.__plugin__ + " Removed: " + videoid + " from: " + repr(videos)
			else:
				print self.__plugin__ + " Didn't remove: " + videoid + " from: " + repr(videos)

			self.unlock("YouTubeQueueLock")
			print self.__plugin__ + " removeVideoFromDownloadQueue released"
		else:
			print self.__plugin__ + " removeVideoFromDownloadQueue Exception "

	def cacheFunction(self, funct = False, params = {}):
		if funct:
			name = repr(funct)
			if params.has_key("new_results_function"):
				del(params["new_results_function"])
			name = name[name.find("method") + 7 :name.find(" of ")]
			print self.__plugin__ + " _cacheFunction: " + name + repr(params)
			cache = {}
			ret = False

			if self.sqlGet("cache" + name):
				print self.__plugin__ + " _cacheFunction cache exists "
				cache = self.sqlGet("cache" + name)
				if cache.strip() == "":
					cache = {}
				else:
					cache = eval(cache)
				print self.__plugin__ + " _cacheFunction: " + name + repr(params) + " in cache: " + repr(name + repr(params) in cache) 
				if name + repr(params) in cache:
					print self.__plugin__ + " _cacheFunction returning cache for : " + name + repr(params)
					#print self.__plugin__ + " _cacheFunction returning : " + str(len(cache[name + repr(params)]["res"])) + " - " + str(cache[name + repr(params)]["timestamp"])
					if cache[name + repr(params)]["timestamp"] > time.time() - (3600 * 24):
						ret = cache[name + repr(params)]["res"]
					else:
						print self.__plugin__ + " _cacheFunction Deleting old cache"
						del(cache[name + repr(params)])
			if not ret :
				print self.__plugin__ + " _cacheFunction no match in cache : " + repr(ret)
				cache[name + repr(params)] = { "timestamp": time.time(),
						       "res": funct(params)}
				#print self.__plugin__ + " _cacheFunction no match in cache2: " + repr(name + repr(params) in cache)
				#print self.__plugin__ + " _cacheFunction saving: " + name + repr(params) + " - " + str(len(cache[name + repr(params)]["res"])) + repr(cache[name + repr(params)]["res"])
				self.sqlSet("cache" + name, repr(cache))
				ret = cache[name + repr(params)]["res"]

			if ret:
				print self.__plugin__ + " _cacheFunction returning "
				return ret

		print self.__plugin__ + " _cacheFunction Error " 
		return False

	def cacheFunctionThree(self, funct = False, items = [], params = {}):
		if funct:
			if params.has_key("new_results_function"):
				del(params["new_results_function"])
			name = repr(funct)
			name = name[name.find("method") + 7 :name.find(" of ")]
			print self.__plugin__ + " _cacheFunctionThree " + name
			cache = {}
			ret = False
			if self.sqlGet("cache" + name):
				#print self.__plugin__ + " _cacheFunctionThree cache exists "
				cache = self.sqlGet("cache" + name)
				if cache.strip() == "":
					cache = {}
				else:
					cache = eval(cache)
				#print self.__plugin__ + " _cacheFunctionThree cache exists: " + repr(name + repr(items) + repr(params) in cache) + repr(cache)
				if name + repr(items) + repr(params) in cache:
					#print self.__plugin__ + " _cacheFunctionThree returning cache for : " + name + repr(items) + repr(params)
					#print self.__plugin__ + " _cacheFunctionThree returning : " + str(len(cache[name + repr(items) + repr(params)]["res"])) + " - " + str(cache[name + repr(items) + repr(params)]["timestamp"])
					if cache[name + repr(items) + repr(params)]["timestamp"] > time.time() - (3600 * 24):
						ret = cache[name + repr(items) + repr(params)]["res"]
					else:
						print self.__plugin__ + " _cacheFunctionThree Deleting old cache"
						del(cache[name + repr(items) + repr(params)])
			if not ret :
				#print self.__plugin__ + " _cacheFunctionThree no match in cache : " + repr(ret)
				cache[name + repr(items) + repr(params)] = { "timestamp": time.time(),
						       "res": funct(items, params)}
				#print self.__plugin__ + " _cacheFunctionThree no match in cache2: " + repr(name + repr(items) + repr(params) in cache)
				#print self.__plugin__ + " _cacheFunctionThree saving: " + repr(cache[name + repr(items) + repr(params)]["timestamp"]) + name + repr(items) + repr(params)
				self.sqlSet("cache" + name, repr(cache))
				#self.sqlSet("cache", "")
				ret = cache[name + repr(items) + repr(params)]["res"]

			if ret:
				print self.__plugin__ + " _cacheFunctionThree returning "
				return ret

		print self.__plugin__ + " _cacheFunctionThree Error " 
		return False

	def cleanCache(self):
		cache = {}
		return False
		if self.sqlGet("cache"):
			cache = eval(self.sqlGet("cache"))

		if cache:
			for item in cache:
				if cache[item]["timestamp"] < time.time() - (3600 * 24):
					del(cache[item])

			self.sqlSet("cache", repr(cache))
			return True
		return False

	def lock(self, name):
			print self.__plugin__ + " lock " + name
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(self.__socket__)
			data = repr({ "action": "lock", "name": name})
			#print self.__plugin__ + " lock sending data "
			s.send(data + "\r\n")
			#print self.__plugin__ + " lock waiting for data "
			res = s.recv(4096 * 4096)
			#print self.__plugin__ + " lock sending ACK "
			s.send("ACK\r\n")
			if res:
				if eval(res) == "true":
					print self.__plugin__ + " lock GOT True : " + res.strip()
					return True
				else:
					print self.__plugin__ + " lock GOT False : " + res.strip()
					return False

	def unlock(self, name):
			print self.__plugin__ + " unlock " + name
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(self.__socket__)
			data = repr({ "action": "unlock", "name": name})
			s.send(data + "\r\n")
			res = s.recv(4096 * 4096)
			print self.__plugin__ + " unlock sending ACK "
			s.send("ACK\r\n")
			print self.__plugin__ + " unlock GOT " + res

	def sqlSet(self, name, data):
			print self.__plugin__ + " sqlSet " + name
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(self.__socket__)
			temp = repr({ "action": "set", "name": name, "data": data})
			while len(temp) > 0:
				if len(temp) > 50000:
					data = temp[:50000]
					temp = temp[50000:]
				else:
					data = temp + "\r\n"
					temp = ""
				s.send(data)
			res = s.recv(4096 * 4096)
			#print self.__plugin__ + " sqlset sending ACK "
			s.send("ACK\r\n")
			#print self.__plugin__ + " sqlset GOT " + res


	def sqlGet(self, name):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(self.__socket__)
			s.send(repr({ "action": "get", "name": name}) + "\r\n")
			res = s.recv(4096 * 4096)
			s.send("ACK\r\n")
			#print self.__plugin__ + " sqlGet sending ACK "
			i = 0
			while res[len(res)-2:] != "\r\n":
				#print self.__plugin__ + " sqlGet while res : " + str(len(res)) + " - " + res[len(res)-1]
				#print self.__plugin__ + " sqlGet sending ACK " + str(i)
				i += 1
				res += s.recv(4096 * 4096)
				s.send("ACK\r\n")
			
			if res:
				res = eval(res.strip())
				return res.strip() # We return " " as nothing. Strip it out.

			return False


