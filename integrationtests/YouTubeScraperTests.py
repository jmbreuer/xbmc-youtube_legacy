import MockYouTubeDepends
import unittest
from mock import Mock, patch

class YouTubePlayerTests():
	
	def playVideo_should_call_getObject(self):
		from YouTubePlayer import YouTubePlayer
		player._fetchPage = Mock()
		player._fetchPage.return_value = "smokey"
		player = YouTubePlayer.YouTubePlayer()
		print "smokey"

	def getVideoUrlMap_should_parse_streamMap(self):
		from YouTubePlayer import YouTubePlayer
		player = YouTubePlayer()
		player._fetchPage = Mock()
		player._fetchPage.return_value = "smokey"
		
		player.getVideoUrlMap({"args":{}},{})
		print "more smokey"
		
if __name__ == "__main__":
	testsuite = YouTubePlayerTests()
	testsuite.getVideoUrlMap_should_parse_streamMap()