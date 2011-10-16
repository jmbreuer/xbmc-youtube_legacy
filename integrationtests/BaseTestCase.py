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