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
	
class YouTubeDownloader:	 
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__utils__ = sys.modules[ "__main__" ].__utils__
						
	def downloadVideo(self, params = {}):
		get = params.get
		
		path = self.__settings__.getSetting( "downloadPath" )
		if (not path):
			self.__utils__.showMessage(self.__language__(30600), self.__language__(30611))
			self.__settings__.openSettings()
			path = self.__settings__.getSetting( "downloadPath" )

		( video, status ) = self.__core__.construct_video_url(params)
			
		if status != 200:
			self.showErrorMessage(self.__language__( 30501 ), video, status)
			if self.__dbg__:
				print self.__plugin__ + " downloadVideo got error from construct_video_url: [%s] %s" % ( status, video)
			return False

		item = video.get
		
		self.__utils__.showMessage(self.__language__(30612), self.__utils__.makeAscii(item("Title", "Unknown Title")))
		
		( video, status ) = self.__core__.downloadVideo(video)
				
		if status == 200:
			self.__utils__.showMessage(self.__language__( 30604 ), self.__utils__.makeAscii(item("Title")))