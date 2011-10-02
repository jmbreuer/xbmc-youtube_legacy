import nose
import BaseTestCase
from mock import Mock, patch
import sys
from YouTubeFeeds import YouTubeFeeds

class TestYouTubeFeeds(BaseTestCase.BaseTestCase):
	def test_createUrl_should_call_getSetting_to_get_videos_pr_page(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		feeds.createUrl()
		
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("perpage")

	def test_createUrl_should_call_getSetting_to_get_region_id(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		feeds.createUrl()
		
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("region_id")

	def test_createUrl_should_get_correct_feed_url_if_feed_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"favorites"})
		result = result[:result.find("?")]
		url = feeds.urls["favorites"] % ("default")
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("region_id")
		assert( result == url)

	def test_createUrl_should_get_correct_user_feed_url_if_user_feed_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"user_feed":"favorites"})
		result = result[:result.find("?")]
		url = feeds.urls["favorites"] % ("default")
		assert( result == url)
		
	def test_createUrl_should_get_correct_search_url_if_search_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"search":"some_search"})
		result = result[:result.find("moderate") + 8]
		url = feeds.urls["search"] % ("some_search","moderate")
		assert( result == url)
		
	def test_createUrl_should_add_contact_name_to_url_if_contact_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"favorites", "contact":"some_contact"})
		
		result = result[:result.find("?")]
		url = feeds.urls["favorites"] % ("some_contact")
		assert( result == url)

	def test_createUrl_should_add_channel_to_url_if_channel_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"favorites", "channel":"some_channel"})
		
		result = result[:result.find("?")]
		url = feeds.urls["favorites"] % ("some_channel")
		assert( result == url)
	
	def test_createUrl_should_add_playlist_to_url_if_playlist_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"playlist", "channel":"some_playlist"})
		
		result = result[:result.find("?")]
		url = feeds.urls["playlist"] % ("some_playlist")
		assert( result == url)

	def test_createUrl_should_add_videoid_to_url_if_videoid_is_in_params(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"related", "videoid":"some_videoid"})
		
		result = result[:result.find("?")]
		url = feeds.urls["related"] % ("some_videoid")
		assert( result == url)

	def test_createUrl_should_add_region_if_standard_feed(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"feed_linked"})
		
		result = result[:result.find("?")]
		assert( result.find("standardfeeds/AU/") > 0)

	def test_createUrl_should_start_index_and_max_results_for_non_folder_non_play_all_feeds(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"feed_linked"})
		
		result = result[result.find("?"):]
		assert( result == "?time=this_week&start-index=1&max-results=15")
	
	def test_createUrl_should_add_time_if_url_contains_time_param(self):
		sys.modules[ "__main__" ].settings.getSetting.return_value = "1"
		feeds = YouTubeFeeds()
		
		result = feeds.createUrl({"feed":"feed_linked"})
		
		assert(result.find("?time=this_week") > 0)
	
	def test_list_should_call_listFolder_if_folder_is_in_params(self):
		assert(False)
		
	def test_list_should_call_listPlaylist_if_playlist_is_in_params(self):
		assert(False)
		
	def test_list_should_call_core_getAuth_to_test_if_login_is_set_if_login_is_in_params(self):
		assert(False)
		
	def test_list_should_return_error_message_if_login_is_not_set_and_login_is_in_params(self):
		assert(False)
		
	def test_list_should_call_createUrl_to_fetch_url(self):
		assert(False)
		
	def test_list_should_call_core_fetchPage_to_get_feed_content(self):
		assert(False)
		
	def test_list_should_call_return_content_and_status_if_fetchPage_failed(self):
		assert(False)
		
	def test_list_should_call_core_getVideoInfo_if_fetchPage_succeded_and_folder_is_not_in_params(self):
		assert(False)
		
	def test_list_should_return_error_status_if_video_list_is_empty(self):
		assert(False)
		
	def test_list_should_call_storage_store_to_save_first_thumbnail_in_list(self):
		assert(False)
		
	def test_listPlaylist_should_call_getSetting_to_get_perpage(self):
		assert(False)
		
	def test_listPlaylist_should_call_storage_retrieve_to_fetch_cached_video_listing(self):
		assert(False)
		
	def test_listPlaylist_should_call_getBatchDetailsOverride_to_fetch_video_info_for_stored_video_list(self):
		assert(False)
		
	def test_listPlaylist_should_call_listAll_if_stored_list_isnt_found(self):
		assert(False)
		
	def test_listPlaylist_should_return_error_status_if_listAll_returns_empty_list(self):
		assert(False)
		
	def test_listPlaylist_should_call_storage_store_with_list_of_video_ids_and_entryids(self):
		assert(False)
		
	def test_listPlaylist_should_call_storage_store_with_first_thumbnail_of_list(self):
		assert(False)
		
	def test_listPlaylist_should_call_addNextFolder_for_lists_longer_than_perpage(self):
		assert(False)
		
	def test_listPlaylist_should_limit_list_lengt_to_perpage_count(self):
		assert(False)
		
	def test_listPlaylist_should_starts_list_position_from_page_count_and_perpage_count(self):
		assert(False)
		
	def test_listFolder_should_call_storage_getUserOptionFolder_if_storage_is_contact_options(self):
		assert(False)
	
	def test_listFolder_should_call_storage_getStoredSearches_if_storage_is_set_but_not_contact_options(self):
		assert(False)

	def test_listFolder_should_call_getSetting_to_get_perpage(self):
		assert(False)
		
	def test_listFolder_should_call_storage_retrieve_to_fetch_cached_video_listing(self):
		assert(False)

	def test_listFolder_should_call_listAll_if_stored_list_isnt_found(self):
		assert(False)

	def test_listFolder_should_call_storage_store_to_save_new_list(self):
		assert(False)

	def test_listFolder_should_call_addNextFolder_for_lists_longer_than_perpage(self):
		assert(False)
		
	def test_listFolder_should_limit_list_lengt_to_perpage_count(self):
		assert(False)
		
	def test_listFolder_should_starts_list_position_from_page_count_and_perpage_count(self):
		assert(False)	
if __name__ == "__main__":
	nose.runmodule()
