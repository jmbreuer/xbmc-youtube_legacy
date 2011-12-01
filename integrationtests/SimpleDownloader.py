'''
   Simple Downloader plugin for XBMC
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

import sys, urllib2, os, xbmcaddon
#import DialogDownloadProgress

class SimpleDownloader():
	dialog = ""
	def __init__(self):
		self.plugin = "SimpleDownloader-0.8"

		self.INVALID_CHARS = "\\/:*?\"<>|"

		if sys.modules[ "__main__" ].common:
			self.common = sys.modules[ "__main__" ].common
		else:
			import CommonFunctions
			common = CommonFunctions.CommonFunctions()
			common.plugin = self.plugin

		if sys.modules[ "__main__" ].cache:
			self.cache = sys.modules[ "__main__" ].cache
		else:
			try:
				import StorageServer
			except:
				import storageserverdummy as StorageServer
			self.cache = StorageServer.StorageServer()
			self.cache.table_name = "Downloader"

                if sys.modules[ "__main__" ].xbmc:
                        self.xbmc = sys.modules["__main__"].xbmc
                else:
                        import xbmc
                        self.xbmc = xbmc

                if sys.modules[ "__main__" ].xbmcvfs:
                        self.xbmcvfs = sys.modules["__main__"].xbmcvfs
                else:
			try:
				import xbmcvfs
			except ImportError:
				import xbmcvfsdummy as xbmcvfs				
                        self.xbmcvfs = xbmcvfs


		try:
			self.DialogDownloadProgress = sys.modules[ "__main__" ].DialogDownloadProgress
		except:
			import DialogDownloadProgress
			self.DialogDownloadProgress = DialogDownloadProgress

		if sys.modules[ "__main__" ].dbglevel:
                        self.dbglevel = sys.modules[ "__main__" ].dbglevel
		else:
                        self.dbglevel = 3

		if sys.modules[ "__main__" ].dbg:
			self.dbg = sys.modules[ "__main__" ].dbg
		else:
			self.dbg = True

		try:
			self.settings = xbmcaddon.Addon(id='script.module.simple.downloader')
		except:
			if hasattr(sys.modules[ "__main__" ], "settings"):
				self.settings = sys.modules[ "__main__" ].settings

		self.language = self.settings.getLocalizedString
		self.download_path = self.settings.getSetting( "downloadPath" )
		self.hide_during_playback = self.settings.getSetting( "hideDuringPlayback" ) == "true"
		self.notification_length = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][int(self.settings.getSetting( 'notification_length' ))]
		
		if hasattr(sys.modules[ "__main__" ], "settings"):
			inherited_settings = sys.modules[ "__main__" ].settings
			if inherited_settings.getSetting( "downloadPath" ):
				self.download_path = inherited_settings.getSetting( "downloadPath" )
			if inherited_settings.getSetting( "hideDuringPlayback" ):
				self.hide_during_playback = inherited_settings.getSetting( "hideDuringPlayback" ) == "true"
			if inherited_settings.getSetting( "notification_length" ):
				self.notification_length = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][int(inherited_settings.getSetting( 'notification_length' ))]

		if sys.modules[ "__main__" ].plugin:
			self.plugin = sys.modules[ "__main__" ].plugin
	
	def downloadVideo(self, params = {}):
		self.common.log("")
		get = params.get
		
		if (not self.download_path):
			self.showMessage(self.language(30600), self.language(30611))
			self.settings.openSettings()
			self.dbg = self.settings.getSetting("debug") == "true"
			self.download_path = self.settings.getSetting( "downloadPath" )

		if self.cache.lock("SimpleDownloaderLock"):
			params["silent"] = "true"
			self.common.log("Downloader not active, initializing downloader.")
			
			self.addVideoToDownloadQueue(params)
			self.processQueue(params)
			self.cache.unlock("SimpleDownloaderLock")
		else:
			self.common.log("Downloader is active, Queueing video.")
			self.addVideoToDownloadQueue(params)

	def processQueue(self, params = {}):
		self.common.log("")
		video = self.getNextVideoFromDownloadQueue()
		
		if video:
			if not self.dialog:
				self.dialog = self.DialogDownloadProgress.DownloadProgress()
				self.dialog.hide_during_playback = self.hide_during_playback

			while video:
				params["videoid"] = video['videoid']
				if not video.has_key("video_url") and video.has_key("callback_for_url"):
					( video, status ) = video['callback_for_url'](params)

				if not video.has_key("video_url"):
					if video.has_key("apierror"):
						self.showMessage(self.language(30625), video["apierror"])
					else:
						self.showMessage(self.language(30625), "ERROR")
					self.removeVideoFromDownloadQueue(video['videoid'])
					video = self.getNextVideoFromDownloadQueue()
					continue

				if video.has_key("stream_map"):
					self.showMessage(self.language(30607), self.language(30619))
					self.removeVideoFromDownloadQueue(video['videoid'])
					video = self.getNextVideoFromDownloadQueue()
					continue

				( video, status ) = self.downloadVideoURL(video)
				self.removeVideoFromDownloadQueue(video['videoid'])
				video = self.getNextVideoFromDownloadQueue()

			self.common.log("Finished download queue.")
			self.dialog.close()
			self.dialog = ""
			
	def downloadVideoURL(self, video, params = {}):
		self.common.log(video['Title'])
		
		if video["video_url"].find("swfurl") > 0:
			self.showMessage(self.language( 30625 ), self.language(30619))
			return ([], 303)
		
		video["downloadPath"] = self.download_path

		url = urllib2.Request(video['video_url'])
		url.add_header('User-Agent', self.common.USERAGENT);
		filename = "%s-[%s].mp4" % ( ''.join(c for c in video['Title'].decode("utf-8") if c not in self.INVALID_CHARS), video["videoid"] )
		filename_incomplete = os.path.join(self.xbmc.translatePath( "special://temp" ).decode("utf-8"), "incomplete-" + filename )
		filename_complete = os.path.join(self.download_path.decode("utf-8"), filename)

		if self.xbmcvfs.exists(filename_complete):
			self.xbmcvfs.delete(filename_complete)

		file = self.common.openFile(filename_incomplete, "wb")
		con = urllib2.urlopen(url);

		total_size = 8192 * 25
		chunk_size = 8192

		if con.info().getheader('Content-Length').strip():			
			total_size = int(con.info().getheader('Content-Length').strip())	
			chunk_size = int(total_size / 200) # We only want 200 updates of the status bar.
			if chunk_size < 100:
				chunk_size = 100
		try:
			bytes_so_far = 0
			
			videos = {}
			while 1:
				chunk = con.read(chunk_size)
				bytes_so_far += len(chunk)
				percent = int(float(bytes_so_far) / float(total_size) * 100)
				file.write(chunk)
				
				queue = self.cache.get("SimpleDownloaderQueue")

				if queue:
					try:
						videos = eval(queue)
					except:
						videos = {}
				else:
					videos = {}
				
				heading = "[%s] %s - %s%%" % ( str(len(videos)), self.language(30624), str(percent))
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
				self.common.log("Failed to close download stream and file handle")
		
		self.common.log(filename_incomplete)
		self.common.log(filename_complete)
		self.xbmcvfs.rename(filename_incomplete, filename_complete)
		self.dialog.update(heading = self.language(30604), label=video["Title"])

		if video.has_key("callback_for_done"):
			video['callback_for_done'](video)

		self.common.log("done")
		return ( video, 200 )

		
	#============================= Download Queue =================================
	def getNextVideoFromDownloadQueue(self):
		if self.cache.lock("SimpleDownloaderQueueLock"):
			videos = {}
			
			queue = self.cache.get("SimpleDownloaderQueue")
			self.common.log("queue loaded : " + repr(queue))
			
			if queue:
				try:
					videos = eval(queue)
				except: 
					videos = {}
		
			videoid = ""
			params = {}
			if videos:
				videoid, params = videos.popitem()

			self.cache.unlock("SimpleDownloaderQueueLock")
			self.common.log("getNextVideoFromDownloadQueue released. returning : " + videoid)
			return params
		else:
			self.common.log("getNextVideoFromDownloadQueue Exception")

	def addVideoToDownloadQueue(self, params = {}):
		if self.cache.lock("SimpleDownloaderQueueLock"):
			get = params.get

			videos = {}
			if get("videoid"):
				queue = self.cache.get("SimpleDownloaderQueue")
				self.common.log("queue loaded : " + repr(queue))

				if queue:
					try:
						videos = eval(queue)
					except:
						videos = {}
		
				if get("videoid") not in videos.keys():
					videos[get("videoid")] = params
					
					self.cache.set("SimpleDownloaderQueue", repr(videos))
					self.common.log("Added: " + get("videoid") + " to: " + repr(videos))

			self.cache.unlock("SimpleDownloaderQueueLock")
			self.common.log("addVideoToDownloadQueue released")
		else:
			self.common.log("addVideoToDownloadQueue Exception")
		
	def removeVideoFromDownloadQueue(self, videoid):
		if self.cache.lock("SimpleDownloaderQueueLock"):
			videos = {}
			
			queue = self.cache.get("SimpleDownloaderQueue")
			self.common.log("queue loaded : " + repr(queue))
			if queue:
				try:
					videos = eval(queue)
				except:
					videos = {}
		
			if videoid in videos.keys():
				del videos[videoid]

				self.cache.set("SimpleDownloaderQueue", repr(videos))
				self.common.log("Removed: " + videoid + " from: " + repr(videos))
			else:
				self.common.log("Didn't remove: " + videoid + " from: " + repr(videos))

			self.cache.unlock("SimpleDownloaderQueueLock")
			self.common.log("removeVideoFromDownloadQueue released")
		else:
			self.common.log("removeVideoFromDownloadQueue Exception")

	# Shows a more user-friendly notification
        def showMessage(self, heading, message):
                self.xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % ( heading, message, self.notification_length) )

