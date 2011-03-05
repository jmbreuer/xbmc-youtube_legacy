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
import os
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import YouTubeCore

core = YouTubeCore.YouTubeCore();

class YouTubePlaylistControl:
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	urls = {};
	urls['playlists'] = "http://gdata.youtube.com/feeds/api/users/%s/playlists"	
	
	def playAll(self, params={}):
		get = params.get
		
		if get("playlistId"):
			self.queuePlayList(params)
			
	def queuePlayList(self, params = {}):
		