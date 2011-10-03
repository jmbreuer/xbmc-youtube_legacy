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

	def ttest_executeAction_should_call_login_login_if_action_is_settings(self):
		assert(False)

	def ttest_executeAction_should_call_storage_deleteStoredSearch_if_action_is_delete_search(self):
		assert(False)

	def ttest_executeAction_should_call_storage_deleteStoredSearch_if_action_is_delete_disco(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

	def ttest_executeAction_should_(self):
		assert(False)

if __name__ == '__main__':
	nose.runmodule()
