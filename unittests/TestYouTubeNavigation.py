# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  YouTubeNavigation import YouTubeNavigation 

class TestYouTubeNavigation(BaseTestCase.BaseTestCase):

	def test_listMenu_should_traverse_menustructure_correctly(self):
		sys.argv = ["something",-1,"something_else"]
		sys.modules["__main__"].settings.getSetting.return_value = "true"
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu()
		
		args = navigation.addListItem.call_args_list
		
		for arg in args:
			assert(arg[0][1]["path"].replace('/root/','').find('/') < 0)
		assert(navigation.addListItem.call_count > 1)
	
	def test_listMenu_should_only_list_subfolders_to_a_path(self):
		sys.argv = ["something",-1,"something_else"]
		list = ["","","",""]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop() 
		navigation = YouTubeNavigation()
		navigation.categories = ({"path":"/root/my_first_level"},{"path":"/root/my_first_level/my_second_level"},{"path":"/root/my_other_first_level"},{"path":"/root/my_other_first_level/my_other_second_level"})
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/my_first_level"})
		
		navigation.addListItem.assert_called_with({"path":"/root/my_first_level"},{"path":"/root/my_first_level/my_second_level"})
		
	def test_listMenu_should_use_visibility_from_settings_to_decide_if_items_are_displayed(self):
		sys.argv = ["something",-1,"something_else"]
		list = ["false","true","false","true"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop() 
		navigation = YouTubeNavigation()
		navigation.categories = ({"path":"/root/my_first_level"},{"path":"/root/my_first_level/my_second_level1"},{"path":"/root/my_first_level/my_second_level2"},{"path":"/root/my_first_level/my_second_level3"})
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/my_first_level"})
		
		navigation.addListItem.assert_called_with({"path":"/root/my_first_level"},{"path":"/root/my_first_level/my_second_level1"})
		navigation.addListItem.assert_called_with({"path":"/root/my_first_level"},{"path":"/root/my_first_level/my_second_level3"})
	
	def test_listMenu_should_check_if_download_path_is_set_to_decide_if_download_folder_is_visible(self):
		sys.argv = ["something",-1,"something_else"]
		list = ["true","true","true","","true"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: list.pop() 
		navigation = YouTubeNavigation()
		navigation.categories = ({"path":"/root/my_first_level/my_second_level1", "feed":"downloads"},{"path":"/root/my_first_level/my_second_level2", "feed":"downloads"})
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/my_first_level"})
		
		navigation.addListItem.assert_called_with({"path":"/root/my_first_level"},{"path":"/root/my_first_level/my_second_level2", "feed":"downloads"})
		
	def test_listMenu_should_call_list_if_feed_in_params(self):
		sys.argv = ["something",-1,"something_else"]
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/some_other_path","feed":"some_feed"})
		
		navigation.list.assert_called_with({"path":"/root/some_other_path","feed":"some_feed"})
		
	def test_listMenu_should_call_list_if_user_feed_in_params(self):
		sys.argv = ["something",-1,"something_else"]
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/some_other_path","user_feed":"some_feed"})
		
		navigation.list.assert_called_with({"path":"/root/some_other_path","user_feed":"some_feed"})
	
	def test_listMenu_should_call_list_if_options_in_params(self):
		sys.argv = ["something",-1,"something_else"]
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/some_other_path","options":"some_options"})
		
		navigation.list.assert_called_with({"path":"/root/some_other_path","options":"some_options"})
	
	def test_listMenu_should_call_list_if_store_in_params(self):
		sys.argv = ["something",-1,"something_else"]
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/some_other_path","store":"some_store"})
		
		navigation.list.assert_called_with({"path":"/root/some_other_path","store":"some_store"})
	
	def test_listMenu_should_call_list_if_scraper_in_params(self):
		sys.argv = ["something",-1,"something_else"]
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/some_other_path","scraper":"some_scraper"})
		
		navigation.list.assert_called_with({"path":"/root/some_other_path","scraper":"some_scraper"})
	
	def test_listMenu_should_call_settings_getSetting_to_get_listview(self):
		sys.argv = ["something",-1,"something_else"]
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		navigation.listMenu({"path":"/root/some_other_path"})
		
		sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")
	
	def ttest_listMenu_should_call_settings_getSetting_to_get_listview_twice(self):
		sys.argv = ["something",-1,"something_else"]
		settings = ["0","0","true"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop() 
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		
		navigation.listMenu({"path":"/root/some_other_path", "scraper":"shows"})
		
		sys.modules["__main__"].settings.getSetting.assert_called_with("list_view")
		counter = 0
		for arg in sys.modules["__main__"].settings.getSetting.call_args_list:
			if arg[0][0] == "list_view":
				counter +=1
		assert(counter == 2)
	
	def test_listMenu_should_call_xbmc_executeBuiltin_correctly_if_list_view_is_set(self):
		sys.argv = ["something",-1,"something_else"]
		settings = ["1","true","1"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop() 
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		
		navigation.listMenu({"path":"/root/some_other_path"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.SetViewMode(500)')
	
	def test_listMenu_should_call_xbmc_plugin_end_of_directory_correctly(self):
		sys.argv = ["something",-1,"something_else"]
		settings = ["1","true","1"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop() 
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.addListItem = Mock()
		
		navigation.listMenu({"path":"/root/some_other_path"})
		
		sys.modules["__main__"].xbmcplugin.endOfDirectory.assert_called_with(cacheToDisc = True, handle = -1, succeeded = True)	

	def test_executeAction_should_call_login_login_if_action_is_settings(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"settings"})
		
		sys.modules["__main__"].login.login.assert_called_with({"action":"settings"})

	def test_executeAction_should_call_storage_deleteStoredSearch_if_action_is_delete_search(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"delete_search"})
		
		sys.modules["__main__"].storage.deleteStoredSearch.assert_called_with({"action":"delete_search"})

	def test_executeAction_should_call_storage_deleteStoredSearch_if_action_is_delete_disco(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"delete_disco"})
		
		sys.modules["__main__"].storage.deleteStoredSearch.assert_called_with({"action":"delete_disco"})

	def test_executeAction_should_call_storage_editStoredSearch_if_action_is_edit_search(self):
		navigation = YouTubeNavigation()
		navigation.listMenu = Mock()
		
		navigation.executeAction({"action":"edit_search"})
		
		sys.modules["__main__"].storage.editStoredSearch.assert_called_with({"action":"edit_search"})

	def test_executeAction_should_call_storage_editStoredSearch_if_action_is_edit_disco(self):
		navigation = YouTubeNavigation()
		navigation.listMenu = Mock()
		
		navigation.executeAction({"action":"edit_disco"})
		
		sys.modules["__main__"].storage.editStoredSearch.assert_called_with({"action":"edit_disco"})

	def test_executeAction_should_call_listMenu_if_action_is_edit_search(self):
		navigation = YouTubeNavigation()
		navigation.listMenu = Mock()
		
		navigation.executeAction({"action":"edit_search"})
		
		navigation.listMenu.assert_called_with({"action":"edit_search"})

	def test_executeAction_should_call_listMenu_if_action_is_edit_disco(self):
		navigation = YouTubeNavigation()
		navigation.listMenu = Mock()
		
		navigation.executeAction({"action":"edit_disco"})
		
		navigation.listMenu.assert_called_with({"action":"edit_disco"})

	def test_executeAction_should_call_storage_deleteStoredArtist_if_action_is_delete_artist(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"delete_artist"})
		
		sys.modules["__main__"].storage.deleteStoredArtist.assert_called_with({"action":"delete_artist"})		

	def test_executeAction_should_call_removeFromFavorites_if_action_is_remove_favorite(self):
		navigation = YouTubeNavigation()
		navigation.removeFromFavorites = Mock()
		
		navigation.executeAction({"action":"remove_favorite"})
		
		navigation.removeFromFavorites.assert_called_with({"action":"remove_favorite"})		

	def test_executeAction_should_call_addToFavorites_if_action_is_add_favorite(self):
		navigation = YouTubeNavigation()
		navigation.addToFavorites = Mock()
		
		navigation.executeAction({"action":"add_favorite"})
		
		navigation.addToFavorites.assert_called_with({"action":"add_favorite"})		

	def test_executeAction_should_call_removeContact_if_action_is_remove_contact(self):
		navigation = YouTubeNavigation()
		navigation.removeContact = Mock()
		
		navigation.executeAction({"action":"remove_contact"})
		
		navigation.removeContact.assert_called_with({"action":"remove_contact"})

	def test_executeAction_should_call_addContact_if_action_is_add_contact(self):
		navigation = YouTubeNavigation()
		navigation.addContact = Mock()
		
		navigation.executeAction({"action":"add_contact"})
		
		navigation.addContact.assert_called_with({"action":"add_contact"})

	def test_executeAction_should_call_removeSubscription_if_action_is_remove_subscription(self):
		navigation = YouTubeNavigation()
		navigation.removeSubscription = Mock()
		
		navigation.executeAction({"action":"remove_subscription"})
		
		navigation.removeSubscription.assert_called_with({"action":"remove_subscription"})

	def test_executeAction_should_call_addSubscription_if_action_is_add_subscription(self):
		navigation = YouTubeNavigation()
		navigation.addSubscription = Mock()
		
		navigation.executeAction({"action":"add_subscription"})
		
		navigation.addSubscription.assert_called_with({"action":"add_subscription"})

	def test_executeAction_should_call_downloader_downloadVideo_if_action_is_download(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"download"})
		
		sys.modules["__main__"].downloader.downloadVideo.assert_called_with({"action":"download"})
	
	def test_executeAction_should_call_player_playVideo_if_action_is_play_video(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"play_video"})
		
		sys.modules["__main__"].player.playVideo.assert_called_with({"action":"play_video"})

	def test_executeAction_should_call_playlist_queueVideo_if_action_is_queue_video(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"queue_video"})
		
		sys.modules["__main__"].playlist.queueVideo.assert_called_with({"action":"queue_video"})

	def test_executeAction_should_call_storage_changeSubscriptionView_if_action_is_change_subscription_view(self):
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.executeAction({"action":"change_subscription_view"})
		
		sys.modules["__main__"].storage.changeSubscriptionView.assert_called_with({"action":"change_subscription_view"})

	def test_executeAction_should_call_list_if_action_is_change_subscription_view(self):
		navigation = YouTubeNavigation()
		navigation.list = Mock()
		navigation.executeAction({"action":"change_subscription_view"})
		
		navigation.list.assert_called_with({"action":"change_subscription_view"})

	def test_executeAction_should_call_playlist_playAll_if_action_is_play_all(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"play_all"})
		
		sys.modules["__main__"].playlist.playAll.assert_called_with({"action":"play_all"})

	def test_executeAction_should_call_playlist_addToPlaylist_if_action_is_add_to_playlist(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"add_to_playlist"})
		
		sys.modules["__main__"].playlist.addToPlaylist.assert_called_with({"action":"add_to_playlist"})

	def test_executeAction_should_call_playlist_removeFromPlaylist_if_action_is_remove_from_playlist(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"remove_from_playlist"})
		
		sys.modules["__main__"].playlist.removeFromPlaylist.assert_called_with({"action":"remove_from_playlist"})

	def test_executeAction_should_call_playlist_deletePlaylist_if_action_is_delete_playlist(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"delete_playlist"})
		
		sys.modules["__main__"].playlist.deletePlaylist.assert_called_with({"action":"delete_playlist"})

	def test_executeAction_should_call_storage_reversePlaylistOrder_if_action_is_reverse_order(self):
		navigation = YouTubeNavigation()
		
		navigation.executeAction({"action":"reverse_order"})
		
		sys.modules["__main__"].storage.reversePlaylistOrder.assert_called_with({"action":"reverse_order"})

	def test_list_should_ask_user_for_input_if_feed_is_search_and_search_is_missing_from_params(self):
		sys.modules["__main__"].feeds.list.return_value = ([],200)
		sys.modules["__main__"].language.return_value = "some_string"
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"feed":"search"})
		
		sys.modules["__main__"].utils.getUserInput.assert_called_with("some_string","")

	def test_list_should_ask_user_for_input_if_scraper_is_search_disco_and_search_is_missing_from_params(self):
		sys.modules["__main__"].scraper.scrape.return_value = ([],200)
		sys.modules["__main__"].language.return_value = "some_string"
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"scraper":"search_disco"})
		
		sys.modules["__main__"].utils.getUserInput.assert_called_with("some_string","")

	def test_list_should_call_storage_saveStoredSearch_if_feed_is_search(self):
		sys.modules["__main__"].feeds.list.return_value = ([],200)
		sys.modules["__main__"].language.return_value = "some_string"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_user_string"
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"feed":"search"})
		
		sys.modules["__main__"].storage.saveStoredSearch.assert_called_with({"feed":"search","search":"some_user_string"})

	def test_list_should_call_storage_saveStoredSearch_if_scraper_is_search_disco(self):
		sys.modules["__main__"].scraper.scrape.return_value = ([],200)
		sys.modules["__main__"].language.return_value = "some_string"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_user_string"
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"scraper":"search_disco"})
		
		sys.modules["__main__"].storage.saveStoredSearch.assert_called_with({"scraper":"search_disco","search":"some_user_string"})

	def test_list_should_call_scraper_scrape_if_scraper_is_in_params(self):
		sys.modules["__main__"].scraper.scrape.return_value = ([],200)
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"scraper":"some_scraper"})
		
		sys.modules["__main__"].scraper.scrape.assert_called_with({"scraper":"some_scraper"})

	def test_list_should_call_storage_list_if_store_is_in_params(self):
		sys.modules["__main__"].storage.list.return_value = ([],200)
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"store":"some_store"})
		
		sys.modules["__main__"].storage.list.assert_called_with({"store":"some_store"})
		
	def test_list_should_call_feeds_list_if_neither_store_or_scraper_is_in_params(self):
		sys.modules["__main__"].feeds.list.return_value = ([],200)
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({})
		
		sys.modules["__main__"].feeds.list.assert_called_with({})
		
	def test_list_should_call_parseFolderList_if_list_was_successfull_and_folder_is_in_params(self):
		sys.modules["__main__"].feeds.list.return_value = ([],200)
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({"folder":"true"})
		
		navigation.parseFolderList.assert_called_with({"folder":"true"},[])
		
	def test_list_should_call_parseVideoList_if_list_was_successfull_and_folder_is_not_in_params(self):
		sys.modules["__main__"].feeds.list.return_value = ([],200)
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({})
		
		navigation.parseVideoList.assert_called_with({},[])		
	
	def test_list_should_call_showListingError_if_list_was_unsuccessfull(self):
		sys.modules["__main__"].feeds.list.return_value = ([],303)
		navigation = YouTubeNavigation()
		navigation.parseVideoList = Mock()
		navigation.parseFolderList = Mock()
		navigation.showListError = Mock()
		
		navigation.list({})
		
		navigation.showListError.assert_called_with({})		
	
	def ttest_showListingError_should_search_categories_for_folder_name_if_external_is_not_in_params(self):
		assert(False)
			
	def ttest_showListingError_should_search_storage_user_options_if_external_is_in_params(self):
		assert(False)
				
	def ttest_showListingError_should_use_channel_title_if_channel_is_in_params(self):
		assert(False)
		
	def ttest_showListingError_should_use_language_string_if_playlist_is_in_params(self):
		assert(False)
		
	def ttest_showListingError_should_call_utils_showMessage_correctly(self):
		assert(False)
				
		
if __name__ == '__main__':
	nose.runmodule()
