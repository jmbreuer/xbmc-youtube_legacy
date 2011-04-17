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

import sys, urllib2, os
	
class YouTubeDownloader:	 
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__player__ = sys.modules["__main__" ].__player__
	__utils__ = sys.modules[ "__main__" ].__utils__
						
	def downloadVideo(self, params = {}):
		get = params.get
		
		path = self.__settings__.getSetting( "downloadPath" )
		if (not path):
			self.__utils__.showMessage(self.__language__(30600), self.__language__(30611))
			self.__settings__.openSettings()
			path = self.__settings__.getSetting( "downloadPath" )
		
		( video, status ) = self.__player__.construct_video_url(params)
			
		if status != 200:
			self.showErrorMessage(self.__language__( 30501 ), video, status)
			if self.__dbg__:
				print self.__plugin__ + " downloadVideo got error from construct_video_url: [%s] %s" % ( status, video)
			return False

		item = video.get
		
		self.__utils__.showMessage(self.__language__(30612), self.__utils__.makeAscii(item("Title", "Unknown Title")))
		
		( video, status ) = self._downloadVideo(video)
				
		if status == 200:
			self.__utils__.showMessage(self.__language__( 30604 ), self.__utils__.makeAscii(item("Title")))
			
	def _downloadVideo(self, video):
		if self.__dbg__:
			print self.__plugin__ + " downloadVideo : " + video['Title']
			
		path = self.__settings__.getSetting( "downloadPath" )
		try:
			url = urllib2.Request(video['video_url'])
			url.add_header('User-Agent', self.USERAGENT);
			valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
			
			filename_incomplete = "%s/%s-incomplete.mp4" % ( path, ''.join(c for c in video['Title'] if c in valid_chars) )
			filename_complete = "%s/%s.mp4" % ( path, ''.join(c for c in video['Title'] if c in valid_chars) )
			file = open(filename_incomplete, "wb")
			con = urllib2.urlopen(url);
			file.write(con.read())
			con.close()
			
			os.rename(filename_incomplete, filename_complete)
			
			self.__settings__.setSetting( "vidstatus-" + video['videoid'], "1" )
		except urllib2.HTTPError, e:
			if self.__dbg__:
				print self.__plugin__ + " downloadVideo except: " + str(e)
			return ( str(e), 303 )
		except:
			if self.__dbg__:
				print self.__plugin__ + " downloadVideo uncaught exception"
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__, sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				
			return (self.__language__(30606), 303)

		if self.__dbg__:
			print self.__plugin__ + " downloadVideo done"
		return ( video, 200 )
