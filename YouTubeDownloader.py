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

import sys, urllib2, os, time, math
from DialogDownloadProgress import DownloadProgress
	
class YouTubeDownloader:	 
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__player__ = sys.modules["__main__" ].__player__
	__utils__ = sys.modules[ "__main__" ].__utils__
	__storage__ = sys.modules[ "__main__" ].__storage__
						
	def downloadVideo(self, params = {}):
		get = params.get
		
		path = self.__settings__.getSetting( "downloadPath" )
		if (not path):
			self.__utils__.showMessage(self.__language__(30600), self.__language__(30611))
			self.__settings__.openSettings()
			path = self.__settings__.getSetting( "downloadPath" )
		
		
		scan = DownloadProgress()
		if scan.active:
			self.__storage__.addVideoToDownloadQeueu(params)
		else:
			params["silent"] = "true"
			self.__storage__.addVideoToDownloadQeueu(params)
			self.processQueue(params)		
		
	def processQueue(self, params):
		
		videoid = self.__storage__.getNextVideoFromDownloadQueue()
		
		while videoid:
			params["videoid"] = videoid
			( video, status ) = self.__player__.getVideoObject(params)
			if status != 200:
				self.__utils__.showMessage(self.__language__(30625), video["apierror"])
				self.__storage__.removeVideoFromDownloadQueue(videoid)
				videoid = self.__storage__.getNextVideoFromDownloadQueue()
				continue
			item = video.get
			if item("stream_map"):
				self.__utils__.showMessage(self.__language__(30632), self.__language__("30626"))
				self.__storage__.removeVideoFromDownloadQueue(videoid)
				videoid = self.__storage__.getNextVideoFromDownloadQueue()
				continue
				
			( video, status ) = self.downloadVideoURL(video)
			self.__storage__.removeVideoFromDownloadQueue(videoid)
			videoid = self.__storage__.getNextVideoFromDownloadQueue()
			
	def downloadVideoURL(self, video, params = {}):
		if self.__dbg__:
			print self.__plugin__ + " downloadVideo : " + video['Title']
		
		if video["video_url"].find("swfurl") > 0:
			self.__utils__.showMessage(self.__language__( 30625 ), self.__language__(30626))
			return ([], 303)
		
		path = self.__settings__.getSetting( "downloadPath" )
		self.__player__.downloadSubtitle(video) 
		url = urllib2.Request(video['video_url'])
		url.add_header('User-Agent', self.__utils__.USERAGENT);
		
		filename_incomplete = "%s/%s-[%s]-incomplete.mp4" % ( path, ''.join(c for c in video['Title'] if c in self.__utils__.VALID_CHARS), video["videoid"] )
		filename_complete = "%s/%s-[%s].mp4" % ( path, ''.join(c for c in video['Title'] if c in self.__utils__.VALID_CHARS), video["videoid"] )
			
		file = open(filename_incomplete, "wb")
		con = urllib2.urlopen(url);
		total_size = 8192 * 25
		
		if con.info().getheader('Content-Length').strip():			
			total_size = int(con.info().getheader('Content-Length').strip())
			
		chunk_size = int(total_size / 25)
		
		try:
			scan = DownloadProgress()
			scan.create( heading = self.__language__( 30624 ), label = video["Title"])
			bytes_so_far = 0
			chunk_size = 8192
			
			while 1:
				chunk = con.read(chunk_size)
				bytes_so_far += len(chunk)
				percent = int(float(bytes_so_far) / float(total_size) * 100)
				file.write(chunk)
				heading = self.__language__(30624) + " - " + str(percent) + "%"
				scan.update(percent=percent, heading = heading)
				if not chunk:
					break
			
			con.close()
			scan.close()
		except:
			print self.__plugin__ + " download failed unknown reason"
			try:
				scan.close()
			except:
				print self.__plugin__ + " failed to close download dialog"
		
		os.rename(filename_incomplete, filename_complete)
		
		self.__settings__.setSetting( "vidstatus-" + video['videoid'], "1" )
		return ( video, 200 )