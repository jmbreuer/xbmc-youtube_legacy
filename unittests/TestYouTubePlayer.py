import nose
from mock import Mock, patch
import sys, io
import MockYouTubeDepends
from YouTubePlayer import YouTubePlayer

class TestYouTubePlayer():
		
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
	
	def test_getVideoUrlMap_should_return_empty_dictionary_on_missing_map(self):
		player = YouTubePlayer()
		
		result = player.getVideoUrlMap({"args":{}},{})
		
		assert(result == {})
	
	def test_getVideoUrlMap_should_parse_streamMap(self):
		player = YouTubePlayer()
		
		result = player.getVideoUrlMap(self.readTestInput("streamMapTest.txt"),{})
		
		assert(len(result) == 11)
		keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
		for key in keys:
			assert(key in result)
		
	def test_getVideoUrlMap_should_parse_url_encoded_stream_map(self):
		player = YouTubePlayer()
		result = player.getVideoUrlMap(self.readTestInput("urlEncodedStreamMapTest.txt"),{})
		assert(len(result) == 11)
		keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
		for key in keys:
			assert(key in result)

		
	def test_getVideoUrlMap_should_parse_url_map(self):
		player = YouTubePlayer()
		result = player.getVideoUrlMap(self.readTestInput("urlMapTest.txt"),{})

	def test_getVideoUrlMap_should_mark_live_play(self):
		player = YouTubePlayer()
		video = {}
		
		result = player.getVideoUrlMap(self.readTestInput("liveStreamTest.txt"),video)
		
		assert(video["live_play"] == "true")
		assert(len(result) == 1)
		assert(result.has_key(34)) 
	
	def test_playVideo_should_call_getObject(self):
		player = YouTubePlayer()
		player.playVideo()
		assert(True)

	def readTestInput(self, filename, should_eval = True):
		testinput = io.open("resources/" + filename)
		inputdata = testinput.read()
		if should_eval:
			inputdata = eval(inputdata)
		return inputdata
	
if __name__ == '__main__':
	nose.run()