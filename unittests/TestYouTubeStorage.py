# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  YouTubeStorage import YouTubeStorage 

class TestYouTubeStorage(BaseTestCase.BaseTestCase):
	
	def test_list_should_call_getUserOptionFolder_if_store_contact_option_is_in_params(self):
		storage = YouTubeStorage()
		storage.getUserOptionFolder = Mock()
		storage.getUserOptionFolder.return_value = ("",200)
		
		storage.list({"store":"contact_options"})
		
		storage.getUserOptionFolder.assert_called_with({"store":"contact_options"})
	
	def test_list_should_call_getStoredArtists_if_store_artist_is_in_params(self):
		storage = YouTubeStorage()
		storage.getStoredArtists = Mock()
		storage.getStoredArtists.return_value = ("",200)
		
		storage.list({"store":"artists"})
		
		storage.getStoredArtists.assert_called_with({"store":"artists"})

	def test_list_should_call_getStoredSearches_if_store_is_defined_in_params_but_not_artist_or_contact_option(self):
		storage = YouTubeStorage()
		storage.getStoredSearches = Mock()
		storage.getStoredSearches.return_value = ("",200)
		
		storage.list({"store":"somestore"})
		
		storage.getStoredSearches.assert_called_with({"store":"somestore"})

	def test_openFile_should_call_io_open(self):
		patcher = patch("io.open")
		patcher.start()
		import io
		io.open.return_value = "my_result"
		storage = YouTubeStorage()
		
		result = storage.openFile("someFile")
		patcher.stop()
		
		assert(result == "my_result")

	def test_getStoredArtists_should_call_retrieve_to_get_list_of_artists(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = []
		#storage.retrieve.return_value = [("some_title","some_artist")]
		
		storage.getStoredArtists({"store":"somestore"})
		
		storage.retrieve.assert_called_with({"store":"somestore"})
		
	def test_getStoredArtists_should_call_retrieve_to_get_artist_thumbnails(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = [("some_title","some_artist")]
		
		storage.getStoredArtists({"path":"some_path","store":"somestore"})
		
		storage.retrieve.assert_called_with({"path":"some_path","store":"somestore"}, "thumbnail", {'artist': 'some_artist', 'Title': 'some_title', 'scraper': 'music_artist', 'path': "some_path", 'thumbnail': [('some_title', 'some_artist')], 'icon': 'music'})
		
	def test_getStoredArtists_should_return_proper_list_structure(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = [("some_title","some_artist")]
		
		(result, status) = storage.getStoredArtists({"path":"some_path","store":"somestore"})
		assert(result[0]["artist"] == "some_artist")
		assert(result[0]["Title"] == "some_title")
		assert(result[0]["scraper"] == "music_artist")
		assert(result[0].has_key("icon"))
		assert(result[0].has_key("thumbnail"))
		
	def test_deleteStoredArtist_should_call_retrieve_to_get_list_of_artists(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = []
		storage.store = Mock()
		
		storage.deleteStoredArtist({"path":"some_path","store":"somestore"})
		
		storage.retrieve.assert_called_with({"path":"some_path","store":"somestore"})

	def test_deleteStoredArtist_should_call_store_to_save_new_list_of_artists(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = [("some_title","some_artist")]
		storage.store = Mock()
		
		storage.deleteStoredArtist({"path":"some_path","store":"somestore"})
		
		storage.store.assert_called_with({"path":"some_path","store":"somestore"},[('some_title', 'some_artist')])

	def test_deleteStoredArtist_should_remove_artist_from_list_before_saving(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = [("some_title","some_artist")]
		storage.store = Mock()
		
		storage.deleteStoredArtist({"path":"some_path","store":"somestore", "artist":"some_artist"})
		
		storage.store.assert_called_with({"path":"some_path","store":"somestore", "artist":"some_artist"},[])

	def test_getStoredArtists_should_call_executebuiltin_when_done(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = [("some_title","some_artist")]
		storage.store = Mock()
		
		storage.deleteStoredArtist({"path":"some_path","store":"somestore", "artist":"some_artist"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')
	
	def test_saveStoredArtist_should_exit_cleanly_if_artist_or_artist_name_is_missing(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.store = Mock()
		
		storage.saveStoredArtist({})
		
		assert(storage.retrieve.call_count == 0)
		assert(storage.store.call_count == 0)

	def test_saveStoredArtist_should_call_retrieve_with_correct_params(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = []
		storage.store = Mock()
		
		storage.saveStoredArtist({"artist":"some_artist","artist_name":"some_artist_name"})
		
		storage.retrieve.assert_called_with({"artist":"some_artist","artist_name":"some_artist_name"})
	
	def test_saveStoredArtist_should_call_getSettings_to_get_max_searches_count(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = []
		storage.store = Mock()
		
		storage.saveStoredArtist({"artist":"some_artist","artist_name":"some_artist_name"})
		
		sys.modules["__main__"].settings.getSetting.assert_called_with("saved_searches")

	def test_saveStoredArtist_should_call_store(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value = []
		storage.store = Mock()
		
		storage.saveStoredArtist({"artist":"some_artist","artist_name":"some_artist_name"})
		
		storage.store.assert_called_with({'artist_name': 'some_artist_name', 'artist': 'some_artist'}, [('some_artist_name', 'some_artist')])

	def test_saveStoredArtist_should_limit_artist_collection_before_calling_store(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  [("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("",""),("","")]
		storage.store = Mock()
		
		storage.saveStoredArtist({"artist":"some_artist","artist_name":"some_artist_name"})
		
		assert(len(storage.store.call_args[0][1]) == 10)
	
	def test_saveStoredArtist_should_add_artist_to_collection_before_calling_store(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  [("","")]
		storage.store = Mock()
		
		storage.saveStoredArtist({"artist":"some_artist","artist_name":"some_artist_name"})
		
		assert(len(storage.store.call_args[0][1]) == 2)
		storage.store.assert_called_with({'artist_name': 'some_artist_name', 'artist': 'some_artist'}, [('some_artist_name', 'some_artist'), ("","")])		

	def test_saveStoredArtist_should_delete_store_from_params_before_exiting(self):
		sys.modules["__main__"].settings.getSetting.return_value = 0
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  [("","")]
		storage.store = Mock()
		params = {"artist":"some_artist","artist_name":"some_artist_name", "store":"artists"}
		
		storage.saveStoredArtist(params)
		
		assert(params.has_key("store") == False)

	def test_getStoredSearches_should_call_retrieve_to_get_searches(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search"]
		storage.store = Mock()
		
		storage.getStoredSearches({"path":"some_path"})
		
		assert(storage.retrieve.call_count > 0)		

	def test_getStoredSearches_should_call_retrieve_to_get_thumbnail_collection(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search"]
		storage.store = Mock()
		
		storage.getStoredSearches({"path":"some_path"})
		
		assert(storage.retrieve.call_args[0][0] == {"path":"some_path"})
		assert(storage.retrieve.call_args[0][1] == "thumbnail")
		assert(storage.retrieve.call_args[0][2] == {'path': 'some_path', 'search': 'some_search', 'thumbnail': ['some_search'], 'Title': 'some_search'})
		assert(storage.retrieve.call_count == 2)

	def test_getStoredSearches_should_return_proper_list_structure(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search"]
		storage.store = Mock()
		
		(result, status) = storage.getStoredSearches({"path":"some_path"})
		
		print repr(result)
		assert(result == [{'path': 'some_path', 'search': 'some_search', 'thumbnail': ['some_search'], 'Title': 'some_search'}])
		
	def test_getStoredSearches_should_call_quote_plus_on_search_items(self):
		patcher = patch("urllib.quote_plus")
		patcher.start()
		import urllib
		urllib.quote_plus.return_value = "some_quoted_search"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search"]
		storage.store = Mock()
		
		(result, status) = storage.getStoredSearches({"path":"some_path"})
		args = urllib.quote_plus.call_args
		patcher.stop()
		
		assert(args[0][0] == "some_search")
		assert(result == [{'path': 'some_path', 'search': 'some_quoted_search', 'thumbnail': ['some_search'], 'Title': 'some_search'}])
				

	def test_deleteStoredSearch_should_call_unquote_on_delete_param(self):
		patcher = patch("urllib.unquote_plus")
		patcher.start()
		import urllib
		urllib.unquote_plus.return_value = "some_unquoted_search"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search1"]
		storage.store = Mock()
		
		storage.deleteStoredSearch({"delete":"some_search2"})
		args = urllib.unquote_plus.call_args
		patcher.stop()
		
		assert(args[0][0] == "some_search2")

	def test_deleteStoredSearch_should_call_retrieve_to_get_searches(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search1"]
		storage.store = Mock()
		
		storage.deleteStoredSearch({"delete":"some_search2"})
		
		storage.retrieve.assert_called_with({'delete': 'some_search2'})
		assert(storage.retrieve.call_count == 1)

	def test_deleteStoredSearch_should_remove_search_from_list_before_calling_store(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.deleteStoredSearch({"delete":"some_search2"})
		
		storage.store.assert_called_with({"delete":"some_search2"},[])

	def test_deleteStoredSearch_should_call_executebuiltin(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.deleteStoredSearch({"delete":"some_search2"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')

	def test_saveStoredSearch_should_exit_cleanly_if_search_is_not_in_params(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.saveStoredSearch({})
		
		assert(storage.retrieve.call_count == 0)
		assert(storage.store.call_count == 0)
		
	def test_saveStoredSearch_should_call_unquote_on_search_param(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"		
		patcher = patch("urllib.unquote_plus")
		patcher.start()
		import urllib
		urllib.unquote_plus.return_value = "some_unquoted_search"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search1"]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search"})

		args = urllib.unquote_plus.call_args
		patcher.stop()
		
		assert(args[0][0] == "some_search")

	def test_saveStoredSearch_should_call_unquote_on_old_search_param_if_it_exists(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"		
		patcher = patch("urllib.unquote_plus")
		patcher.start()
		import urllib
		urllib.unquote_plus.return_value = "some_unquoted_search"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search1"]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search1", "old_search":"some_search2"})
		
		args = urllib.unquote_plus.call_args_list
		patcher.stop()
		
		assert(args[0][0][0] == "some_search1")
		assert(args[1][0][0] == "some_search2")

	def test_saveStoredSearch_should_call_retrieve_to_get_list_of_searches(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search1", "old_search":"some_search2"})
		
		storage.retrieve.assert_called_with({"search":"some_search1", "old_search":"some_search2"})

	def test_saveStoredSearch_should_remove_old_search_from_collection_and_prepend_new_search(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search4","some_search2", "some_search3"]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search1", "old_search":"some_search2"})
		
		storage.store.assert_called_with({"search":"some_search1", "old_search":"some_search2"},['some_search1', 'some_search4', 'some_search3'])
		
	def test_saveStoredSearch_should_limit_search_collection_before_calling_store(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search4","some_search2", "some_search3","","","","","","","",""]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search1", "old_search":"some_search2"})
		
		assert(len(storage.store.call_args[0][1]) == 10)
		storage.store.assert_called_with({"search":"some_search1", "old_search":"some_search2"},['some_search1', 'some_search4', 'some_search3',"","","","","","",""])

	def test_saveStoredSearch_should_call_getSettings_to_get_max_searches_count(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search1", "old_search":"some_search2"})
		
		sys.modules["__main__"].settings.getSetting.assert_called_with("saved_searches")

	def test_saveStoredSearch_should_call_store_to_save_searches_collection(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.saveStoredSearch({"search":"some_search1", "old_search":"some_search2"})
		
		assert(storage.store.call_count > 0)

	def test_editStoredSearch_should_exit_cleanly_if_search_param_is_missing(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.editStoredSearch({})
		
		assert(storage.store.call_count == 0)
		assert(storage.retrieve.call_count == 0)

	def test_editStoredSearch_should_ask_user_for_new_search_phrase(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].language.return_value = "some_title"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.editStoredSearch({"search":"some_search1"})
		
		sys.modules["__main__"].utils.getUserInput.assert_called_with('some_title', 'some_search1')

	def test_editStoredSearch_should_set_store_to_searches_if_editing_searches(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].language.return_value = "some_title"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.editStoredSearch({"search":"some_search1"})
		
		assert(storage.store.call_args[0][0].has_key("feed"))
		
	def test_editStoredSearch_should_set_store_to_disco_if_editing_disco_searches(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].language.return_value = "some_title"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		
		storage.editStoredSearch({"search":"some_search1", "action":"edit_disco"})
		
		assert(storage.store.call_args[0][0].has_key("scraper"))

	def test_editStoredSearch_should_call_saveStoredSearch(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].language.return_value = "some_title"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		storage.saveStoredSearch = Mock()
		
		storage.editStoredSearch({"search":"some_search1", "action":"edit_disco"})
		
		storage.saveStoredSearch.assert_called_with({'search': 'some_search3', 'scraper': 'search_disco'})

	def test_editStoredSearch_should_remove_old_search_param_before_exiting(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].language.return_value = "some_title"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		storage.saveStoredSearch = Mock()
		params = {"search":"some_search1", "action":"edit_disco", "old_search":"some_search4"}
		
		storage.editStoredSearch(params)
		
		assert(params.has_key("old_search") == False)
	
	def test_editStoredSearch_should_set_search_params_before_exiting(self):
		sys.modules["__main__"].settings.getSetting.return_value = "0"
		sys.modules["__main__"].language.return_value = "some_title"
		sys.modules["__main__"].utils.getUserInput.return_value = "some_search3"
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  ["some_search2"]
		storage.store = Mock()
		storage.saveStoredSearch = Mock()
		params = {"search":"some_search1", "action":"edit_disco", "old_search":"some_search4"}
		
		storage.editStoredSearch(params)
		
		assert(params.has_key("search"))
		assert(params["search"] == "some_search3")
	
	def test_getUserOptionFolder_should_return_modified_version_of_items_in_user_options(self):
		sys.modules["__main__"].language.return_value = "some_title"
		storage = YouTubeStorage()
		
		(result, status) = storage.getUserOptionFolder({})
		
		assert(len(result) == 4)
		assert(result[0]["user_feed"] == "favorites")
		assert(result[1]["user_feed"] == "playlists")
		assert(result[2]["user_feed"] == "subscriptions")
		assert(result[3]["user_feed"] == "uploads")
		
	def test_changeSubscriptionView_should_exit_cleanly_if_view_mode_is_not_in_params(self):
		storage = YouTubeStorage()
		storage.getStorageKey = Mock()
		storage.storeValue = Mock()
		
		storage.changeSubscriptionView({})
		
		assert(storage.getStorageKey.call_count == 0)
		assert(storage.storeValue.call_count == 0)

	def test_changeSubscriptionView_should_call_getStorageKey(self):
		storage = YouTubeStorage()
		storage.getStorageKey = Mock()
		storage.storeValue = Mock()
		
		storage.changeSubscriptionView({"view_mode":"my_view_mode"})
		
		storage.getStorageKey.assert_called_with({"user_feed":"my_view_mode","view_mode":"my_view_mode"}, "viewmode")

	def test_changeSubscriptionView_should_call_storeValue(self):
		storage = YouTubeStorage()
		storage.getStorageKey = Mock()
		storage.getStorageKey.return_value = "my_key"
		storage.storeValue = Mock()
		
		storage.changeSubscriptionView({"view_mode":"my_view_mode"})
		
		storage.storeValue.assert_called_with("my_key","my_view_mode")

	def test_changeSubscriptionView_should_fill_params_collection_before_exiting(self):
		storage = YouTubeStorage()
		storage.getStorageKey = Mock()
		storage.getStorageKey.return_value = "my_key"
		storage.storeValue = Mock()
		
		params = {"view_mode":"my_view_mode"}
		storage.changeSubscriptionView(params)
		
		assert(params.has_key("user_feed"))

	def test_reversePlaylistOrder_should_exit_cleanly_if_playlist_params_is_missing(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  "false"
		storage.store = Mock()
		
		storage.reversePlaylistOrder({})
		
		assert(storage.retrieve.call_count == 0)
		assert(storage.store.call_count == 0)
				
	def test_reversePlaylistOrder_should_call_retrieve_to_fetch_reverse_value(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  "false"
		storage.store = Mock()
		
		storage.reversePlaylistOrder({"playlist":"some_playlists"})
		
		storage.retrieve.assert_called_with({'playlist': 'some_playlists'}, 'value')
		
	def test_reversePlaylistOrder_should_call_store_to_save_reverse_value(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  "false"
		storage.store = Mock()
		
		storage.reversePlaylistOrder({"playlist":"some_playlists"})
		
		storage.store.assert_called_with({'playlist': 'some_playlists'}, 'true', 'value')
	
	def test_reversePlaylistOrder_should_executebuiltin_on_succes(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  "false"
		storage.store = Mock()
		
		storage.reversePlaylistOrder({"playlist":"some_playlists"})
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('Container.Refresh')
		
	def test_getReversePlaylistOrder_should_return_false_if_playlist_is_not_in_params(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  "true"
		storage.store = Mock()
		
		result = storage.getReversePlaylistOrder()
		
		assert(result == False)
		
	def test_getReversePlaylistOrder_should_call_retrieve_to_fetch_reverse_value(self):
		storage = YouTubeStorage()
		storage.retrieve = Mock()
		storage.retrieve.return_value =  "true"
		
		result = storage.getReversePlaylistOrder({"playlist":"some_playlists"})
		
		assert(result == True)
	
if __name__ == '__main__':
	nose.run()
