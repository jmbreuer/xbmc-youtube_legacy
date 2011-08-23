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
from DialogDownloadProgress import DownloadProgress
import YouTubeUtils
import xbmc
try: import xbmcvfs
except ImportError: import xbmcvfsdummy as xbmcvfs
import StorageServer

class YouTubeDownloader(YouTubeUtils.YouTubeUtils):
	__settings__ = sys.modules[ "__main__" ].__settings__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__"].__plugin__	
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	
	__player__ = sys.modules["__main__" ].__player__
	__storage__ = sys.modules[ "__main__" ].__storage__

        __storage_server__ = StorageServer.StorageServer()
	__storage_server__.__table_name__ = "YouTube"

	dialog = ""

	def downloadVideo(self, params = {}):
		get = params.get
		
		path = self.__settings__.getSetting( "downloadPath" )
		if (not path):
			self.showMessage(self.__language__(30600), self.__language__(30611))
			self.__settings__.openSettings()
			self.__dbg__ = self.__settings__.getSetting("debug") == "true"
			path = self.__settings__.getSetting( "downloadPath" )

		if self.__storage_server__.lock("YouTubeDownloadLock"):
			params["silent"] = "true"
			if self.__plugin__:
				print self.__plugin__ + " Downloader not active, initializing downloader"
			
			self.__storage__.addVideoToDownloadQeueu(params)
			self.processQueue(params)
			self.__storage_server__.unlock("YouTubeDownloadLock")
		else:
			if self.__dbg__:
				print self.__plugin__ + " Downloader is active, Queueing video "
			self.__storage__.addVideoToDownloadQeueu(params)

	def processQueue(self, params = {}):
		videoid = self.__storage__.getNextVideoFromDownloadQueue()
		
		if videoid:
			if not self.dialog:
				self.dialog = DownloadProgress()
			#self.dialog.create( heading = self.__language__( 30605 ), label = "")
	
			while videoid:
				params["videoid"] = videoid
				( video, status ) = self.__player__.getVideoObject(params)
				if status != 200:
					self.showMessage(self.__language__(30625), video["apierror"])
					self.__storage__.removeVideoFromDownloadQueue(videoid)
					videoid = self.__storage__.getNextVideoFromDownloadQueue()
					continue
				item = video.get
				if item("stream_map"):
					self.showMessage(self.__language__(30607), self.__language__(30619))
					self.__storage__.removeVideoFromDownloadQueue(videoid)
					videoid = self.__storage__.getNextVideoFromDownloadQueue()
					continue
				
				( video, status ) = self.downloadVideoURL(video)
				self.__storage__.removeVideoFromDownloadQueue(videoid)
				videoid = self.__storage__.getNextVideoFromDownloadQueue()

			print self.__plugin__  +  " Finished download queue."
			self.dialog.close()
			self.dialog = ""

			#self.__lock__.release()

			
	def downloadVideoURL(self, video, params = {}):
		if self.__dbg__:
			print self.__plugin__ + " downloadVideo: " + video['Title']
		
		if video["video_url"].find("swfurl") > 0:
			self.showMessage(self.__language__( 30625 ), self.__language__(30619))
			return ([], 303)
		
		video["downloadPath"] = self.__settings__.getSetting( "downloadPath" )
		self.__player__.downloadSubtitle(video) 
		url = urllib2.Request(video['video_url'])
		url.add_header('User-Agent', self.USERAGENT);
		filename = "%s-[%s].mp4" % ( ''.join(c for c in video['Title'] if c in self.VALID_CHARS), video["videoid"] )
		filename_incomplete = os.path.join(xbmc.translatePath( "special://temp" ), filename )
		filename_complete = os.path.join(self.__settings__.getSetting( "downloadPath" ), filename )

		if xbmcvfs.exists(filename_complete):
			xbmcvfs.delete(filename_complete)

		file = open(filename_incomplete, "wb")
		con = urllib2.urlopen(url);

		total_size = 8192 * 25
		chunk_size = 8192
		
		if con.info().getheader('Content-Length').strip():			
			total_size = int(con.info().getheader('Content-Length').strip())	
			chunk_size = int(total_size / 200) # We only want 200 updates of the status bar.
		try:
			bytes_so_far = 0
			
			videos = []
			while 1:
				chunk = con.read(chunk_size)
				bytes_so_far += len(chunk)
				percent = int(float(bytes_so_far) / float(total_size) * 100)
				file.write(chunk)
				
				queue = self.__storage__.sqlGet("YouTubeDownloadQueue")

				if queue:
					try:
						videos = eval(queue)
					except:
						videos = []
				else:
					videos = []

				heading = "[%s] %s - %s%%" % ( str(len(videos)), self.__language__(30624), str(percent))
				self.dialog.update(percent=percent, heading = heading, label=video["Title"])

				if not chunk:
					break
			
			con.close()
			file.close()
		except:
			try:
				con.close()
				file.close()
			except:
				print self.__plugin__ + " downloadVideoURL - Failed to close download stream and file handle"	
		
		xbmcvfs.rename(filename_incomplete, filename_complete)
		self.dialog.update(heading = self.__language__(30604), label=video["Title"])
		self.__storage__.storeValue( "vidstatus-" + video['videoid'], "1" )
		return ( video, 200 )
