import nose
import BaseTestCase
from mock import Mock, patch
import sys, io
import MockYouTubeDepends
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
	
		subtitlessettings = ["false","0","true"]
		def popSetting(self, *args, **kwargs):			
			val = subtitlessettings.pop()
			return val
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = popSetting
		player.transformAnnotationToSSA = Mock()
		player.transformAnnotationToSSA.return_value = ("", "style")
		player.downloadSubtitle()
		
		player.transformAnnotationToSSA.assert_called_with("nothingness")
	
	def test_downloadSubtitle_should_call_saveSubtitle(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":200, "content":"nothingness"}
	
		subtitlessettings = ["false","0","true"]
		def popSetting(self, *args, **kwargs):			
			val = subtitlessettings.pop()
			return val
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = popSetting
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
	
		subtitlessettings = ["false","2","true"]
		def popSetting(self, *args, **kwargs):			
			val = subtitlessettings.pop()
			return val
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = popSetting
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
	
		subtitlessettings = ["true","2","true"]
		def popSetting(self, *args, **kwargs):			
			val = subtitlessettings.pop()
			return val
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = popSetting
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
	
		subtitlessettings = ["true","2","true"]
		def popSetting(self, *args, **kwargs):			
			val = subtitlessettings.pop()
			return val
		
		sys.modules[ "__main__"].settings.getSetting = Mock()
		sys.modules[ "__main__"].settings.getSetting.side_effect = popSetting
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
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":303, "content":""}
		
		player.getSubtitleUrl({"videoid":"some_id"})
		
		assert(False) 

	def test_getSubtitleUrl_should_fall_back_to_english_if_proper_language_code_is_not_found(self):
		player = YouTubePlayer()
		sys.modules[ "__main__"].core._fetchPage = Mock()
		sys.modules[ "__main__"].core._fetchPage.return_value = {"status":303, "content":""}
		
		player.getSubtitleUrl({"videoid":"some_id"})
		assert(False)
			
	def test_transformSubtitleXMLtoSRT_should_parse_youtube_subtitle_xml(self):
		assert(False)
		
	def test_transformSubtitleXMLtoSRT_should_call_replaceHtmlCodes_for_user_visible_text(self):
		assert(False)
	
	def test_transformSubtitleXMLtoSRT_should_correctly_find_start_time_for_text_elements(self):
		assert(False)
		
	def test_transformSubtitleXMLtoSRT_should_correctly_recalculate_duration_time_for_text_elements(self):
		assert(False)
		
	def test_transformAnnotationToSSA_should_parse_youtube_annotations_xml(self):
		assert(False)
	
	def test_transformAnnotationToSSA_should_call_replaceHtmlCodes_for_user_visible_text(self):
		assert(False)
	
	def test_addSubtitles_should_call_downloadSubtitle(self):
		assert(False)
	
	def test_addSubtitles_should_check_if_subtitle_exists_locally_before_calling_downloadSubtitle(self):
		assert(False)
	
	def test_addSubtitles_should_call_xbmcs_setSubtitles(self):
		assert(False)
	
	def test_addSubtitles_should_check_if_subtitle_exists_locally_before_calling_xbmcs_setSubtitles(self):
		assert(False)
		
	def test_addSubtitles_should_wait_for_playback_to_start_before_adding_subtitle(self):
		assert(False)
		
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
		assert(False)
		
	def test_playVideo_should_call_addSubtitles(self):
		assert(False)
	
	def test_playVideo_should_call_remove_from_playlist_if_viewing_video_from_watch_later_queue(self):
		assert(False)
		
	def test_playVideo_should_update_locally_stored_watched_status(self):
		assert(False)
	
	def test_getInfo_should_use_cache_when_possible(self):
		assert(False)
		
	def test_getInfo_should_call_fetchPage_with_correct_url(self):
		assert(False)
		
	def test_getInfo_should_call_core_getVideoInfo_to_parse_youtube_xml(self):
		assert(False)
	
	def test_getInfo_should_fail_correctly_if_api_is_unavailable(self):
		assert(False)
		
	def test_getInfo_should_save_video_info_in_cache(self):
		assert(False)
		
	def test_selectVideoQuality_should_prefer_h264_over_vp8_as_appletv2_cant_handle_vp8_properly(self):
		assert(False)
		
	def test_selectVideoQuality_should_choose_highest_sd_quality_if_only_multiple_sd_qualities_are_available(self):
		assert(False)
	
	def test_selectVideoQuality_should_prefer_1080p_if_user_has_selected_that_option(self):
		assert(False)
		
	def test_selectVideoQuality_should_limit_to_720p_if_user_has_selected_that_option(self):
		assert(False)
		
	def test_selectVideoQuality_should_limit_to_sd_if_user_has_selected_that_option(self):
		assert(False)
		
	def test_selectVideoQuality_should_call_userSelectsVideoQuality_if_user_selected_that_option(self):
		assert(False)
		
	def test_selectVideoQuality_should_add_user_agent_when_not_called_by_download_function(self):
		assert(False)
		
	def test_selectVideoQuality_should_not_add_user_agent_when_called_by_download_function(self):
		assert(False)
		
	def test_userSelectsVideoQuality_should_append_list_of_known_qualities(self):
		assert(False)
		
	def test_userSelectsVideoQuality_should_prefer_h264_over_vp8_as_appletv2_cant_handle_vp8_properly(self):
		assert(False)
		
	def test_userSelectsVideoQuality_should_select_proper_quality_based_on_user_input(self):
		assert(False)
	
	def test_userSelectsVideoQuality_should_call_xbmc_dialog_select_to_ask_for_user_input(self):
		assert(False)
		
	def test_getVideoObject_should_get_video_information_from_getInfo(self):
		assert(False)
		
	def test_getVideoObject_should_test_if_local_file_exists_if_download_path_is_set(self):
		assert(False)
		
	def test_getVideoObject_should_use_local_file_for_playback_if_found(self):
		assert(False)
		
	def test_getVideoObject_should_call_getVideoLinks_if_local_file_not_found(self):
		assert(False)
		
	def test_getVideoObject_should_call_selectVideoQuality_if_local_file_not_found_and_remote_links_found(self):
		assert(False)
	
	def test_getVideoObject_should_use_pre_defined_error_messages_on_missing_url(self):
		assert(False)
		
	def test_convertFlashVars_should_parse_html_properly(self):
		assert(False)
	
	def test_getVideoLinks_should_try_scraping_first(self):
		assert(False)
		
	def test_getVideoLinks_should_fall_back_to_embed(self):
		assert(False)
		
if __name__ == '__main__':
	nose.run()
