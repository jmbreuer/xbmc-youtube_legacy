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
		
	def test_downloadVideo_should_lock_cache_to_ensure_no_other_downloaders_are_running(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"apierror":"some_error"},303)
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].cache.lock.return_value = False
		downloader = YouTubeDownloader()
		downloader.processQueue = Mock()
		
		downloader.downloadVideo({})
		
		sys.modules["__main__"].cache.lock.assert_called_with("YouTubeDownloadLock")
		
	def test_downloadVideo_should_ask_user_for_downloadPath_if_its_missing(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"apierror":"some_error"},303)
		sys.modules["__main__"].settings.getSetting.return_value = ""
		sys.modules["__main__"].language.return_value = "my_message" 
		sys.modules["__main__"].cache.lock.return_value = False
		downloader = YouTubeDownloader()
		downloader.processQueue = Mock()
		
		downloader.downloadVideo({})
		
		sys.modules["__main__"].utils.showMessage.assert_called_with("my_message","my_message")
		sys.modules["__main__"].settings.openSettings.assert_called_with()
		
	def test_downloadVideo_should_just_call_addVideoToDownloadQueue_if_a_downloader_is_already_running(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"apierror":"some_error"},303)
		sys.modules["__main__"].settings.getSetting.return_value = ""
		sys.modules["__main__"].language.return_value = "my_message" 
		sys.modules["__main__"].cache.lock.return_value = False
		downloader = YouTubeDownloader()
		downloader.processQueue = Mock()
		
		downloader.downloadVideo({})
		
		sys.modules["__main__"].storage.addVideoToDownloadQueue.assert_called_with({})
		assert(downloader.processQueue.call_count == 0)
		
	def test_downloadVideo_should_call_processQueue_if_no_other_downloads_are_running(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"apierror":"some_error"},303)
		sys.modules["__main__"].settings.getSetting.return_value = ""
		sys.modules["__main__"].language.return_value = "my_message" 
		sys.modules["__main__"].cache.lock.return_value = True
		downloader = YouTubeDownloader()
		downloader.processQueue = Mock()
		
		downloader.downloadVideo({})
		
		sys.modules["__main__"].storage.addVideoToDownloadQueue.assert_called_with({'silent': 'true'})
		downloader.processQueue.assert_called_once_with({'silent': 'true'})
		
	def test_downloadVideo_should_unlock_cache_when_done(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"apierror":"some_error"},303)
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].cache.lock.return_value = True
		downloader = YouTubeDownloader()
		downloader.processQueue = Mock()
		
		downloader.downloadVideo({})
		
		sys.modules["__main__"].cache.unlock.assert_called_with("YouTubeDownloadLock")
		
	def test_processQueue_should_call_storage_getNextVideoFromDownloadQueue(self):
		sys.modules["__main__"].player.getVideoObject.return_value = ({"videoid":"some_id","Title":"sometitle"},200)
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		videoids = [""]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()  
		downloader = YouTubeDownloader()
		downloader.dialog = "some_dialog"
		
		downloader.processQueue({})
		
		assert(sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.call_count == 1)
		
	def test_processQueue_should_create_a_DownloadProgress_dialog(self):				
		video = ({"videoid":"some_id", "Title":"sometitle"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		sys.modules["DialogDownloadProgress"].DownloadProgress.assert_called_with()
		
	def test_processQueue_should_call_player_getVideoObject(self):
		video = ({"videoid":"some_id", "Title":"sometitle"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		sys.modules["__main__"].player.getVideoObject.assert_called_with({"videoid":"some_id"})
		
	def test_processQueue_should_show_error_message_if_player_cant_find_video(self):
		video = ({"apierror":"some_error"}, 303)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		assert(downloader.downloadVideoURL.call_count == 0)
		sys.modules["__main__"].utils.showMessage.assert_called_with("my_string","some_error")
		sys.modules["__main__"].language.assert_called_with(30625)
		
	def test_processQueue_should_remove_video_from_queue_if_player_cant_find_video(self):
		video = ({"apierror":"some_error"}, 303)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		assert(downloader.downloadVideoURL.call_count == 0)
		assert(sys.modules["__main__"].storage.removeVideoFromDownloadQueue.call_args[0][0] == "some_id")
		assert(sys.modules["__main__"].storage.removeVideoFromDownloadQueue.call_count == 1)
		
	def test_processQueue_should_get_new_video_from_queue_if_player_cant_find_video(self):
		video = ({"apierror":"some_error"}, 303)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		assert(downloader.downloadVideoURL.call_count == 0)
		assert(sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.call_count == 2)
		
	def test_processQueue_should_show_error_message_if_player_returns_stream_map(self):
		video = ({"videoid":"some_id","Title":"some_title", "stream_map":"some_map"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		args = sys.modules["__main__"].language.call_args_list 
		args = args[len(args)-2:]
		assert(args[0][0][0] == 30607)
		assert(args[1][0][0] == 30619)
		assert(downloader.downloadVideoURL.call_count == 0)
		sys.modules["__main__"].utils.showMessage.assert_called_with("my_string","my_string")
	
	def test_processQueue_should_remove_video_from_queue_if_player_returns_stream_map(self):
		video = ({"videoid":"some_id","Title":"some_title", "stream_map":"some_map"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		assert(downloader.downloadVideoURL.call_count == 0)
		assert(sys.modules["__main__"].storage.removeVideoFromDownloadQueue.call_args[0][0] == "some_id")
		assert(sys.modules["__main__"].storage.removeVideoFromDownloadQueue.call_count == 1)
		
	def test_processQueue_should_get_new_video_from_queue_if_player_returns_stream_map(self):
		video = ({"videoid":"some_id","Title":"some_title", "stream_map":"some_map"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		assert(downloader.downloadVideoURL.call_count == 0)
		assert(sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.call_count == 2)

	def test_processQueue_should_call_downloadVideoURL_if_video_is_found(self):
		video = ({"videoid":"some_id","Title":"some_title"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		downloader.downloadVideoURL.assert_called_with(video[0])
		
	def test_processQueue_should_call_removeVideoFromDownloadQueue_after_downloading(self):
		video = ({"videoid":"some_id","Title":"some_title"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		downloader.downloadVideoURL.assert_called_with(video[0])
		assert(sys.modules["__main__"].storage.removeVideoFromDownloadQueue.call_args[0][0] == "some_id")
		assert(sys.modules["__main__"].storage.removeVideoFromDownloadQueue.call_count == 1)

	def test_processQueue_should_call_getNextVideoFromDownloadQueue_after_downloading(self):
		video = ({"videoid":"some_id","Title":"some_title"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "my_string"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		downloader.downloadVideoURL.assert_called_with(video[0])
		assert(sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.call_count == 2)
	
	def test_processQueue_should_call_dialog_close_when_processing_is_done(self):
		video = ({"videoid":"some_id", "Title":"sometitle"}, 200)
		sys.modules["__main__"].player.getVideoObject.return_value = video 
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		videoids = ["","some_id"]
		sys.modules["__main__"].storage.getNextVideoFromDownloadQueue.side_effect = lambda: videoids.pop()
		
		downloader = YouTubeDownloader()
		downloader.dialog = ""
		downloader.downloadVideoURL = Mock()
		downloader.downloadVideoURL.return_value = video
		
		downloader.processQueue()
		
		sys.modules["DialogDownloadProgress"].DownloadProgress().close.assert_called_with()
	
	def test_downloadVideoURL_should_show_error_meesage_if_video_contains_a_rtmpe_stream(self):
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"		
		downloader = YouTubeDownloader()
		
		downloader.downloadVideoURL({"videoid":"someid", "video_url":"some url with swfurl", "Title":"some_title"})
		
		args = sys.modules["__main__"].language.call_args_list 
		args = args[len(args)-2:]
		assert(args[0][0][0] == 30625)
		assert(args[1][0][0] == 30619)
		sys.modules["__main__"].utils.showMessage.assert_called_with("some_message","some_message")		
		
	def test_downloadVideoURL_should_call_getSetting_to_get_downloadPath(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		
		downloader.downloadVideoURL({"videoid":"someid", "video_url":"some_url", "Title":"some_title"})

		url_patcher.stop()
		sys.modules["__main__"].settings.getSetting.assert_called_with("downloadPath")
		
	def test_downloadVideoURL_should_call_player_downloadSubtitle(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		sys.modules["__main__"].player.downloadSubtitle.assert_called_with(input)
		assert(input.has_key("downloadPath"))
		
	def test_downloadVideoURL_should_use_translate_path_to_find_temp_dir(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		sys.modules["__main__"].xbmc.translatePath.assert_called_with('special://temp')
		
	def test_downloadVideoURL_should_download_file_to_temporary_path(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		sys.modules["__main__"].xbmc.translatePath.return_value = "some_temporary_path"
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		sys.modules["__main__"].xbmc.translatePath.assert_called_with('special://temp')
		sys.modules["__main__"].storage.openFile.assert_called_with('some_temporary_path/some_title-[someid].mp4', 'wb')
		
	def test_downloadVideoURL_should_move_file_to_download_path_when_finished(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		sys.modules["__main__"].xbmc.translatePath.return_value = "some_temporary_path"
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		sys.modules["__main__"].xbmcvfs.rename.assert_called_with('some_temporary_path/some_title-[someid].mp4', 'mypath/some_title-[someid].mp4')
		
	def test_downloadVideoURL_should_check_if_file_existins_before_downloading_and_delete_if_it_does(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		sys.modules["__main__"].xbmcvfs.exists.return_value = True
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		sys.modules["__main__"].xbmcvfs.exists.assert_called_with('mypath/some_title-[someid].mp4')
		sys.modules["__main__"].xbmcvfs.delete.assert_called_with('mypath/some_title-[someid].mp4')
		
	def test_downloadVideoURL_should_call_con_info_getHeader_to_get_file_size(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		dummy_connection.info().getheader.assert_called_with("Content-Length")
		
	def test_downloadVideoURL_should_call_con_read_with_correct_chunk_size(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		print repr(dummy_connection.call_count)
		dummy_connection.read.assert_called_with(5)
	
	def test_downloadVideoURL_should_call_read_until_stream_is_empty(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		chunks = ["","1","2","3","4","5"]
		dummy_connection.read.side_effect = lambda x: chunks.pop()
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		assert(dummy_connection.read.call_count == 6)
		dummy_connection.read.assert_called_with(5)
		
	def test_downloadVideoURL_should_call_sqlGet_to_fetch_download_queue_while_downloading(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		sys.modules["__main__"].cache.sqlGet.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		
		sys.modules["__main__"].cache.sqlGet.assert_called_with("YouTubeDownloadQueue")
	
	def test_downloadVideoURL_should_calculate_progress_correctly(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		sys.modules["__main__"].cache.sqlGet.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		
		sys.modules["__main__"].cache.sqlGet.assert_called_with("YouTubeDownloadQueue")
		
	def test_downloadVideoURL_should_update_download_dialog_with_progress(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()
		chunk = "12345"
		chunks = ["", chunk, chunk, chunk, chunk]		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.side_effect = lambda x: chunks.pop()
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		sys.modules["__main__"].cache.sqlGet.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		
		assert(downloader.dialog.update.call_args_list[0][1]["percent"] == 0)
		assert(downloader.dialog.update.call_args_list[1][1]["percent"] == 1)
		assert(downloader.dialog.update.call_args_list[2][1]["percent"] == 1)
		assert(downloader.dialog.update.call_args_list[3][1]["percent"] == 2)
		assert(downloader.dialog.update.call_args_list[4][1]["percent"] == 2)
		
	def test_downloadVideoURL_should_close_connection_and_filehandle_when_done(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		sys.modules["__main__"].cache.sqlGet.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		
		dummy_connection.close.assert_called_with()
		sys.modules["__main__"].storage.openFile().close.assert_called_with()	
		
	def test_downloadVideoURL_should_call_xbmcvfs_rename_to_move_file_to_final_destination(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		sys.modules["__main__"].cache.sqlGet.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
		
		assert(sys.modules["__main__"].xbmcvfs.rename.call_count == 1)

	def test_downloadVideoURL_should_call_storage_storeValue_to_update_vidoe_download_status(self):
		url_patcher = patch("urllib2.urlopen")
		url_patcher.start()		
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = ""
		dummy_connection.geturl.return_value = ""
		dummy_connection.info().getheader.return_value = "1000"
		sys.modules["__main__"].cache.sqlGet.return_value = ""
		url_patcher(urllib2.urlopen).return_value = dummy_connection
		sys.modules["__main__"].settings.getSetting.return_value = "mypath"
		sys.modules["__main__"].language.return_value = "some_message"
		downloader = YouTubeDownloader()
		downloader.dialog = Mock()
		input = {"videoid":"someid", "video_url":"some_url", "Title":"some_title"}
		
		downloader.downloadVideoURL(input)
		
		url_patcher.stop()
				
		sys.modules["__main__"].storage.storeValue.assert_called_with('vidstatus-someid', '1')

if __name__ == '__main__':
	nose.run()
