import nose
import BaseTestCase
from mock import Mock, patch
import sys
from YouTubeCore import YouTubeCore

class TestYouTubeCore(BaseTestCase.BaseTestCase):

	def test_delete_favorite_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/favorites/test"

		core.delete_favorite({ "editid": "test" })
				
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

	def test_remove_contact_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/contacts/come_contact"		

		core.remove_contact({ "contact": "come_contact" })
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

	def test_remove_subscription_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions/edit_id"		

		core.remove_subscription({ "editid": "edit_id" })
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

	def test_add_contact_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/contacts"		
		request = '<?xml version="1.0" encoding="UTF-8"?> <entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><yt:username>some_contact</yt:username></entry>'
		
		core.add_contact({ "editid": "edit_id", "contact":"some_contact" })
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"request":request,"link": delete_url, "api": "true", "login": "true", "auth": "true"})

	def test_add_favorite_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		url = "http://gdata.youtube.com/feeds/api/users/default/favorites"		
		request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom"><id>some_id</id></entry>'
		
		core.add_favorite({ "editid": "edit_id", "videoid":"some_id" })
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"request":request,"link": url, "api": "true", "login": "true", "auth": "true"})

	def test_add_subscription_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions"		
		request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"> <category scheme="http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat" term="user"/><yt:username>channel</yt:username></entry>'
		
		core.add_subscription({ "channel": "channel"})
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"request":request,"link": url, "api": "true", "login": "true", "auth": "true"})
		
	def test_add_playlist_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		url = "http://gdata.youtube.com/feeds/api/users/default/playlists"		
		request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><title type="text">some_title</title><summary>some_summary</summary></entry>'
		
		core.add_playlist({ "title": "some_title", "summary":"some_summary"})
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"request":request,"link": url, "api": "true", "login": "true", "auth": "true"})

	def test_del_playlist_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		url = "http://gdata.youtube.com/feeds/api/users/default/playlists/some_playlist"
		
		core.del_playlist({ "playlist": "some_playlist"})
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"link": url, "api": "true", "login": "true", "auth": "true","method":"DELETE"})

	def test_add_to_playlist_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		url = "http://gdata.youtube.com/feeds/api/playlists/some_playlist"
		request = '<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><id>some_id</id></entry>'
		
		core.add_to_playlist({ "playlist": "some_playlist","videoid":"some_id"})
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"request":request,"link": url, "api": "true", "login": "true", "auth": "true"})

	def test_remove_from_playlist_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}
		url = "http://gdata.youtube.com/feeds/api/playlists/some_playlist/some_entry_id"
		
		core.remove_from_playlist({ "playlist": "some_playlist","playlist_entry_id":"some_entry_id"})
		
		assert(core._fetchPage.called)
		assert(core._fetchPage.call_count == 1)
		core._fetchPage.assert_called_with({"link": url, "api": "true", "login": "true", "auth": "true","method":"DELETE"})

	def test_getFolderInfo_should_use_getElementsByTagName_to_look_for_link_and_entries(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("xml.dom.minidom.parseString")
		patcher.start()
		import xml.dom.minidom
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString().getElementsByTagName.return_value = ""
		core = YouTubeCore()

		core.getFolderInfo("xml", {})
		
		calls = xml.dom.minidom.parseString().getElementsByTagName.call_args_list
		patcher.stop("")
		assert(calls[0][0][0] == "link")
		assert(calls[1][0][0] == "entry")

	def test_getFolderInfo_should_search_links_relation_attribute_for_multiple_pages(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("xml.dom.minidom.parseString")
		patcher.start()
		import xml.dom.minidom
		link = Mock()
		rel = Mock()
		rel.value = "next"
		link.attributes = {"rel":rel}
		tags = ["", [link]]
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString().getElementsByTagName.side_effect = lambda x: tags.pop() 
		core = YouTubeCore()
		
		core.getFolderInfo("xml", {})

		patcher.stop("")
		sys.modules["__main__"].utils.addNextFolder.assert_called_with([], {})
	
	def test_getFolderInfo_should_find_edit_id_in_xml_structure_if_id_tag_is_present(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		input = self.readTestInput("getFolderInfoPlaylistTest.xml", False)
		core = YouTubeCore()
		
		result = core.getFolderInfo(input, {})

		assert(result[0]["editid"] == "some_playlist_id")


	def test_getFolderInfo_should_set_item_params_correctly_for_contacts_feed(self):
		settings = ["4","3" ]
		sys.modules["__main__"].storage.retrieve.return_value = "some_thumbnail"
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		input = self.readTestInput("getFolderInfoContactTest.xml", False)
		core = YouTubeCore()
		
		result = core.getFolderInfo(input, {"user_feed":"contacts"})
		
		assert(result[0]["editid"] == "some_other_user")
		assert(result[0]["thumbnail"] == "some_thumbnail")
		assert(result[0]["login"] == "true")
		assert(result[0]["contact"] == "some_other_user")
		assert(result[0]["store"] == "contact_options")
		assert(result[0]["Title"] == "some_other_user")
		assert(result[0]["folder"] == "true")

	def test_getFolderInfo_should_set_item_params_correctly_for_subscriptions_feed(self):
		settings = ["4","3" ]
		sys.modules["__main__"].storage.retrieve.return_value = "some_thumbnail"
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		input = self.readTestInput("getFolderInfoSubscriptionsTest.xml", False)
		core = YouTubeCore()
		
		result = core.getFolderInfo(input, {"user_feed":"subscriptions"})
		
		assert(result[0]["editid"] == "some_edit_id")
		assert(result[0]["thumbnail"] == "some_thumbnail")
		assert(result[0]["login"] == "true")
		assert(result[0]["channel"] == "GoogleTechTalks")
		assert(result[0]["Title"] == "GoogleTechTalks")
		
	def test_getFolderInfo_should_set_item_params_correctly_for_playlist_feed(self):
		settings = ["4","3" ]
		sys.modules["__main__"].storage.retrieve.return_value = "some_thumbnail"
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		input = self.readTestInput("GetFolderInfoPlaylistTest.xml", False)
		core = YouTubeCore()
		
		result = core.getFolderInfo(input, {"user_feed":"playlists"})
		
		assert(result[0]["editid"] == "some_playlist_id")
		assert(result[0]["thumbnail"] == "some_thumbnail")
		assert(result[0]["login"] == "true")
		assert(result[0]["playlist"] == "some_playlist_id")
		assert(result[0]["user_feed"] == "playlist")
		assert(result[0]["Title"] == "Stand back I'm going to try Science!")

	def test_getFolderInfo_should_call_storage_retrieve_to_find_thumbnail(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		input = self.readTestInput("getFolderInfoPlaylistTest.xml", False)
		core = YouTubeCore()
		
		result = core.getFolderInfo(input, {})

		assert(sys.modules["__main__"].storage.retrieve.call_count == 1)
	
	def test_getFolderInfo_should_call_utils_addNextFolder_to_set_default_next_folder_on_feed(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("xml.dom.minidom.parseString")
		patcher.start()
		import xml.dom.minidom
		link = Mock()
		rel = Mock()
		rel.value = "next"
		link.attributes = {"rel":rel}
		tags = ["", [link]]
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString().getElementsByTagName.side_effect = lambda x: tags.pop() 
		core = YouTubeCore()
		
		core.getFolderInfo("xml", {})

		patcher.stop("")
		sys.modules["__main__"].utils.addNextFolder.assert_called_with([], {})
		
	def test_getBatchDetailsOverride_should_call_getBatchDetails_with_list_of_video_ids(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core.getBatchDetails = Mock()
		core.getBatchDetails.return_value = ([{"videoid":"some_id3"},{"videoid":"some_id2"},{"videoid":"some_id1"}], 200)
		items = [{"videoid":"some_id1","some_key1":"value1"},{"videoid":"some_id2","some_key2":"value2"}, {"videoid":"some_id3","some_key3":"value3"}]
		
		(result, status) = core.getBatchDetailsOverride(items, params={})
		
		core.getBatchDetails.assert_called_with(['some_id1', 'some_id2', 'some_id3'], {})

	def test_getBatchDetailsOverride_should_override_specified_properties_in_output_from_getBatchDetails(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core.getBatchDetails = Mock()
		core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"},{"videoid":"some_id1","some_key1":"blabla"}], 200)
		items = [{"videoid":"some_id1","some_key1":"value1"},{"videoid":"some_id2","some_key2":"value2"}, {"videoid":"some_id3","some_key3":"value3"}]
		
		(result, status) = core.getBatchDetailsOverride(items, params={})
		
		assert(result[0]["some_key3"] == "value3")
		assert(result[1]["some_key2"] == "value2")
		assert(result[2]["some_key1"] == "value1")

	def test_getBatchDetailsThumbnails_should_call_getBatchDetails_with_list_of_video_ids(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core.getBatchDetails = Mock()
		core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"},{"videoid":"some_id1","some_key1":"blabla"}], 200)
		items = [("some_id3","some_thumb3"),("some_id2","some_thumb2"),("some_id1","some_thumb1")]
		
		(result, status) = core.getBatchDetailsThumbnails(items, params={})
		
		core.getBatchDetails.assert_called_with(['some_id3', 'some_id2', 'some_id1'], {})
		
	def test_getBatchDetailsThumbnails_should_override_thumbnails_in_output_from_getBatchDetails(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core.getBatchDetails = Mock()
		core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"},{"videoid":"some_id1","some_key1":"blabla"}], 200)
		items = [("some_id3","some_thumb3"),("some_id2","some_thumb2"),("some_id1","some_thumb1")]
		
		(result, status) = core.getBatchDetailsThumbnails(items, params={})
		
		assert(result[0]["thumbnail"] == "some_thumb3")
		assert(result[1]["thumbnail"] == "some_thumb2")
		assert(result[2]["thumbnail"] == "some_thumb1")
		
	def test_getBatchDetailsThumbnails_should_fill_out_missing_videos_in_collection_from_getBatchDetails_to_maintain_collection_size(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core.getBatchDetails = Mock()
		core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"}], 200)
		items = [("some_id3","some_thumb3"),("some_id2","some_thumb2"),("some_id1","some_thumb1")]
		
		(result, status) = core.getBatchDetailsThumbnails(items, params={})
		
		assert(result[0]["thumbnail"] == "some_thumb3")
		assert(result[1]["thumbnail"] == "some_thumb2")
		assert(result[2]["videoid"] == "false")

	def test_getBatchDetailsOverride_should_fill_out_missing_videos_in_collection_from_getBatchDetails_to_maintain_collection_size(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core.getBatchDetails = Mock()
		core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"}], 200)
		items = [{"videoid":"some_id1","some_key1":"value1"},{"videoid":"some_id2","some_key2":"value2"}, {"videoid":"some_id3","some_key3":"value3"}]
		
		(result, status) = core.getBatchDetailsOverride(items, params={})
		
		assert(result[0]["some_key3"] == "value3")
		assert(result[1]["some_key2"] == "value2")
		assert(result[2]["videoid"] == "false")
		
	def test_getBatchDetails_should_call_cache_sqlGetMulti_before_hitting_youtube(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core._fetchPage = Mock()
		
		core.getBatchDetails([],{})
		
		sys.modules["__main__"].cache.sqlGetMulti.assert_called_with('videoidcache', [])

	def test_getBatchDetails_should_not_request_video_information_for_cached_videos(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core._fetchPage = Mock()
		core.getVideoInfo = Mock()
		core.getVideoInfo.return_value = []
		core._fetchPage.return_value = {"content":"","status":303}
		sys.modules["__main__"].cache.sqlGetMulti.return_value = ['{"videoid":"some_id_1"}',"","","",'{"videoid":"some_id_5"}']
		
		core.getBatchDetails(["some_id_1","some_id_2","some_id_3","some_id_4","some_id_5"],{})
		
		request = core._fetchPage.call_args_list[0][0][0]["request"]
		assert(request.find("some_id_1") < 0)
		assert(request.find("some_id_5") < 0)
	
	def test_getBatchDetails_should_at_most_request_50_videos_in_one_call(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core._fetchPage = Mock()
		core.getVideoInfo = Mock()
		core.getVideoInfo.return_value = []
		core._fetchPage.return_value = {"content":"","status":303}
		sys.modules["__main__"].cache.sqlGetMulti.return_value = []
		sys.modules["__main__"].common.parseDOM.return_value = ""
		ids = []
		i= 1
		while i < 52:
			ids.append("some_id_"  + str(i))
			i += 1
		
		core.getBatchDetails(ids,{})
		
		request = core._fetchPage.call_args_list[0][0][0]["request"]
		assert(request.find("some_id_52") < 0)
		assert(request.find("some_id_1") > 0)
		assert(request.find("some_id_50") > 0)

	def test_getBatchDetails_should_search_result_for_response_status_code(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core._fetchPage = Mock()
		core.getVideoInfo = Mock()
		core.getVideoInfo.return_value = []
		core._fetchPage.return_value = {"content":"","status":303}
		sys.modules["__main__"].cache.sqlGetMulti.return_value = []
		sys.modules["__main__"].common.parseDOM.return_value = ""
		ids = []
		i= 1
		while i < 52:
			ids.append("some_id_"  + str(i))
			i += 1
		
		core.getBatchDetails(ids,{})
		
		sys.modules["__main__"].common.parseDOM.assert_called_with("","batch:status",ret="code")

	def test_getBatchDetails_should_sleep_for_5_seconds_if_youtube_returns_error(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("time.sleep")
		patcher.start()
		import time
		time.sleep = Mock() 		
		core = YouTubeCore()
		core._fetchPage = Mock()
		core.getVideoInfo = Mock()
		core.getVideoInfo.return_value = []
		core._fetchPage.return_value = {"content":"","status":303}
		sys.modules["__main__"].cache.sqlGetMulti.return_value = []
		status = [[],["","403"]]
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "", y ="",attrs = {},ret = {}: status.pop()  
		ids = []
		i= 1
		while i < 52:
			ids.append("some_id_"  + str(i))
			i += 1
		
		core.getBatchDetails(ids,{})
		
		time.sleep.assert_called_with(5)
		patcher.stop()


	def test_getBatchDetails_should_call_get_video_info_on_result(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core._fetchPage = Mock()
		core.getVideoInfo = Mock()
		core.getVideoInfo.return_value = []
		core._fetchPage.return_value = {"content":"some_content","status":303}
		sys.modules["__main__"].cache.sqlGetMulti.return_value = ['{"videoid":"some_id_1"}',"","","",'{"videoid":"some_id_5"}']
		
		core.getBatchDetails(["some_id_1","some_id_2","some_id_3","some_id_4","some_id_5"],{"param":"some_params"})
		
		core.getVideoInfo.assert_called_with("some_content",{"param":"some_params"})
		
	def test_getBatchDetails_should_handle_collection_sizes_above_50(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()		
		core = YouTubeCore()
		core._fetchPage = Mock()
		core.getVideoInfo = Mock()
		core.getVideoInfo.return_value = []
		core._fetchPage.return_value = {"content":"","status":303}
		sys.modules["__main__"].cache.sqlGetMulti.return_value = []
		sys.modules["__main__"].common.parseDOM.return_value = ""
		ids = []
		i= 1
		while i < 75:
			ids.append("some_id_"  + str(i))
			i += 1
		
		core.getBatchDetails(ids,{})
		
		assert(core._fetchPage.call_count == 2)
			
	def test_fetchPage_should_return_error_status_and_empty_content_if_no_params_are_provided(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("urllib2.urlopen")
		patcher.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore()
				
		ret = core._fetchPage({})
		patcher.stop()
		
		assert(ret['status'] == 500 and ret['content'] == "")
	
	def test_fetchPage_should_call_getAuth_to_fetch_oauth_token_if_auth_is_in_params_collection(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("urllib2.urlopen")
		patcher.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk"})
		
		patcher.stop()
		core._getAuth.assert_called_with()

	def test_fetchPage_should_call_getSettings_if_to_fetch_oauth_token_if_auth_is_in_params_collection(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("urllib2.urlopen")
		patcher.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk"})
		
		patcher.stop()
		assert(sys.modules[ "__main__" ].settings.getSetting.call_args_list[2][0][0] == "oauth2_access_token")
	
	def test_fetchPage_should_give_up_after_3_tries(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk", "error":"3"})
		
		sys.modules[ "__main__" ].common.log.assert_called_with("giving up ")
	
	def test_fetchPage_should_call_urllib_add_header_id_url_data_is_in_params_collection(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher1 = patch("urllib2.urlopen")
		
		patcher2 = patch("urllib2.Request")
		patcher1.start()
		patcher2.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		dummy_request = Mock()
		urllib2.Request = Mock()
		patcher2(urllib2.Request).return_value = dummy_request
		core = YouTubeCore()
		core._getAuth = Mock()
		ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk", "url_data":{"data":"some_data"}})
		
		args = urllib2.Request.call_args
		patcher1.stop()
		patcher2.stop()
		assert(args[0][0] == 'www.somelink.dk?oauth_token=4')
		assert(args[0][1]== 'data=some_data')
		assert(dummy_request.add_header.call_args[0][1] == 'GoogleLogin auth=my_auth')
		assert(dummy_request.add_header.call_args[0][0] == 'Authorization')
	
	def test_fetchPage_should_set_request_method_to_get_if_request_is_not_in_params_collection(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk"})
		
		patcher1.stop()
		args = YouTubeCore.url2request.call_args
		patcher2.stop()
		assert(args[0][1] == "GET")
	
	def test_fetchPage_should_append_GdataApi_headers_if_request_is_set(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher1 = patch("urllib2.urlopen")
		
		patcher2 = patch("urllib2.Request")
		patcher1.start()
		patcher2.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		dummy_request = Mock()
		urllib2.Request = Mock()
		patcher2(urllib2.Request).return_value = dummy_request
		core = YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk", "request":"some_request"})
		
		patcher1.stop()
		patcher2.stop()
		assert(dummy_request.add_header.call_args_list[0][0][0] == 'X-GData-Client')
		assert(dummy_request.add_header.call_args_list[1][0][0] == 'Content-Type')
		assert(dummy_request.add_header.call_args_list[1][0][1] == 'application/atom+xml')
		assert(dummy_request.add_header.call_args_list[2][0][0] == 'Content-Length')
		assert(dummy_request.add_header.call_args_list[2][0][1] == '12')
		assert(dummy_request.add_header.call_args[0][1] == 'GoogleLogin auth=my_auth')
		assert(dummy_request.add_header.call_args[0][0] == 'Authorization')
			
	def test_fetchPage_should_append_api_key_to_headers_if_api_is_in_params(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		core.APIKEY = "MYKEY"
		
		ret = core._fetchPage({"api":"true", "link":"www.somelink.dk"})
		
		patcher1.stop()
		args = YouTubeCore.url2request().add_header.call_args_list
		patcher2.stop()
		
		assert(args[0][0][0] == 'GData-Version')
		assert(args[0][0][1] == '2')
		assert(args[1][0][0] == "X-GData-Key")
		assert(args[1][0][1] == "key=MYKEY")

	def test_fetchPage_should_append_user_agent_and_no_language_cookie_to_headers_if_api_is_not_in_params(self):
		settings = ["my_auth","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"link":"www.somelink.dk"})
		
		patcher1.stop()
		args = YouTubeCore.url2request().add_header.call_args_list
		patcher2.stop()
		
		assert(args[0][0][0] == 'User-Agent')
		assert(args[0][0][1] == 'Mozilla/5.0 (MOCK)')
		assert(args[1][0][0] == 'Cookie')
		assert(args[1][0][1] == 'PREF=f1=50000000&hl=en')
	
	def test_fetchPage_should_return_error_message_if_login_is_in_params_collection_and_plugin_is_missing_login_info(self):
		settings = ["","","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules[ "__main__" ].language.return_value = "error_message"
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"login":"true","link":"www.somelink.dk"})
		patcher1.stop()
		patcher2.stop()
		
		assert(ret["status"] == 303)
		assert(ret["content"] == "error_message")
		sys.modules[ "__main__" ].language.assert_called_with(30622)
	
	def test_fetchPage_should_fetch_token_from_settings_if_login_is_in_params(self):
		settings = ["my_token","my_token","my_token","my_token","my_token","user","pass","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules[ "__main__" ].language.return_value = "error_message"
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"login":"true","link":"www.somelink.dk"})
		
		patcher1.stop()
		patcher2.stop()
		
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("login_info")
		
	
	def test_fetchPage_should_append_login_token_to_request_headers_if_login_is_in_params(self):
		settings = ["my_token","my_token","my_token","my_token","my_token","user","pass","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules[ "__main__" ].language.return_value = "error_message"
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		
		ret = core._fetchPage({"login":"true","link":"www.somelink.dk"})
		
		patcher1.stop()
		args = YouTubeCore.url2request().add_header.call_args_list
		patcher2.stop()
		
		assert(args[2][0][0] == "Cookie")
		assert(args[2][0][1] == 'LOGIN_INFO=my_token')

	def test_fetchPage_should_call_retry_if_youtube_ask_user_to_verify_age(self):
		settings = ["my_token","my_token","my_token","my_token","my_token","user","pass","4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules[ "__main__" ].language.return_value = "error_message"
		patcher1 = patch("urllib2.urlopen")
		patcher2 = patch("YouTubeCore.url2request")
		patcher1.start()
		patcher2.start()
		import YouTubeCore
		import urllib2
		YouTubeCore.url2request = Mock()
		dummy_connection = Mock()
		read_values = ["Nothing here\n","something verify-age-actions"]
		dummy_connection.read.side_effect = lambda: read_values.pop()
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher1(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore.YouTubeCore()
		core._getAuth = Mock()
		
		params = {"login":"","link":"www.somelink.dk"}
		ret = core._fetchPage(params)
		
		patcher1.stop()
		args = YouTubeCore.url2request().add_header.call_args_list
		patcher2.stop()
		
		assert(dummy_connection.read.call_count == 2)
		
	def test_fetchPage_should_return_content_of_link_and_proper_status_code(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("urllib2.urlopen")
		patcher.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		dummy_connection.geturl.return_value = ""
		dummy_connection.info.return_value = "Mock header"
		patcher(urllib2.urlopen).return_value = dummy_connection
		core = YouTubeCore()
				
		ret = core._fetchPage({ "link": "http://tobiasussing.dk"})
		patcher.stop()
		
		assert(ret['status'] == 200 and ret['content'] == "Nothing here\n")
		
	def test_findErrors_should_use_parseDOM_to_look_for_errormsg_tag(self):
		settings = [ "3"]
		input = { "content": "some_content"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		parsedom = [ ["Mock error [" ] ] # This should probably be updated to something real.
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
		core = YouTubeCore()
		
		result = core._findErrors( input )
		
		sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "class": "errormsg" })
		assert(result == "Mock error")

	def test_findErrors_should_use_parseDOM_to_look_for_error_smaller(self):
		settings = [ "3"]
		input = { "content": "some_content"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		parsedom = [ ["Mock error ["],[] ] # This should probably be updated to something real.
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
		core = YouTubeCore()
		
		result = core._findErrors({"content":"some_content"})
		
		sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "class": "error smaller" })
		assert(result == "Mock error")
		
	def test_findErrors_should_use_parseDOM_to_look_for_unavailable_message(self):
		settings = [ "3"]
		input = { "content": "some_content"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		parsedom = [ ["Mock error ["],[],[] ] # This should probably be updated to something real.
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
		core = YouTubeCore()
		
		result = core._findErrors({"content":"some_content"})
		
		sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "id": "unavailable-message" })
		assert(result == "Mock error")
		
	def test_findErrors_should_use_parseDOM_to_look_for_error_if_content_contains_yt_quota(self):
		settings = [ "3"]
		input = { "content": "some_content yt:quota"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		parsedom = [ ["Mock error ["],[],[],[],[] ] # This should probably be updated to something real.
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x = "",y ="",attrs = {}: parsedom.pop()
		core = YouTubeCore()
		
		result = core._findErrors(input)
		
		assert(sys.modules[ "__main__" ].common.parseDOM.call_args_list[3][0][0] == input["content"])
		assert(sys.modules[ "__main__" ].common.parseDOM.call_args_list[3][0][1] == 'error')
		sys.modules[ "__main__" ].common.parseDOM.assert_called_with([], 'code')
		assert(result == "Mock error")

	def test_findErrors_should_return_if_error_found(self):
		settings = [ "3"]
		input = { "content": "some_content"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		parsedom = [ ["Mock error [" ] ] # This should probably be updated to something real.
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
		core = YouTubeCore()
		
		result = core._findErrors( input )
		
		assert(result == "Mock error")
	
	def ttest_verifyAge_should_work_at_some_point(self):
		assert(False)

	def test_oRefreshToken_should_reset_access_token_before_calling_fetch_page(self):
		settings = [ "","some_token","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"status":303,"content":"fail"}
		
		result = core._oRefreshToken()
		
		sys.modules[ "__main__" ].settings.setSetting.assert_called_with("oauth2_access_token","")

	def test_oRefreshToken_should_fetch_refresh_token_from_settings(self):
		settings = [ "","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		
		result = core._oRefreshToken()
		
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("oauth2_refresh_token")

	def test_oRefreshToken_should_fetchPage_with_correct_params(self):
		settings = [ "","some_token","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"status":303,"content":"fail"}
		
		result = core._oRefreshToken()
		
		assert(core._fetchPage.call_args[0][0]["link"] == "https://accounts.google.com/o/oauth2/token")
		assert(core._fetchPage.call_args[0][0].has_key("url_data"))

	def test_oRefreshToken_should_pars_token_json_structure_correctly(self):
		settings = [ "","some_token","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"status":200,"content":'{"access_token":""}'}
		
		result = core._oRefreshToken()
		
		sys.modules[ "__main__" ].settings.setSetting.assert_called_with("oauth2_access_token","")

	def test_oRefreshToken_should_log_error_if_invalid_json_structure_is_returned(self):
		settings = [ "","some_token","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		output = {"status":200,"content":'{"access_token"][sdlkfjfksldf"super_secrect_token"[}]'}
		core._fetchPage.return_value = output
		
		result = core._oRefreshToken()
		
		sys.modules[ "__main__" ].common.log.assert_called_with(repr(output))

	def test_oRefreshToken_should_set_access_token_if_found(self):
		settings = [ "","some_token","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"status":200,"content":'{"access_token":"super_secrect_token"}'}
		
		result = core._oRefreshToken()
		
		sys.modules[ "__main__" ].settings.setSetting.assert_called_with("oauth2_access_token","super_secrect_token")
			
	def test_getAuth_should_check_token_expiration_before_calling_refresh_token(self):
		settings = [ "","some_token","3249320480292","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._oRefreshToken = Mock()
		
		result = core._getAuth()
		
		assert(sys.modules[ "__main__" ].settings.getSetting.call_args_list[2][0][0] == "oauth2_expires_at")
	
	def test_getAuth_should_call_oRefreshToken_to_refresh_token(self):
		settings = [ "","some_token","2","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._oRefreshToken = Mock()
		
		result = core._getAuth()
		
		core._oRefreshToken.assert_called_with()
	
	def test_getAuth_should_fetch_token_from_settings(self):
		settings = [ "","","32342498270492","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._oRefreshToken = Mock()
		sys.modules[ "__main__" ].login.login.return_value = ("",200)
		
		result = core._getAuth()
		
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("oauth2_access_token")
	
	def ttest_getAuth_should_call_login_if_token_isnt_found(self):
		settings = [ "","","","3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules[ "__main__" ].login.login.return_value = ("",200)
		core = YouTubeCore()
		core._oRefreshToken = Mock()
		
		result = core._getAuth()
		
		sys.modules[ "__main__" ].login.login.assert_called_with()
		sys.modules[ "__main__" ].settings.getSetting.assert_called_with("oauth2_access_token")

	def test_getNodeAttribute_should_parse_node_structure_correctly(self):
		settings = ["3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		node = Mock()
		
		node.getElementsByTagName
		result = core._getNodeAttribute(node, "tag","attribute","default")
		
		node.getElementsByTagName.assert_called_with("tag")
		node.getElementsByTagName().item.assert_called_with(0)
		node.getElementsByTagName().item().hasAttribute.assert_called_with("attribute")
		node.getElementsByTagName().item().getAttribute.assert_called_with("attribute")
		
	def test_getNodeValue_should_parse_node_structure_correctly(self):
		settings = ["3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		node = Mock()
		node.getElementsByTagName().item().firstChild.nodeValue = 5
		
		node.getElementsByTagName
		result = core._getNodeValue(node, "tag","default")
		
		node.getElementsByTagName.assert_called_with("tag")
		node.getElementsByTagName().item.assert_called_with(0)
		assert(result == 5)
		
	def test_getVideoInfo_should_call_minidom_getElementsByTagName_to_find_links(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("xml.dom.minidom.parseString")
		patcher.start()
		import xml.dom.minidom
		dom = Mock()
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString.return_value = dom
		dom.getElementsByTagName.return_value = ""
		core = YouTubeCore()
		
		result = core.getVideoInfo("xml", {})
		patcher.stop()
		
		args = dom.getElementsByTagName.call_args_list
		assert(args[0][0][0] == "link")

	def test_getVideoInfo_should_call_minidom_getElementsByTagName_to_find_entries(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("xml.dom.minidom.parseString")
		patcher.start()
		import xml.dom.minidom
		dom = Mock()
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString.return_value = dom
		dom.getElementsByTagName.return_value = ""
		core = YouTubeCore()
		
		result = core.getVideoInfo("xml", {})
		patcher.stop()
		
		args = dom.getElementsByTagName.call_args_list
		assert(args[1][0][0] == "entry")
		assert(args[2][0][0] == "atom:entry")

	def test_getVideoInfo_should_search_links_for_next_page_indicator(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		patcher = patch("xml.dom.minidom.parseString")
		patcher.start()
		import xml.dom.minidom
		dom = Mock()
		link = Mock()
		tags = ["","", [link]]
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString.return_value = dom
		dom.getElementsByTagName.side_effect = lambda x: tags.pop()
		core = YouTubeCore()
		link.attributes.get.value.return_value = "next"
		
		result = core.getVideoInfo("xml", {})
		patcher.stop()
		
		link.attributes.get.assert_called_with("rel")
	
	def mock_setup_getVideoInfo_full_run(self):
		self.my_core = ""
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		self.dompatcher = patch("xml.dom.minidom.parseString")
		self.dompatcher.start()
		import xml.dom.minidom
		sys.modules["__main__"].storage.retrieveValue.return_value = "1"
		self.testing_dom = Mock()
		xml.dom.minidom.parseString = Mock()
		xml.dom.minidom.parseString.return_value = self.testing_dom
		self.entry = Mock()
		self.edit_link = Mock()
		link_attributes = ["","some_link/some_id","edit"]
		self.edit_link.getAttribute.side_effect = lambda x: link_attributes.pop()
		entry_elements = ["","","","","","","","","",[self.edit_link],Mock(),Mock(),""]
		self.entry.getElementsByTagName.side_effect = lambda x ="",y = "",z = "": entry_elements.pop()
		elements = [[self.entry],[]]
		self.testing_dom.getElementsByTagName.side_effect = lambda x ="",y = "",z = "": elements.pop() 
		self.my_core = YouTubeCore()
		self.my_core._getNodeValue = Mock()
		nodes = ["","","","","","","","","","","","","2011-09-11T12:00:00","","","","false"]
		self.my_core._getNodeValue.side_effect = lambda x ="",y = "",z = "": nodes.pop()
		self.my_core._getNodeAttribute = Mock() 
		attributes = ["","","","","","","","","","","","","","1","2.0","1","","","/some_video_id"] 
		self.my_core._getNodeAttribute.side_effect = lambda x ="",y = "",z = "", v = "": attributes.pop() 
		
	def test_getVideoInfo_should_call_getNodeValue_to_get_video_id(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeValue.call_args_list
		assert(args[0][0][1] == "yt:videoid")
		assert(args[0][0][2] == "false")

	def test_getVideoInfo_should_call_getNodeValue_to_get_Title(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeValue.call_args_list
		assert(args[2][0][1] == "media:title")
		assert(args[2][0][2] == "Unknown Title")

	def test_getVideoInfo_should_call_getNodeValue_to_get_Plot(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeValue.call_args_list
		assert(args[3][0][1] == 'media:description')
		assert(args[3][0][2] == "Unknown Plot")

	def test_getVideoInfo_should_call_getNodeValue_to_get_Date(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeValue.call_args_list
		assert(args[4][0][1] == 'published')
		assert(args[4][0][2] == "Unknown Date")

	def test_getVideoInfo_should_call_getNodeValue_to_get_user(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeValue.call_args_list
		assert(args[5][0][1] == 'name')
		assert(args[5][0][2] == "Unknown Name")

	def test_getVideoInfo_should_call_getNodeValue_to_get_Studio(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeValue.call_args_list
		assert(args[6][0][1] == 'media:credit')
		assert(args[6][0][2] == "")
		assert(args[7][0][1] == 'name')
		assert(args[7][0][2] == "Unknown Uploader")
		
	def test_getVideoInfo_should_call_getNodeAttribute_to_get_Duration(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeAttribute.call_args_list
		assert(args[3][0][1] == 'yt:duration')
		assert(args[3][0][2] == "seconds")
		assert(args[3][0][3] == "0")

	def test_getVideoInfo_should_call_getNodeAttribute_to_get_Rating(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeAttribute.call_args_list
		assert(args[4][0][1] == 'gd:rating')
		assert(args[4][0][2] == "average")
		assert(args[4][0][3] == "0.0")

	def test_getVideoInfo_should_call_getNodeAttribute_to_get_view_Count(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeAttribute.call_args_list
		assert(args[5][0][1] == 'yt:statistics')
		assert(args[5][0][2] == "viewCount")
		assert(args[5][0][3] == "0")

	def test_getVideoInfo_should_call_getNodeValue_to_get_Genre(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeAttribute.call_args_list
		assert(args[6][0][1] == 'media:category')
		assert(args[6][0][2] == "label")
		assert(args[6][0][3] == "Unknown Genre")

	def test_getVideoInfo_should_add_date_to_plot(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeAttribute.call_args_list
		assert(result[0]["Plot"].find("2011-09-11 12:00:00") > 0)
		

	def test_getVideoInfo_should_add_view_count_to_plot(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.my_core._getNodeAttribute.call_args_list
		assert(result[0]["Plot"].find("View count: 1") > 0)

	def test_getVideoInfo_should_call_getNodeValue_to_search_for_edit_id(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()
		args = self.entry.getElementsByTagName.call_args_list
		assert(args[3][0][0] == "link")
		assert(result[0]["Plot"].find("View count: 1") > 0)
		args = self.edit_link.getAttribute.call_args_list
		assert(args[0][0][0] == "rel")
		assert(args[1][0][0] == "href")
		assert(result[0]["editid"] == "some_id")
		
	def test_getVideoInfo_should_call_storage_retrieveValue_to_get_watch_status(self):
		self.mock_setup_getVideoInfo_full_run()
		
		result = self.my_core.getVideoInfo("xml", {})
		
		self.dompatcher.stop()

		sys.modules["__main__"].storage.retrieveValue.assert_called_with("vidstatus-false")
		
	def test_getVideoInfo_should_parse_youtube_xml(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules[ "__main__" ].storage.retrieveValue.return_value = "7"
		core = YouTubeCore()
		
		result = core.getVideoInfo(self.readTestInput("youtubeFavoritesFeed.xml", False))
		
		print repr(result[0])
		assert(result[0]["Overlay"] == 7)
		assert(result[0]["editid"] == 'some_edit_id')
		assert(result[0]["Title"] == "Aurora seen from the ISS in Orbit")
		assert(result[0]["playlist_entry_id"] == 'some_edit_id')
		assert(result[0]["Rating"] > 4.9)
		assert(result[0]["videoid"] == 'ogtKe7N05F0')
		assert(result[0]["Duration"] == "00:35")
		assert(result[0]["Genre"] == "Science & Technology")
		assert(result[0]["Studio"] == "isoeph")
		assert(result[0]["user"] == "some_user")
		assert(result[0]["Date"] == "29-09-2011")
		assert(result[0]["thumbnail"] == "http://i.ytimg.com/vi/ogtKe7N05F0/0.jpg")
				
		
		

if __name__ == "__main__":
	nose.runmodule()