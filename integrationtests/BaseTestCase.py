import sys
import unittest2, io
from mock import Mock
import MockYouTubeDepends

MockYouTubeDepends.MockYouTubeDepends().mockXBMC()

sys.path.append('../plugin/')
sys.path.append('../xbmc-mocks/')

class BaseTestCase(unittest2.TestCase):
	
	def setUp(self):
		MockYouTubeDepends.MockYouTubeDepends().mock()
		MockYouTubeDepends.MockYouTubeDepends().mockXBMC()
		self.intializePlugin()
		
	def intializePlugin(self):
		import cookielib, urllib2
		sys.modules[ "__main__" ].cookiejar = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(sys.modules[ "__main__" ].cookiejar))
		urllib2.install_opener(opener)
		
		sys.argv = ["something",-1,"something_else"]
		import YouTubeUtils
		sys.modules[ "__main__" ].utils = YouTubeUtils.YouTubeUtils()
		import CommonFunctions
		sys.modules[ "__main__" ].common = CommonFunctions.CommonFunctions() 
		import YouTubeStorage
		sys.modules[ "__main__" ].storage = YouTubeStorage.YouTubeStorage()
		import YouTubeCore
		sys.modules[ "__main__" ].core = YouTubeCore.YouTubeCore()
		import YouTubeLogin 
		sys.modules[ "__main__" ].login = YouTubeLogin.YouTubeLogin()
		import YouTubeFeeds
		sys.modules[ "__main__" ].feeds = YouTubeFeeds.YouTubeFeeds()
		import YouTubeScraper 
		sys.modules[ "__main__" ].scraper = YouTubeScraper.YouTubeScraper()
		import YouTubePlayer
		sys.modules[ "__main__" ].player = YouTubePlayer.YouTubePlayer()
		import YouTubeDownloader
		sys.modules[ "__main__" ].downloader = YouTubeDownloader.YouTubeDownloader()
		import YouTubeScraper
		sys.modules[ "__main__" ].scraper = YouTubeScraper.YouTubeScraper()
		import YouTubePlaylistControl
		sys.modules[ "__main__" ].playlist = YouTubePlaylistControl.YouTubePlaylistControl()
		import YouTubeNavigation
		self.navigation = YouTubeNavigation.YouTubeNavigation()
		
	def assert_directory_count_greater_than_or_equals(self, count):
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		if len(args) < count:
			print "Directory list length %s is not greater than or equal to expected list lengt %s" % (repr(len(args)), repr(count))
		
		assert(len(args) >= count)
	
	def assert_directory_count_less_than_or_equals(self, count):
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		if len(args) > count:
			print "Directory list length %s is not less than or equal to expected list lengt %s" % (repr(len(args)), repr(count))
		
		assert(len(args) <= count)

	def assert_directory_count_equals(self, count):
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		if len(args) != count:
			print "Expected directory list length %s does not match actual list lengt %s" % (repr(count), repr(len(args)))
		
		assert(len(args) == count)
	
	def assert_directory_is_a_video_list(self):
		folder_count = 0
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		for call in args:
			if call[1]["isFolder"] == True:
				folder_count += 1
		
		if folder_count > 1:
			print "Directory is not a video list, it contains %s folders (Max 1 allowed)" % folder_count
			print "Directory list: \r\n" + repr(args)

		assert(folder_count <= 1)
		
	def assert_directory_is_a_folder_list(self):
		video_count = 0
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		for call in args:
			if call[1]["isFolder"] == False:
				video_count += 1
		
		if video_count > 0:
			print "Directory is not a folder list, it contains %s videos" % video_count
			print "Directory list: \r\n" + repr(args)
			
		assert(video_count == 0)
		
	def assert_directory_contains_only_unique_video_items(self):
		video_ids = []
		non_unique = []
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		for call in args:
			url = call[1]["url"]
			if url.find("videoid=") > 0:
				video = url[url.find("videoid=") + len("videoid="):]
				if video.find("&"):
					video = video[:video.find("&")]
				
				if video:
					if video in video_ids:
						non_unique.append(video)
					video_ids.append(video)
		
		if len(non_unique) > 0:
			print "Directory contains one or more duplicate videoids.\r\n Duplicates: %s \r\n Full List: %s" % (repr(non_unique), repr(video_ids)) 
			print "Directory list: \r\n" + repr(args)
			
		assert(len(non_unique) == 0)
	
	def assert_directory_items_should_have_thumbnails(self):
		args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list
		
		missing_thumb_count = 0
		for call in args:
			if call[1]["thumbnailImage"].find("http://") == -1: 
				missing_thumb_count += 1
		
		if missing_thumb_count > 1:
			print "Directory contains more than one item with an invalid thumbnail: " 
			print "List Items: \r\n" + repr(args)
		
		assert(missing_thumb_count <= 1)
		
	def assert_directory_items_should_have_poster_thumbnails(self):
		args = sys.modules["__main__"].xbmcgui.ListItem.call_args_list
		
		missing_poster_count = 0
		for call in args:
			if call[1]["thumbnailImage"].find("poster") == -1: 
				missing_poster_count += 1
		
		if missing_poster_count > 1:
			print "Directory contains more than one item with an invalid thumbnail: " 
			print "List Items: \r\n" + repr(args)
		
		assert(missing_poster_count <= 1)
	
	def assert_directory_should_have_next_folder(self):
		args = sys.modules["__main__"].xbmcplugin.addDirectoryItem.call_args_list
		
		next_folder_count = 0
		
		for call in args:
			if call[1]["url"].find("page=") > 0:
				next_folder_count += 1
		
		if next_folder_count != 1:
			print "Expected Directory Listing to contain a next folder but didn't find any:"
			print "List Items: \r\n" + repr(args)
		assert(next_folder_count == 1)
