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

import sys
import xbmc
import xbmcgui

class YouTubePlaylistControl:
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__

	__core__ = sys.modules[ "__main__" ].__core__
	__scraper__ = sys.modules[ "__main__" ].__scraper__
	__utils__ = sys.modules[ "__main__" ].__utils__
	
	urls = {};
	urls['playlists'] = "http://gdata.youtube.com/feeds/api/playlists/%s?"
	urls['favorites'] = "http://gdata.youtube.com/feeds/api/users/%s/favorites?"
	urls['newsubscriptions'] = "http://gdata.youtube.com/feeds/api/users/%s/newsubscriptionvideos?";
	
	
	def playAll(self, params={}):
		get = params.get
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
		elif get("user_feed") == "newsubscriptions":
			result = self.getNewSubscriptions(params)
		else:
			return

		if len(result) == 0:
			return

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
	
	def getPlayList(self, params = {}):
		get = params.get
		feed = self.urls["playlists"] % get("playlist")
		return self.__core__.listAll(feed, params)
	
	def getDiscoSearch(self, params = {}):
		(result, status) = self.__scraper__.searchDisco(params)
		return result
	
	def getFavorites(self, params = {}):
		get = params.get
		if not get("contact"):
			return
		feed = self.urls["favorites"] % get("contact")  
		return self.__core__.listAll(feed, params)
	
	def getNewSubscriptions(self, params = {}):
		get = params.get
		if not get("contact"):
			return
		feed = self.urls["newsubscriptions"] % get("contact")
		return self.__core__.listAll(feed, params)
	
	def addToPlaylist(self, params = {}):
		get = params.get
		if (not get("playlist")):
			params["user_feed"] = "playlists"
			(result, status) = self.__core__.listAll(params)
			if status == 200:
				list = []
				list.append("New Playlist")
				for item in result:
					list.append(item["Title"])
				dialog = xbmcgui.Dialog()
				selected = dialog.select(self.__language__(30520), ['The','Funsized','Bear'])
				
				if selected == 0:
					self.createPlayList(params)
				elif selected > 0:
					params["playlist"] = result[selected].get("playlist")
					self.__core__.add_to_playlist(self, params)
					self.__utils__.showMessage("Success", "Added to playlist")
					return True
		return False
	
	def createPlayList(self, params = {}):
		get = params.get
		input = self.__utils__.getUserInput("New Playlist")
		
		
		
	def removeFromPlaylist(self, params = {}):
		get = params.get
		
		if get("playlist") and get("videoid"):
			(message, status) = self.__core__.remove_from_playlist(self, params = {})
			
			if (status != 200):
				self.__utils__.showErrorMessage(self.__language__(30023), message, status)