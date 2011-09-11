import MockYouTubeDepends
import unittest2
import sys
from YouTubePlayer import YouTubePlayer
from mock import Mock, patch

class YouTubePlayerTests(unittest2.TestCase):
#class YouTubePlayerTests():
		
	def playVideo_should_call_getObject(self):
		player = YouTubePlayer.YouTubePlayer()
	
	def test_saveSubtitle_should_call_xbmcvfs_translatePath(self):
		sys.modules["xbmcvfs"].translatePath = Mock()
		sys.modules["xbmcvfs"].translatePath.return_value = "tempFilePath" 
		player = YouTubePlayer()
		player.saveSubtitle("my_subtitle_stream",{"Title":"testTitle","videoid":"someVideoId","downloadPath":"downloadFilePath"})
		sys.modules["xbmcvfs"].translatePath.assert_called_with("special://temp")
		
	
	def test_saveSubtitle_should_call_xbmcvfs_rename(self):
		sys.modules["xbmcvfs"].translatePath = Mock()
		sys.modules["xbmcvfs"].translatePath.return_value = "tempFilePath" 
		player = YouTubePlayer()
		player.saveSubtitle("my_subtitle_stream",{"Title":"testTitle","videoid":"someVideoId","downloadPath":"downloadFilePath"})
		sys.modules["xbmcvfs"].rename.assert_called_with("tempFilePath/testTitle-[someVideoId].ssa","downloadFilePath/testTitle-[someVideoId].ssa")
		
	def getVideoUrlMap_should_parse_streamMap(self):
		player = YouTubePlayer()
		player._fetchPage = Mock()
		player._fetchPage.return_value = "smokey"
		
		player.getVideoUrlMap({"args":{}},{})
		
if __name__ == "__main__":
#	suite = YouTubePlayerTests()
#	suite.test_saveSubtitle_should_call_xbmcvfs_rename()
#	suite.test_saveSubtitle_should_call_xbmcvfs_translatePath()
	unittest2.main()