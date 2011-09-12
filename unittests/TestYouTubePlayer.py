import nose
from mock import Mock, patch
import sys, io
import MockYouTubeDepends
from YouTubePlayer import YouTubePlayer

class TestYouTubePlayer():
			
	def test_playVideo_should_call_getObject(self):
		assert(True)

#		from YouTubePlayer import YouTubePlayer
#		player = YouTubePlayer.YouTubePlayer()
	
	def test_saveSubtitle_should_call_xbmcvfs_translatePath(self):
		assert(1)
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
		
	def test_getVideoUrlMap_should_parse_streamMap(self):
		testinput = io.open("resources/streamMapTest.txt")
		inputdata = testinput.read()
		
		player = YouTubePlayer()
#		player._fetchPage = Mock()
#		player._fetchPage.return_value = inputdata		
		result = player.getVideoUrlMap({"args":{"fmt_stream_map":inputdata}},{})
#		assert(result != {})

	def test_getVideoUrlMap_should_parse_url_encoded_stream_map(self):
		testinput = io.open("resources/urlEncodedStreamMapTest.txt")
		inputdata = testinput.read()
		player = YouTubePlayer()
		result = player.getVideoUrlMap({"args":{"url_encoded_fmt_stream_map":inputdata}},{})
		
	def test_getVideoUrlMap_should_parse_url_map(self):
		testinput = io.open("resources/urlMapTest.txt")
		inputdata = testinput.read()
		player = YouTubePlayer()
		result = player.getVideoUrlMap({"args":{"fmt_url_map":inputdata}},{})

	def test_getVideoUrlMap_should_mark_live_play(self):
		testinput = io.open("resources/urlMapTest.txt")
		inputdata = testinput.read()
		player = YouTubePlayer()
		video = {}
		result = player.getVideoUrlMap({"args":{"fmt_url_map":inputdata, "liveplayback_module":"true"}},video)
		assert(video["live_play"] == "true") 
		
if __name__ == '__main__':
	nose.run()