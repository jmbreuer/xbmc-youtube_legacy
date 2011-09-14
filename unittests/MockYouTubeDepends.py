class MockYouTubeDepends:
	common = ""
	def mock(self):
		import sys, string
		from mock import Mock
				
		#Emulate more of XBMC
		sys.modules[ "__main__" ].plugin = "unittest"
		sys.modules[ "__main__" ].dbg = True
		sys.modules[ "__main__" ].dbglevel = 10
		sys.modules[ "__main__" ].settings = Mock()
		sys.modules[ "__main__" ].settings.getAddonInfo = Mock()
		sys.modules[ "__main__" ].settings.getAddonInfo.return_value = "somepath"
		sys.modules[ "__main__" ].language = Mock()
		
		import YouTubeLogin 
		sys.modules[ "__main__" ].login = Mock(spec=YouTubeLogin.YouTubeLogin)
		
		import YouTubeStorage
		sys.modules[ "__main__" ].storage = Mock(spec=YouTubeStorage.YouTubeStorage)

		import CommonFunctions
		sys.modules[ "__main__" ].common = Mock(spec = CommonFunctions.CommonFunctions)
		sys.modules[ "__main__" ].common.log = Mock()
		sys.modules[ "__main__" ].common.USERAGENT = "Mozilla/5.0 (MOCK)"
		
		import YouTubeUtils
		sys.modules[ "__main__" ].utils = Mock(spec=YouTubeUtils.YouTubeUtils)
		sys.modules[ "__main__" ].utils.VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)

		sys.modules[ "__main__" ].cache = Mock()
		
		import YouTubeCore
		sys.modules[ "__main__" ].core = Mock(spec=YouTubeCore.YouTubeCore)
		import YouTubeFeeds
		sys.modules[ "__main__" ].feeds = Mock(spec=YouTubeFeeds.YouTubeFeeds)
		import YouTubeScraper 
		sys.modules[ "__main__" ].scraper = Mock(spec=YouTubeScraper.YouTubeScraper)
		import YouTubePlayer
		sys.modules[ "__main__" ].player = Mock(spec=YouTubePlayer.YouTubePlayer)
		
		sys.modules[ "__main__" ].log_override = self
		sys.modules[ "__main__" ].common.log.side_effect = sys.modules[ "__main__" ].log_override.log

	def log(self, description, level = 0):
		import inspect
		print "[%s] %s : '%s'" % ("YouTube", inspect.stack()[2][3], description) # inspect.stack() is dependent on testcommonfunctions.py
		#print "[%s] %s : '%s'" % ("YouTube", "No inspect", description)
