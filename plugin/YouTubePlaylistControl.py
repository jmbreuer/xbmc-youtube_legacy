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

import sys, xbmcgui, xbmc

class YouTubePlaylistControl():
	
	def __init__(self):
		self.settings = sys.modules[ "__main__" ].settings
		self.language = sys.modules[ "__main__" ].language
		self.plugin = sys.modules[ "__main__"].plugin
		self.dbg = sys.modules[ "__main__" ].dbg

		self.common = sys.modules["__main__"].common
		self.utils =  sys.modules[ "__main__" ].utils
		self.core = sys.modules["__main__" ].core		
			
		self.feeds = sys.modules[ "__main__" ].feeds
		self.scraper = sys.modules[ "__main__" ].scraper
		self.player = sys.modules[ "__main__" ].player
			
	def playAll(self, params={}):
		get = params.get
		self.common.log("")

		params["fetch_all"] = "true"
		result = []
		# fetch the video entries
		if get("playlist"):
			result = self.getPlayList(params)
		elif get("search_disco"):
			params["search"] = params["search_disco"]
			result = self.getDiscoSearch(params)
		elif get("user_feed") == "favorites":
			result = self.getFavorites(params)
		elif get("scraper") == "watch_later":
			result = self.getWatchLater(params)
		elif get("scraper") == "liked_videos":
			result = self.getLikedVideos(params)
		elif get("scraper") == "music_artists":
			result = self.getArtist(params)
		elif get("scraper") == "recommended":
			result = self.getRecommended(params)
		elif get("user_feed") == "newsubscriptions":
			result = self.getNewSubscriptions(params)
		else:
			return
		
		if len(result) == 0:
			return
		
		self.common.log(repr(len(result)) + " video results ")
		
		if get("videoid"):
			video_index = -1
			for index, video in enumerate(result):
				vget = video.get
				if vget("videoid") == get("videoid"):
					video_index = index
			if video_index >= 0:
				result = result[video_index:]
		
		player = xbmc.Player()
		if (player.isPlaying()):
			player.stop()
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
		
		video_url = "%s?path=/root&action=play_video&videoid=%s"  
		# queue all entries
		for entry in result:
			video = entry.get
			listitem=xbmcgui.ListItem(label=video("Title"), iconImage=video("thumbnail"), thumbnailImage=video("thumbnail"))
			listitem.setProperty('IsPlayable', 'true')
			listitem.setProperty( "Video", "true" )
			listitem.setInfo(type='Video', infoLabels=entry)
			playlist.add(video_url % (sys.argv[0], video("videoid") ), listitem)
		
		if (get("shuffle")):
			playlist.shuffle()

		xbmc.executebuiltin('playlist.playoffset(video , 0)')
		
	def queueVideo(self, params = {}):
		get = params.get
		self.common.log("Queuing videos: " + get("videoid"))
		
		items =[]
		videoids = get("videoid")
		
		if videoids.find(','):
			items = videoids.split(',')
		else:
			items.append(videoids)
		
		(video, status) = self.core.getBatchDetails(items, params);

		if status != 200:
			self.common.log("construct video url failed contents of video item " + repr(video))
				
			self.utils.showErrorMessage(self.language(30603), video["apierror"], status)
			return False

		listitem=xbmcgui.ListItem(label=video['Title'], iconImage=video['thumbnail'], thumbnailImage=video['thumbnail'], path=video['video_url']);
		listitem.setProperty('IsPlayable', 'true')
		listitem.setInfo(type='Video', infoLabels=video)

		self.common.log("Queuing video: " + self.makeAscii(video['Title']) + " - " + get('videoid') + " - " + video['video_url'])

		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.add("%s?path=/root&action=play_video&videoid=%s" % (sys.argv[0], video["videoid"] ), listitem)

	def getPlayList(self, params = {}):
		get = params.get
		
		if not get("playlist"):
			return False
		params["user_feed"] = "playlist" 
		return self.feeds.listAll(params)
	
	def getWatchLater(self, params = {}):
		(result, status ) = self.scraper.scrapeWatchLater(params)
		return result

	def getDiscoSearch(self, params = {}):
		(result, status) = self.scraper.searchDisco(params)
		
		if status == 200:
			(result, status) = self.getBatchDetails(result, params)
		
		return result
	
	def getFavorites(self, params = {}):
		get = params.get
		
		if not get("contact"):
			return False
		
		params["user_feed"] = "favorites"
		return self.feeds.listAll(params)
	
	def getNewSubscriptions(self, params = {}):
		get = params.get
		
		if not get("contact"):
			return False
		params["user_feed"] = "newsubscriptions"
		return self.feeds.listAll(params)
	
	def getRecommended(self, params = {}):
		get = params.get
		
		if not get("scraper") or not get("login"):
			return False
		
		(result, status) = self.scraper.scrapeRecommended(params)
		
		if status == 200:
			(result, status) = self.getBatchDetails(result, params)
		
		return result
	
	def getArtist(self, params = {}):
		get = params.get
		
		if not get("artist"):
			return False
		
		(result, status) = self.scraper.scrapeArtist(params)
		
		if status == 200:
			(result, status) = self.getBatchDetails(result, params)
		
		return result
	
	def getLikedVideos(self, params = {}):
		get = params.get
		if not get("scraper") or not get("login"):
			return False
		
		(result, status) = self.scraper.scrapeLikedVideos(params)
		self.common.log("Liked videos "  + repr(result))
		if status == 200:
			(result, status) = self.getBatchDetails(result, params)
			
		return result
		
	def addToPlaylist(self, params = {}):
		get = params.get
		
		result = []
		if (not get("playlist")):
			params["user_feed"] = "playlists"
			params["login"] = "true"
			params["folder"] = "true"
			result = self.feeds.listAll(params)
		
		selected = -1
		if result:
			list = []
			list.append(self.language(30529))
			for item in result:
				list.append(item["Title"])
			dialog = xbmcgui.Dialog()
			selected = dialog.select(self.language(30528), list)
			
		if selected == 0:
			self.createPlayList(params)
			if get("title"):
				result = self.feeds.listAll(params)
				for item in result:
					if get("title") == item["Title"]:
						params["playlist"] = item["playlist"]
						break
		elif selected > 0:
			params["playlist"] = result[selected - 1].get("playlist")
		
		if get("playlist"):
			self.add_to_playlist(params)
			return True
		
		return False
	
	def createPlayList(self, params = {}):
		get = params.get
		
		input = self.getUserInput(self.language(30529))
		if input:
			params["title"] = input
			self.add_playlist(params)
			return True
		return False
				
	def removeFromPlaylist(self, params = {}):
		get = params.get
		
		if get("playlist") and get("playlist_entry_id"):
			(message, status) = self.core.remove_from_playlist(params)
			
			if (status != 200):
				self.showErrorMessage(self.language(30600), message, status)
				return False
			xbmc.executebuiltin( "Container.Refresh" )
		return True
	
	def deletePlaylist(self, params):
		get = params.get
		if get("playlist"):
			(message, status) = self.core.del_playlist(params)
			
			if status != 200:
				self.showErrorMessage(self.language(30600), message, status)
				return False
			xbmc.executebuiltin( "Container.Refresh" )
		return True
