# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  YouTubeDownloader import YouTubeDownloader 

class TestYouTubeDownloader(BaseTestCase.BaseTestCase):
	
	def test_downloadVideo_should_call_getSetting_to_get_downloadPath(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"apierror":"some_error"},303)
		downloader = YouTubeDownloader()
		downloader.processQueue = Mock()
		
		downloader.downloadVideo({})
		
		sys.modules["__main__"].settings.getSetting.assert_called_with("downloadPath")
		
	def ttest_downloadVideo_should_call_cache_get_lock_to_ensure_no_other_downloaders_are_running(self):
		assert(False)
		
	def ttest_downloadVideo_should_ask_user_for_downloadPath_if_its_missing(self):
		assert(False)
		
	def ttest_downloadVideo_should_only_call_addVideoToDownloadQeueu_if_a_downloader_is_already_running(self):
		assert(False)
		
	def ttest_downloadVideo_should_call_processQueue_if_no_other_downloads_are_running(self):
		assert(False)
		
	def ttest_processQueue_should_call_storage_getNextVideoFromDownloadQueue(self):
		assert(False)
		
	def ttest_processQueue_should_create_a_DownloadProgress_dialog(self):
		assert(False)
		
	def ttest_processQueue_should_call_player_getVideoObject(self):
		assert(False)
		
	def ttest_processQueue_should_show_error_message_if_player_cant_find_video(self):
		assert(False)
		
	def ttest_processQueue_should_remove_video_from_queue_if_player_cant_find_video(self):
		assert(False)
		
	def ttest_processQueue_should_get_new_video_from_queue_if_player_cant_find_video(self):
		assert(False)
		
	def ttest_processQueue_should_show_error_message_if_player_returns_stream_map(self):
		assert(False)
		
	def ttest_processQueue_should_remove_video_from_queue_if_player_returns_stream_map(self):
		assert(False)
		
	def ttest_processQueue_should_get_new_video_from_queue_if_player_returns_stream_map(self):
		assert(False)

	def ttest_processQueue_should_call_downloadVideoURL_if_video_is_found(self):
		assert(False)
		
	def ttest_processQueue_should_call_removeVideoFromDownloadQueue_after_downloading(self):
		assert(False)

	def ttest_processQueue_should_call_getNextVideoFromDownloadQueue_after_downloading(self):
		assert(False)
	
	def ttest_processQueue_should_call_dialog_close_when_processing_is_done(self):
		assert(False)

	def ttest_downloadVideoURL_should_show_error_meesage_if_video_contains_a_rtmpe_stream(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_call_getSetting_to_get_downloadPath(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_call_player_downloadSubtitle(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_user_translate_path_to_find_temp_dir(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_download_file_to_temporary_path(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_move_file_to_download_path_when_finished(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_check_if_file_existins_before_downloading_and_delete_if_it_does(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_call_con_info_getHeader_to_get_file_size(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_call_con_read_with_correct_chunk_size(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_call_sqlGet_to_fetch_download_queue_while_downloading(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_update_download_dialog_with_progress(self):
		assert(False)
		
	def ttest_downloadVideoURL_should_close_connection_and_filehandle_when_done(self):
		assert(False)	
		
	def ttest_downloadVideoURL_should_call_xbmcvfs_rename_to_move_file_to_final_destination(self):
		assert(False)

	def ttest_downloadVideoURL_should_call_storage_storeValue_to_update_vidoe_download_status(self):
		assert(False)

if __name__ == '__main__':
	nose.run()
