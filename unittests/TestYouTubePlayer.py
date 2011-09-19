import nose
import BaseTestCase
from mock import Mock, patch
import sys, io
from YouTubePlayer import YouTubePlayer

class TestYouTubePlayer(BaseTestCase.BaseTestCase):
	
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
		
		assert(len(result) == 11)
		keys = [5, 18, 22, 34, 35, 37, 43, 44, 45, 82, 84]
		for key in keys:
			assert(key in result)

	def test_getVideoUrlMap_should_mark_live_play(self):
		player = YouTubePlayer()
		video = {}
		
		result = player.getVideoUrlMap(self.readTestInput("liveStreamTest.txt"),video)
		
		assert(video["live_play"] == "true")
		assert(len(result) == 1)
		assert(result.has_key(34)) 
				
	def test_downloadSubtitle_should_call_transformSubtitleToSSA(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"nothingness"}
	
		subtitlesettings = ["false","0","true"]
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = lambda x: subtitlesettings.pop()
		player.transformAnnotationToSSA = Mock()
		player.transformAnnotationToSSA.return_value = ("", "style")
		player.downloadSubtitle()
		
		player.transformAnnotationToSSA.assert_called_with("nothingness")
	
	def test_downloadSubtitle_should_call_saveSubtitle(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"nothingness"}
		subtitlesettings = ["false","0","true"]
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = lambda x: subtitlesettings.pop()
		player.transformAnnotationToSSA = Mock()
		player.transformAnnotationToSSA.return_value = ("something", "style")
		player.saveSubtitle = Mock()
		
		result = player.downloadSubtitle()
		
		assert (result == True)
		assert (player.saveSubtitle.called)
		
	def test_downloadSubtitle_should_call_getSubtitleUrl(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"nothingness"}
	
		subtitlesettings = ["false","2","true"]
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = lambda x: subtitlesettings.pop()
		player.transformAnnotationToSSA = Mock()
		player.transformAnnotationToSSA.return_value = ("", "style")
		player.getSubtitleUrl = Mock()
		player.getSubtitleUrl.return_value = ""
		
		player.downloadSubtitle()
		
		player.getSubtitleUrl.assert_called_with({})
	
	def test_downloadSubtitle_should_call_getTranscriptionUrl(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"nothingness"}
		subtitlesettings = ["true","2","true"]
			
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = lambda x: subtitlesettings.pop()
		player.transformAnnotationToSSA = Mock()
		player.transformAnnotationToSSA.return_value = ("", "style")
		player.getSubtitleUrl = Mock()
		player.getSubtitleUrl.return_value = ""
		player.getTranscriptionUrl = Mock()
		player.getTranscriptionUrl.return_value = ""
		
		player.downloadSubtitle()
		
		player.getTranscriptionUrl.assert_called_with({})
		
	def test_downloadSubtitle_should_call_transformSubtitleXMLtoSRT(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"nothingness"}
	
		subtitlesettings = ["true","2","true"]
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = lambda x: subtitlesettings.pop()
		player.transformAnnotationToSSA = Mock()
		player.transformAnnotationToSSA.return_value = ("", "style")
		player.getSubtitleUrl = Mock()
		player.getSubtitleUrl.return_value = ""
		player.getTranscriptionUrl = Mock()
		player.getTranscriptionUrl.return_value = "something"
		player.transformSubtitleXMLtoSRT = Mock()
		player.transformSubtitleXMLtoSRT.return_value = ""
		
		player.downloadSubtitle()
		
		player.transformSubtitleXMLtoSRT.assert_called_with("nothingness")
		
	def test_downloadSubtitle_should_exit_gracefully_if_subtitles_and_annotations_are_disabled(self):
		player = YouTubePlayer()
	
		subtitlessettings = ["false","0","false"]
		def popSetting(self, *args, **kwargs):			
			val = subtitlessettings.pop()
			return val
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = popSetting
		
		result = player.downloadSubtitle()
		
		assert(result == False)

	def test_getSubtitleUrl_should_call_fetchPage_with_correct_url(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":303, "content":""}
		
		player.getSubtitleUrl({"videoid":"some_id"})
		
		sys.modules[ "__main__"].core._fetchPage.assert_called_with({"link":player.urls["timed_text_index"] % ('some_id')}) 
		
	def test_getSubtitleUrl_should_find_url_with_proper_language_code(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":self.readTestInput("timedtextDirectoryTest.xml", False).encode("utf-8")}
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.return_value = "3"
		
		url = player.getSubtitleUrl({"videoid":"some_id"})
		
		assert(url.find("lang=de") > 0)

	def test_getSubtitleUrl_should_fall_back_to_english_if_proper_language_code_is_not_found(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":self.readTestInput("timedtextDirectoryTest.xml", False).encode("utf-8")}
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.return_value = "2"
		
		url = player.getSubtitleUrl({"videoid":"some_id"})
		
		assert(url.find("lang=en") > 0)
			
	def test_transformSubtitleXMLtoSRT_should_parse_youtube_subtitle_xml(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].utils.replaceHtmlCodes = Mock()
		sys.modules[ "__main__"].utils.replaceHtmlCodes.side_effect = lambda x: x.encode("ascii", 'ignore')
		
		result = player.transformSubtitleXMLtoSRT(self.readTestInput("subtitleTest.xml",False).encode("utf-8")) 
		
		assert(len(result.split("\r\n")) == 66) 
		
	def test_transformSubtitleXMLtoSRT_should_call_replaceHtmlCodes_for_user_visible_text(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].utils.replaceHtmlCodes = Mock()
		sys.modules[ "__main__"].utils.replaceHtmlCodes.side_effect = lambda x: x.encode("ascii", 'ignore')
		
		result = player.transformSubtitleXMLtoSRT(self.readTestInput("subtitleTest.xml",False).encode("utf-8")) 
		
		assert(sys.modules[ "__main__"].utils.replaceHtmlCodes.call_count > 0) 
	
	def test_transformSubtitleXMLtoSRT_should_correctly_find_start_time_for_text_elements(self):
		input = '<?xml version="1.0" encoding="utf-8" ?><transcript>\n\
				<text start="14.017" dur="2.07">first</text>\n\
				<text start="16.087" dur="2.996">second</text>\n\
				</transcript>'
		player = YouTubePlayer()
		sys.modules[ "__main__"].utils.replaceHtmlCodes = Mock()
		sys.modules[ "__main__"].utils.replaceHtmlCodes.side_effect = lambda x: x.encode("ascii", 'ignore')
		
		result = player.transformSubtitleXMLtoSRT(input).split("\r\n")

		assert(result[0].find("Marked=0,0:00:14.017") > 0)
		assert(result[1].find("Marked=0,0:00:16.087") > 0)
		
	def test_transformSubtitleXMLtoSRT_should_correctly_recalculate_duration_time_for_text_elements(self):
		input = '<?xml version="1.0" encoding="utf-8" ?><transcript>\n\
				<text start="14.017" dur="2.07">first</text>\n\
				<text start="16.087" dur="2.996">second</text>\n\
				</transcript>'
		player = YouTubePlayer()
		sys.modules[ "__main__"].utils.replaceHtmlCodes = Mock()
		sys.modules[ "__main__"].utils.replaceHtmlCodes.side_effect = lambda x: x.encode("ascii", 'ignore')
		
		result = player.transformSubtitleXMLtoSRT(input).split("\r\n")
				
		assert(result[0].find("0:00:16.087,Default") > 0)
		assert(result[1].find("0:00:19.083,Default") > 0)
				
	def test_transformAnnotationToSSA_should_parse_youtube_annotations_xml(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].utils.replaceHtmlCodes = Mock()
		sys.modules[ "__main__"].utils.replaceHtmlCodes.side_effect = lambda x: x.encode("ascii", 'ignore')
		
		(result, style) = player.transformAnnotationToSSA(self.readTestInput("annotationsTest.xml",False).encode("utf-8")) 
		
		assert(len(result.split("\r\n")) == 6)
	
	def test_transformAnnotationToSSA_should_call_replaceHtmlCodes_for_user_visible_text(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].utils.replaceHtmlCodes = Mock()
		sys.modules[ "__main__"].utils.replaceHtmlCodes.side_effect = lambda x: x.encode("ascii", 'ignore')
		
		result = player.transformAnnotationToSSA(self.readTestInput("annotationsTest.xml",False).encode("utf-8")) 
		
		assert(sys.modules[ "__main__"].utils.replaceHtmlCodes.call_count > 0)
	
	def test_addSubtitles_should_call_downloadSubtitle(self):
		player = YouTubePlayer()
		
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "testDownloadPath"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = False
		player.downloadSubtitle = Mock()
		player.downloadSubtitle.return_value = False
		
		player.addSubtitles({"videoid":"testid","Title":"testTitle"})
		
		player.downloadSubtitle.assert_called_with({"videoid":"testid","Title":"testTitle"})
	
	def test_addSubtitles_should_check_if_subtitle_exists_locally_before_calling_downloadSubtitle(self):
		player = YouTubePlayer()
		
		settings =[False, True]
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "testDownloadPath"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.side_effect = lambda x: settings.pop()
		player.downloadSubtitle = Mock()
		player.downloadSubtitle.return_value = False
		
		player.addSubtitles({"videoid":"testid","Title":"testTitle"})
		
		sys.modules["xbmcvfs"].exists.assert_called_with('testDownloadPath/testTitle-[testid].ssa')
		assert(player.downloadSubtitle.call_count == 0)
	
	def test_addSubtitles_should_call_xbmcs_setSubtitles(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "testDownloadPath"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = True
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].Player().setSubtitles = Mock()
		player.downloadSubtitle = Mock()
		player.downloadSubtitle.return_value = True
		
		player.addSubtitles({"videoid":"testid","Title":"testTitle"})
		
		sys.modules["xbmcvfs"].exists.assert_called_with('testDownloadPath/testTitle-[testid].ssa')
		sys.modules["xbmc"].Player().setSubtitles.assert_called_with('testDownloadPath/testTitle-[testid].ssa')		
	
	def test_addSubtitles_should_check_if_subtitle_exists_locally_before_calling_xbmcs_setSubtitles(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "testDownloadPath"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = True
		player.downloadSubtitle = Mock()
		player.downloadSubtitle.return_value = False
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].Player().setSubtitles = Mock()
		
		player.addSubtitles({"videoid":"testid","Title":"testTitle"})
		
		sys.modules["xbmcvfs"].exists.assert_called_with('testDownloadPath/testTitle-[testid].ssa')
		assert(player.downloadSubtitle.call_count == 0)
		sys.modules["xbmc"].Player().setSubtitles.assert_called_with('testDownloadPath/testTitle-[testid].ssa')	
		
	def test_addSubtitles_should_wait_for_playback_to_start_before_adding_subtitle(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "testDownloadPath"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = True
		sys.modules["xbmc"].Player = Mock()
		sys.modules["xbmc"].Player().setSubtitles = Mock()
		player.addSubtitles({"videoid":"testid","Title":"testTitle"})
		
		sys.modules["xbmc"].Player().isPlaying.assert_called_with()
		sys.modules["xbmc"].Player().setSubtitles.assert_called_with('testDownloadPath/testTitle-[testid].ssa')	
		
	def test_playVideo_should_call_getVideoObject(self):
		player = YouTubePlayer()
		player.getVideoObject = Mock(return_value = [{"apierror":"some error"},303]) 
		
		player.playVideo()
		
		player.getVideoObject.assert_called_with({})
	
	def test_playVideo_should_log_and_fail_gracefully_on_apierror(self):
		player = YouTubePlayer()
		player.getVideoObject = Mock()
		player.getVideoObject.return_value = [{"apierror":"some error"},303]
		
		result = player.playVideo()
		
		assert(result == False)
		sys.modules[ "__main__" ].common.log.assert_called_with("construct video url failed contents of video item {'apierror': 'some error'}")

	def test_playVideo_should_call_xbmc_setResolvedUrl(self):
		player = YouTubePlayer()
		player.getVideoObject = Mock()
		player.getVideoObject.return_value = ({"Title":"someTitle","videoid":"some_id", "thumbnail":"someThumbnail", "video_url":"someUrl"}, 200)
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["xbmcplugin"].setResolvedUrl = Mock()
		sys.modules["xbmc"].ListItem = Mock()
		sys.argv = ["test1","1","test2"]
		player.addSubtitles = Mock()
		
		player.playVideo({"videoid":"some_id"})
		
		assert(sys.modules["xbmcplugin"].setResolvedUrl.call_count > 0)
		
		
	def test_playVideo_should_call_addSubtitles(self):
		player = YouTubePlayer()
		player.getVideoObject = Mock()
		video = {"Title":"someTitle","videoid":"some_id", "thumbnail":"someThumbnail", "video_url":"someUrl"}
		player.getVideoObject.return_value = (video, 200)
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		sys.modules["xbmcplugin"].setResolvedUrl = Mock()
		sys.modules["xbmc"].ListItem = Mock()
		sys.argv = ["test1","1","test2"]
		player.addSubtitles = Mock()
		
		player.playVideo({"videoid":"some_id"})
		
		player.addSubtitles.assert_called_with(video)
	
	def test_playVideo_should_call_remove_from_playlist_if_viewing_video_from_watch_later_queue(self):
		player = YouTubePlayer()
		player.getVideoObject = Mock()
		player.getVideoObject.return_value = ({"Title":"someTitle","videoid":"some_id", "thumbnail":"someThumbnail", "video_url":"someUrl"}, 200)
		sys.modules["__main__"].settings.getSetting = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["xbmcplugin"].setResolvedUrl = Mock()
		sys.modules["xbmc"].ListItem = Mock()
		sys.modules["__main__"].core.remove_from_playlist = Mock() 
		sys.argv = ["test1","1","test2"]
		player.addSubtitles = Mock()
		call_params = {"videoid":"some_id", "watch_later":"true","playlist":"playlist_id","playlist_entry_id":"entry_id"}
		
		player.playVideo(call_params)
		
		sys.modules["__main__"].core.remove_from_playlist.assert_called_with(call_params)
		
	def test_playVideo_should_update_locally_stored_watched_status(self):
		player = YouTubePlayer()
		player.getVideoObject = Mock()
		player.getVideoObject.return_value = ({"Title":"someTitle","videoid":"some_id", "thumbnail":"someThumbnail", "video_url":"someUrl"}, 200)
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["xbmcplugin"].setResolvedUrl = Mock()
		sys.modules["xbmc"].ListItem = Mock()
		sys.argv = ["test1","1","test2"]
		player.addSubtitles = Mock()
		
		player.playVideo({"videoid":"some_id"})
		sys.modules["__main__"].storage.storeValue.assert_called_with("vidstatus-some_id", "7" )


	def test_getInfo_should_use_cache_when_possible(self):
		player = YouTubePlayer()
		sys.modules["__main__"].cache.sqlGet.return_value = '["something"]'
		
		player.getInfo({"videoid":"some_id"})
		
		sys.modules["__main__"].cache.sqlGet.assert_called_with("videoidcachesome_id")
		
	def test_getInfo_should_call_fetchPage_with_correct_url(self):
		player = YouTubePlayer()
		sys.modules["__main__"].cache.sqlGet.return_value = {}
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":303, "content":"something"}
		
		player.getInfo({"videoid":"some_id"})
		
		sys.modules[ "__main__"].core._fetchPage.assert_called_with({"api":"true","link":player.urls["video_info"] % ("some_id")})
		
	def test_getInfo_should_call_core_getVideoInfo_to_parse_youtube_xml(self):
		player = YouTubePlayer()
		sys.modules["__main__"].cache.sqlGet.return_value = {}
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"something"}
		sys.modules["__main__"].core.getVideoInfo.return_value = [{"videoid":"some_id"}]
		
		player.getInfo({"videoid":"some_id"})
		
		sys.modules[ "__main__"].core.getVideoInfo.assert_called_with("something",{"videoid":"some_id"})
	
	def test_getInfo_should_fail_correctly_if_api_is_unavailable(self):
		player = YouTubePlayer()
		sys.modules["__main__"].cache.sqlGet.return_value = {}
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"something"}
		sys.modules["__main__"].core.getVideoInfo.return_value = []
		sys.modules["__main__"].language.return_value = "some_string"
		
		(video, status) = player.getInfo({"videoid":"some_id"})
		
		sys.modules["__main__"].common.log.assert_called_with("- Couldn't parse API output, YouTube doesn't seem to know this video id?")
		sys.modules["__main__"].language.assert_called_with(30608)
		assert(video["apierror"] == "some_string")
				
	def test_getInfo_should_save_video_info_in_cache(self):
		player = YouTubePlayer()
		sys.modules["__main__"].cache.sqlGet.return_value = {}
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"something"}
		sys.modules["__main__"].core.getVideoInfo.return_value = [{"videoid":"some_id"}]
		
		(video, status) = player.getInfo({"videoid":"some_id"})
		
		sys.modules["__main__"].cache.sqlSet.assert_called_with('videoidcachesome_id', "{'videoid': 'some_id'}")

	def test_selectVideoQuality_should_prefer_h264_over_vp8_for_720p_as_appletv2_cant_handle_vp8_properly(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "2"
		
		url = player.selectVideoQuality({22:"h264",45:"vp8"},{})
		
		assert(url == "h264 | Mozilla/5.0 (MOCK)")
		
	def test_selectVideoQuality_should_choose_highest_sd_quality_if_only_multiple_sd_qualities_are_available(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		
		url = player.selectVideoQuality({5:"1",33:"2",18:"3",26:"4",43:"5",34:"6",78:"7",44:"8",59:"9",35:"10"},{})
		
		assert(url == "10 | Mozilla/5.0 (MOCK)")
			
	def test_selectVideoQuality_should_prefer_1080p_if_user_has_selected_that_option(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "3"
		
		url = player.selectVideoQuality({35:"SD",22:"720p",37:"1080p"},{})
		
		assert(url == "1080p | Mozilla/5.0 (MOCK)")
		
	def test_selectVideoQuality_should_limit_to_720p_if_user_has_selected_that_option(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "2"
		
		url = player.selectVideoQuality({35:"SD",22:"720p",37:"1080p"},{})
		
		assert(url == "720p | Mozilla/5.0 (MOCK)")
		
	def test_selectVideoQuality_should_limit_to_sd_if_user_has_selected_that_option(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		
		url = player.selectVideoQuality({35:"SD",22:"720p",37:"1080p"},{})
		
		assert(url == "SD | Mozilla/5.0 (MOCK)")
		
	def test_selectVideoQuality_should_call_userSelectsVideoQuality_if_user_selected_that_option(self):
		player = YouTubePlayer()
		player.userSelectsVideoQuality = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		
		player.selectVideoQuality({35:"SD",22:"720p",37:"1080p"},{})
		
		player.userSelectsVideoQuality.assert_called_with({}, {35: 'SD', 37: '1080p', 22: '720p'})
		
	def test_selectVideoQuality_should_add_user_agent_when_not_called_by_download_function(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		
		url = player.selectVideoQuality({35:"SD",22:"720p",37:"1080p"},{})
		
		assert(url.find("| Mozilla/5.0 (MOCK)") > 0)
		
	def test_selectVideoQuality_should_not_add_user_agent_when_called_by_download_function(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		
		url = player.selectVideoQuality({35:"SD",22:"720p",37:"1080p"},{"action":"download"})
		
		assert(url.find("| Mozilla/5.0 (MOCK)") < 0)
	
	
	def test_userSelectsVideoQuality_should_append_list_of_known_qualities(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		sys.modules["xbmcgui"].Dialog = Mock()
		sys.modules["xbmcgui"].Dialog().select.return_value = -1
		sys.modules["__main__"].language.return_value = "" 
		
		url = player.userSelectsVideoQuality({},{35:"SD",22:"720p",37:"1080p"})
		
		sys.modules["xbmcgui"].Dialog().select.assert_called_with("",["1080p","720p","480p"])
		
	def test_userSelectsVideoQuality_should_prefer_h264_over_vp8_as_appletv2_cant_handle_vp8_properly(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		sys.modules["xbmcgui"].Dialog = Mock()
		sys.modules["xbmcgui"].Dialog().select.return_value = 0
		sys.modules["__main__"].language.return_value = "" 
		
		url = player.userSelectsVideoQuality({},{22:"h264",45:"vp8"})
		
		assert(url == "h264")
		
	def test_userSelectsVideoQuality_should_select_proper_quality_based_on_user_input(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		sys.modules["xbmcgui"].Dialog = Mock()
		sys.modules["xbmcgui"].Dialog().select.return_value = 0
		sys.modules["__main__"].language.return_value = "" 
		
		url = player.userSelectsVideoQuality({},{35:"SD",22:"720p",37:"1080p"})
		
		sys.modules["xbmcgui"].Dialog().select.assert_called_with("",["1080p","720p","480p"])
		assert(url == "1080p")
	
	def test_userSelectsVideoQuality_should_call_xbmc_dialog_select_to_ask_for_user_input(self):
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		sys.modules["xbmcgui"].Dialog = Mock()
		sys.modules["xbmcgui"].Dialog().select.return_value = -1
		sys.modules["__main__"].language.return_value = "" 
		
		url = player.userSelectsVideoQuality({},{35:"SD",22:"720p",37:"1080p"})
		
		assert(sys.modules["xbmcgui"].Dialog().select.call_count > 0)
	
	def test_getVideoObject_should_get_video_information_from_getInfo(self):
		player = YouTubePlayer()
		player.getInfo = Mock()
		player.getInfo.return_value = ({},303)
		player._getVideoLinks = Mock()
		player._getVideoLinks.return_value = ({},{})
		
		player.getVideoObject({})
		
		player.getInfo.assert_called_with({})
		
	def test_getVideoObject_should_test_if_local_file_exists_if_download_path_is_set(self):
		params = {"videoid":"some_id"}
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = False
		player.getInfo = Mock()
		player.getInfo.return_value = ({"videoid":"some_id","Title":"someTitle"},200)
		player._getVideoLinks = Mock()
		player._getVideoLinks.return_value = ({},{})
		
		player.getVideoObject(params)
		
		sys.modules["xbmcvfs"].exists.assert_called_with("somePath/someTitle-[some_id].mp4")
		
	def test_getVideoObject_should_use_local_file_for_playback_if_found(self):
		params = {"videoid":"some_id"}
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = True
		player.getInfo = Mock()
		player.getInfo.return_value = ({"videoid":"some_id","Title":"someTitle"},200)
		player._getVideoLinks = Mock()
		player._getVideoLinks.return_value = ({},{})
		
		(video, status) = player.getVideoObject(params)
		
		sys.modules["xbmcvfs"].exists.assert_called_with("somePath/someTitle-[some_id].mp4")
		assert(player._getVideoLinks.call_count == 0)
		assert(video["video_url"] == "somePath/someTitle-[some_id].mp4")
		
	def test_getVideoObject_should_call_getVideoLinks_if_local_file_not_found(self):
		params = {"videoid":"some_id"}
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = False
		player.getInfo = Mock()
		player.getInfo.return_value = ({"videoid":"some_id","Title":"someTitle"},200)
		player._getVideoLinks = Mock()
		player._getVideoLinks.return_value = ({},{})
		
		(video, status) = player.getVideoObject(params)
		
		sys.modules["xbmcvfs"].exists.assert_called_with("somePath/someTitle-[some_id].mp4")
		assert(player._getVideoLinks.call_count > 0)
		
	def test_getVideoObject_should_call_selectVideoQuality_if_local_file_not_found_and_remote_links_found(self):
		params = {"videoid":"some_id"}
		player = YouTubePlayer()
		sys.modules["__main__"].settings.getSetting.return_value = "somePath/"
		sys.modules["xbmcvfs"].exists = Mock()
		sys.modules["xbmcvfs"].exists.return_value = False
		player.getInfo = Mock()
		player.getInfo.return_value = ({"videoid":"some_id","Title":"someTitle"},200)
		player._getVideoLinks = Mock()
		player._getVideoLinks.return_value = ({22:"720p"},{})
		player.selectVideoQuality = Mock()
		
		(video, status) = player.getVideoObject(params)
		
		sys.modules["xbmcvfs"].exists.assert_called_with("somePath/someTitle-[some_id].mp4")
		player.selectVideoQuality.assert_called_with({22:"720p"},params)
		assert(player._getVideoLinks.call_count > 0)
	
	def test_getVideoObject_should_use_pre_defined_error_messages_on_missing_url(self):
		player = YouTubePlayer()
		player.getInfo = Mock()
		player.getInfo.return_value = ({},303)
		player._getVideoLinks = Mock()
		player._getVideoLinks.return_value = ({},{})
		
		player.getVideoObject({})
		
		player.getInfo.assert_called_with({})
		sys.modules["__main__"].language.assert_called_with(30618)
	
	def test_convertFlashVars_should_parse_html_properly(self):
		player = YouTubePlayer()
		
		result = player._convertFlashVars(self.readTestInput("flashVarsTest.html", False))
		
		assert(len(result["PLAYER_CONFIG"]["args"]) == 77)		
	
	def test_getVideoLinks_should_try_scraping_first(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"something"}
		sys.modules[ "__main__"].common.parseDOM.return_value = ""
		
		player._getVideoLinks({},{"videoid":"some_id"})
		
		sys.modules[ "__main__"].core._fetchPage.assert_called_with({"link": player.urls["video_stream"] % ("some_id")})
		
	def test_getVideoLinks_should_fall_back_to_embed(self):
		player = YouTubePlayer()
		
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":303, "content":"something"}
		
		player._getVideoLinks({},{"videoid":"some_id"})
		
		sys.modules[ "__main__"].core._fetchPage.assert_called_with({"link": player.urls["embed_stream"] % ("some_id")})

if __name__ == '__main__':
	nose.run()
