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
import xbmc
	
class YouTubePluginStorage:
	__settings__ = sys.modules[ "__main__"].__settings__ 
	__plugin__ = sys.modules[ "__main__"].__plugin__
	__language__ = sys.modules[ "__main__" ].__language__
	__utils__ = sys.modules[ "__main__" ].__utils__
	
	# This list contains the list options a user sees when indexing a contact 
	#				label					  , external		 , login		 ,	thumbnail					, feed
	user_options = (
				{'Title':__language__( 30020 ), 'external':"true", 'login':"true", 'thumbnail':"favorites", 	'user_feed':"favorites"},
				{'Title':__language__( 30023 ), 'external':"true", 'login':"true", 'thumbnail':"playlists", 	'user_feed':"playlists", 'folder':"true"},
				{'Title':__language__( 30021 ), 'external':"true", 'login':"true", 'thumbnail':"subscriptions", 'user_feed':"subscriptions", 'folder':"true"},
				{'Title':__language__( 30022 ), 'external':"true", 'login':"true", 'thumbnail':"uploads", 		'user_feed':"uploads"},
				)

	def getStoredSearches(self, params = {}):
		get = params.get
		try:
			if (get("store") == "searches"):
				searches = eval(self.__settings__.getSetting("stored_searches"))
			else:
				searches = eval(self.__settings__.getSetting("stored_disco_searches"))
		except:
			searches = []
		
		result = []
		for search in searches:
			item = {}
			item["path"] = get("path")
			item["Title"] = search
			item["search"] = urllib.quote_plus(search)
			
			if (get("store") == "searches"):
				item["feed"] = "search"
				item["icon"] = self.__utils__.getThumbnail("search")
				item["thumbnail"] = self.__settings__.getSetting("search_" + search + "_thumb")
			else:
				item["scraper"] = "search_disco"
				item["icon"] = self.__utils__.getThumbnail("discoball")
				item["thumbnail"] = self.__settings__.getSetting("disco_search_" + search + "_thumb")
			
			result.append(item)
				
		return (result, 200)
						
	def deleteStoredSearch(self, params = {}):
		get = params.get
		query = get("delete")
		query = urllib.unquote_plus(query)
		try:
			if (get("action") == "delete_search"):
				searches = eval(self.__settings__.getSetting("stored_searches"))
			else:
				searches = eval(self.__settings__.getSetting("stored_disco_searches"))
		except:
			searches = []
			
		for count, search in enumerate(searches):
			if (search.lower() == query.lower()):
				del(searches[count])
				break
		
		if (get("action") == "delete_search"):
			self.__settings__.setSetting("stored_searches", repr(searches))
		else:
			self.__settings__.setSetting("stored_disco_searches", repr(searches))
		
		xbmc.executebuiltin( "Container.Refresh" )
		
	def saveSearch(self, params = {}):
		get = params.get
		
		if (get("store") == "searches" or get("feed") == "search"):
			store = "stored_searches"
		else:
			store = "stored_disco_searches"
		
		new_query = urllib.unquote_plus(get("search"))
		old_query = new_query
		
		if get("old_search"):
			old_query = urllib.unquote_plus(get("old_search"))
		try:
			searches = eval(self.__settings__.getSetting(store))
		except:
			searches = []
		
		for count, search in enumerate(searches):
			if (search.lower() == old_query.lower()):
				del(searches[count])
				break
		
		searchCount = ( 10, 20, 30, 40, )[ int( self.__settings__.getSetting( "saved_searches" ) ) ]
		searches = [new_query] + searches[:searchCount]
		self.__settings__.setSetting(store, repr(searches))
	
	def editStoredSearch(self, params = {}):
		get = params.get
		if (get("search")):
			old_query = urllib.unquote_plus(get("search"))
			new_query = self.__utils__.getUserInput(self.__language__(30515), old_query)
			params["search"] = new_query
			params["old_search"] = old_query
			
			if (get("action") == "edit_search"):
				params["store"] = "searches"
				self.saveSearch(params)
			else:
				params["scraper"] = "search_disco"
				self.saveSearch(params)
		params["feed"] = "search"
		params["old_search"] = ""
		params["store"] = ""
		xbmc.executebuiltin( "Container.Refresh" )
	
	def refineStoredSearch(self, params = {}):
		get = params.get
		query = get("search")
		query = urllib.unquote_plus(query)
		
		try:
			searches = eval(self.__settings__.getSetting("stored_searches_author"))
		except :
			searches = {}
			
		if query in searches:
			author = self.__utils__.getUserInput(self.__language__(30517), searches[query])
		else:
			author = self.__utils__.getUserInput(self.__language__(30517), '')

		if author == "":
			if author in searches:
				del searches[query]
				xbmc.executebuiltin( "Container.Refresh" )
		elif author:
			searches[query] = author
			
			self.__settings__.setSetting("stored_searches_author", repr(searches))
			self.__utils__.showMessage(self.__language__(30006), self.__language__(30616))
			xbmc.executebuiltin( "Container.Refresh" )
		
	def deleteStoredSearchRefinement(self, params = {}):
		get = params.get
		query = get("search")
		query = urllib.unquote_plus(query)
		try:
			searches = eval(self.__settings__.getSetting("stored_searches_author"))
		except :
			searches = {}
			
		if query in searches:
			del searches[query]
			self.__settings__.setSetting("stored_searches_author", repr(searches))
			self.__utils__.showMessage(self.__language__(30006), self.__language__(30610))
			xbmc.executebuiltin( "Container.Refresh" )
		
	def getUserOptionFolder(self, params = {}):
		get = params.get
		result = []
		for item in self.user_options:
			item["path"] = get("path")
			item["contact"] = get("contact")
			result.append(item)
		
		return (result, 200)
	
	def changeSubscriptionView(self, params = {}):
		get = params.get
		
		if (get("view_mode")):  
			viewmode = ""
			if (get("external")):
				viewmode += "external_" + get("contact") + "_"
			viewmode += "view_mode_" + get("channel")
			
			self.__settings__.setSetting(viewmode, get("view_mode"))
		
		xbmc.executebuiltin( "Container.Refresh" )
	
	def reversePlaylistOrder(self, params = {}):
		get = params.get
		
		if (get("playlist")):
			sort = ""
			if (get("external")):
				sort += "external_" + get("contact") + "_"
			sort += "view_mode_" + get("playlist")
			
			existing = self.__settings__.getSetting(sort)
			if existing != "true":
				self.__settings__.setSetting(sort, "true")
			else:
				self.__settings__.setSetting(sort, "false")
		
		xbmc.executebuiltin( "Container.Refresh" )