import MockYouTubeDepends
import unittest
import sys
from YouTubePlayer import YouTubePlayer
from mock import Mock, patch

class YouTubePlayerTests():
	
	def playVideo_should_call_getObject(self):
		player = YouTubePlayer.YouTubePlayer()
		print "smokey"
	
	def saveSubtitle_should_call_xbmcvfs_rename(self):
		sys.modules["xbmcvfs"].translatePath = Mock()
		sys.modules["xbmcvfs"].translatePath.return_value = "testFilePath" 
		player = YouTubePlayer()
		player.saveSubtitle({},{"Title":"testTitle","downloadPath":"testPath"})
		assert(sys.modules["xbmcvfs"].recieved())
		
	def getVideoUrlMap_should_parse_streamMap(self):
		player = YouTubePlayer()
		player._fetchPage = Mock()
		player._fetchPage.return_value = "smokey"
		
		player.getVideoUrlMap({"args":{}},{})
		print "more smokey"
		
if __name__ == "__main__":
	testsuite = YouTubePlayerTests()
	#testsuite.getVideoUrlMap_should_parse_streamMap()
	testsuite.saveSubtitle_should_call_xbmcvfs_rename()