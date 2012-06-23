import nose
import BaseTestCase
from mock import Mock, patch
import sys
import datetime
from YouTubeCore import YouTubeCore

class TestYouTubeCore(BaseTestCase.BaseTestCase):

    def setUp(self):
        super(self.__class__,self).setUp()
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3","4", "my_auth"]
        sys.modules[ "__main__" ].storage.retrieve.return_value = "some_thumbnail"
        sys.modules[ "__main__" ].language.return_value = "error_message"
        sys.modules[ "__main__" ].common.parseDOM.return_value = []
        sys.modules[ "__main__" ].common.replaceHTMLCodes.return_value = "SomeHTMLFreeString"
        sys.modules[ "__main__" ].common.makeUTF8.return_value = "SomeUTF8EncodedString"
	
    def test_delete_favorite_should_call_fetchPage_with_correct_fetch_options(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"success", "status":200}
        delete_url = "http://gdata.youtube.com/feeds/api/users/default/favorites/test"

        core.delete_favorite({ "editid": "test" })
                
        assert(core._fetchPage.called)
        assert(core._fetchPage.call_count == 1)
        core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

    def test_remove_contact_should_call_fetchPage_with_correct_fetch_options(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"success", "status":200}
        delete_url = "http://gdata.youtube.com/feeds/api/users/default/contacts/come_contact"        

        core.remove_contact({ "contact": "come_contact" })
        
        assert(core._fetchPage.called)
        assert(core._fetchPage.call_count == 1)
        core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

    def test_remove_subscription_should_call_fetchPage_with_correct_fetch_options(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"success", "status":200}
        delete_url = "http://gdata.youtube.com/feeds/api/users/default/subscriptions/edit_id"        

        core.remove_subscription({ "editid": "edit_id" })
        
        assert(core._fetchPage.called)
        assert(core._fetchPage.call_count == 1)
        core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

    def test_add_contact_should_call_fetchPage_with_correct_fetch_options(self):
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
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"success", "status":200}
        url = "http://gdata.youtube.com/feeds/api/users/default/playlists/some_playlist"
        
        core.del_playlist({ "playlist": "some_playlist"})
        
        assert(core._fetchPage.called)
        assert(core._fetchPage.call_count == 1)
        core._fetchPage.assert_called_with({"link": url, "api": "true", "login": "true", "auth": "true","method":"DELETE"})

    def test_add_to_playlist_should_call_fetchPage_with_correct_fetch_options(self):
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
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"success", "status":200}
        url = "http://gdata.youtube.com/feeds/api/playlists/some_playlist/some_entry_id"
        
        core.remove_from_playlist({ "playlist": "some_playlist","playlist_entry_id":"some_entry_id"})
        
        assert(core._fetchPage.called)
        assert(core._fetchPage.call_count == 1)
        core._fetchPage.assert_called_with({"link": url, "api": "true", "login": "true", "auth": "true","method":"DELETE"})

    def test_remove_from_watch_later_should_call_fetchPage_with_correct_fetch_options(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"success", "status":200}
        url = "https://gdata.youtube.com/feeds/api/users/default/watch_later/some_entry_id"
        
        core.remove_from_watch_later({ "playlist": "some_playlist","playlist_entry_id":"some_entry_id"})
        
        assert(core._fetchPage.called)
        assert(core._fetchPage.call_count == 1)
        core._fetchPage.assert_called_with({"link": url, "api": "true", "login": "true", "auth": "true","method":"DELETE"})
        
	
    def test_getCategoriesFolderInfo_should_set_item_params_correctly_for_contacts_feed(self):
        input = self.readTestInput("categories-test.xml", False)
        core = YouTubeCore()
        sys.modules["__main__"].common.parseDOM.side_effect = [["entries"], [], ["Film & Animation"], ["Film"]]
        
        result = core.getCategoriesFolderInfo(input, {"feed":"feed_categories"})
        
        assert(len(result) > 0)
        assert(result[0]["thumbnail"] == "explore")
        assert(result[0]["Title"] == "Film & Animation")
        assert(result[0]["category"] == "Film")
        
    def test_getCategoriesFolderInfo_should_use_parseDOM_to_look_for_categories(self):
        core = YouTubeCore()
        sys.modules["__main__"].common.parseDOM.side_effect = [["entries"], [], ["label"], ["term"]]

        core.getCategoriesFolderInfo("xml", {})
        
        sys.modules["__main__"].common.parseDOM.assert_any_call('entries', 'atom:category', ret="label")
	
    def test_getCategoriesFolderInfo_should_use_parseDOM_to_look_for_deprecated_categories(self):
        core = YouTubeCore()
        sys.modules["__main__"].common.parseDOM.side_effect = [["entries"], ["dep"]]

        core.getCategoriesFolderInfo("xml", {})
                        
        sys.modules["__main__"].common.parseDOM.assert_any_call('entries', 'yt:deprecated')
        
    def test_getCategoriesFolderInfo_should_skip_deprecated_categories(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["entries"], ["depcrecated"], ["label"], ["term"]]
        core = YouTubeCore()

        result = core.getCategoriesFolderInfo("xml", {})
        
        calls = sys.modules["__main__"].common.parseDOM.call_args_list #assert_any_call('entries', 'yt:deprecated')
        print repr(calls)
        assert(len(calls) == 2)

    def test_getFolderInfo_should_use_getElementsByTagName_to_look_for_link_and_entries(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], [""], ["title"], ["published"], ["id"]]
        core = YouTubeCore()

        core.getFolderInfo("xml", {})
        
        calls = sys.modules["__main__"].common.parseDOM.call_args_list
        print repr(calls)

        assert(calls[0][0][1] == "entry")
        assert(calls[1][0][1] == "link")

    def test_getFolderInfo_should_search_links_relation_attribute_for_multiple_pages(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], ["next"], ["title"], ["published"], ["id"]]
        sys.modules["__main__"].common.parseDOM.side_effect = [[], ["next"]]
        core = YouTubeCore()
        
        core.getFolderInfo("xml", {})

        sys.modules["__main__"].utils.addNextFolder.assert_called_with([], {})
	
    def test_getFolderInfo_should_find_edit_id_in_xml_structure_if_id_tag_is_present(self):
        input = self.readTestInput("getFolderInfoPlaylistTest.xml", False)
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], [], ["title"], ["published"], ["some_playlist_id"]]
        core = YouTubeCore()
        
        result = core.getFolderInfo(input, {})

        assert(result[0]["editid"] == "some_playlist_id")


    def test_getFolderInfo_should_set_item_params_correctly_for_contacts_feed(self):
        input = self.readTestInput("getFolderInfoContactTest.xml", False)
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], [], ["some_other_user"], ["published"], ["some_other_user"]]
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
        input = self.readTestInput("getFolderInfoSubscriptionsTest.xml", False)
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], [], ["GoogleTechTalks"], ["published"], ["some_edit_id"]]
        core = YouTubeCore()
        
        result = core.getFolderInfo(input, {"user_feed":"subscriptions"})
        
        assert(result[0]["editid"] == "some_edit_id")
        assert(result[0]["thumbnail"] == "some_thumbnail")
        assert(result[0]["login"] == "true")
        assert(result[0]["channel"] == "GoogleTechTalks")
        assert(result[0]["Title"] == "GoogleTechTalks")
        
    def test_getFolderInfo_should_set_item_params_correctly_for_playlist_feed(self):
        input = self.readTestInput("getFolderInfoPlaylistTest.xml", False)
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], [], ["Stand back I'm going to try Science!"], ["published"], ["some_playlist_id"], ["some_playlist_id"]]
        core = YouTubeCore()
        
        result = core.getFolderInfo(input, {"user_feed":"playlists"})
        
        assert(result[0]["editid"] == "some_playlist_id")
        assert(result[0]["thumbnail"] == "some_thumbnail")
        assert(result[0]["login"] == "true")
        assert(result[0]["playlist"] == "some_playlist_id")
        assert(result[0]["user_feed"] == "playlist")
        assert(result[0]["Title"] == "Stand back I'm going to try Science!")

    def test_getFolderInfo_should_call_storage_retrieve_to_find_thumbnail(self):
        input = self.readTestInput("getFolderInfoPlaylistTest.xml", False)
        sys.modules["__main__"].common.parseDOM.side_effect = [["entry"], [], ["Stand back I'm going to try Science!"], ["published"], ["some_playlist_id"], ["some_playlist_id"]]
        core = YouTubeCore()
        
        result = core.getFolderInfo(input, {})

        assert(sys.modules["__main__"].storage.retrieve.call_count == 1)
	
    def test_getFolderInfo_should_call_utils_addNextFolder_to_set_default_next_folder_on_feed(self):
        sys.modules["__main__"].common.parseDOM.side_effect = [[], ["next"]]
        core = YouTubeCore()
        
        core.getFolderInfo("xml", {})

        sys.modules["__main__"].utils.addNextFolder.assert_called_with([], {})
        
    def test_getBatchDetailsOverride_should_call_getBatchDetails_with_list_of_video_ids(self):
        core = YouTubeCore()
        core.getBatchDetails = Mock()
        core.getBatchDetails.return_value = ([{"videoid":"some_id3"},{"videoid":"some_id2"},{"videoid":"some_id1"}], 200)
        items = [{"videoid":"some_id1","some_key1":"value1"},{"videoid":"some_id2","some_key2":"value2"}, {"videoid":"some_id3","some_key3":"value3"}]
        
        (result, status) = core.getBatchDetailsOverride(items, params={})
        
        core.getBatchDetails.assert_called_with(['some_id1', 'some_id2', 'some_id3'], {})

    def test_getBatchDetailsOverride_should_override_specified_properties_in_output_from_getBatchDetails(self):
        core = YouTubeCore()
        core.getBatchDetails = Mock()
        core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"},{"videoid":"some_id1","some_key1":"blabla"}], 200)
        items = [{"videoid":"some_id1","some_key1":"value1"},{"videoid":"some_id2","some_key2":"value2"}, {"videoid":"some_id3","some_key3":"value3"}]
        
        (result, status) = core.getBatchDetailsOverride(items, params={})
        
        assert(result[0]["some_key3"] == "value3")
        assert(result[1]["some_key2"] == "value2")
        assert(result[2]["some_key1"] == "value1")

    def test_getBatchDetailsThumbnails_should_call_getBatchDetails_with_list_of_video_ids(self):
        core = YouTubeCore()
        core.getBatchDetails = Mock()
        core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"},{"videoid":"some_id1","some_key1":"blabla"}], 200)
        items = [("some_id3","some_thumb3"),("some_id2","some_thumb2"),("some_id1","some_thumb1")]
        
        (result, status) = core.getBatchDetailsThumbnails(items, params={})
        
        core.getBatchDetails.assert_called_with(['some_id3', 'some_id2', 'some_id1'], {})
        
    def test_getBatchDetailsThumbnails_should_override_thumbnails_in_output_from_getBatchDetails(self):
        core = YouTubeCore()
        core.getBatchDetails = Mock()
        core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"},{"videoid":"some_id1","some_key1":"blabla"}], 200)
        items = [("some_id3","some_thumb3"),("some_id2","some_thumb2"),("some_id1","some_thumb1")]
        
        (result, status) = core.getBatchDetailsThumbnails(items, params={})
        
        assert(result[0]["thumbnail"] == "some_thumb3")
        assert(result[1]["thumbnail"] == "some_thumb2")
        assert(result[2]["thumbnail"] == "some_thumb1")
        
    def test_getBatchDetailsThumbnails_should_fill_out_missing_videos_in_collection_from_getBatchDetails_to_maintain_collection_size(self):
        core = YouTubeCore()
        core.getBatchDetails = Mock()
        core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"}], 200)
        items = [("some_id3","some_thumb3"),("some_id2","some_thumb2"),("some_id1","some_thumb1")]
        
        (result, status) = core.getBatchDetailsThumbnails(items, params={})
        
        assert(result[0]["thumbnail"] == "some_thumb3")
        assert(result[1]["thumbnail"] == "some_thumb2")
        assert(result[2]["videoid"] == "false")

    def test_getBatchDetailsOverride_should_fill_out_missing_videos_in_collection_from_getBatchDetails_to_maintain_collection_size(self):
        core = YouTubeCore()
        core.getBatchDetails = Mock()
        core.getBatchDetails.return_value = ([{"videoid":"some_id3","some_key3":"blabla"},{"videoid":"some_id2","some_key2":"blabla"}], 200)
        items = [{"videoid":"some_id1","some_key1":"value1"},{"videoid":"some_id2","some_key2":"value2"}, {"videoid":"some_id3","some_key3":"value3"}]
        
        (result, status) = core.getBatchDetailsOverride(items, params={})
        
        assert(result[0]["some_key3"] == "value3")
        assert(result[1]["some_key2"] == "value2")
        assert(result[2]["videoid"] == "false")
        
    def test_getBatchDetails_should_call_cache_getMulti_before_hitting_youtube(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        
        core.getBatchDetails([],{})
        
        sys.modules["__main__"].cache.getMulti.assert_called_with('videoidcache', [])

    def test_getBatchDetails_should_not_request_video_information_for_cached_videos(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core.getVideoInfo = Mock()
        core.getVideoInfo.return_value = []
        core._fetchPage.return_value = {"content":"","status":303}
        sys.modules["__main__"].cache.getMulti.return_value = ['{"videoid":"some_id_1"}',"","","",'{"videoid":"some_id_5"}']
        
        core.getBatchDetails(["some_id_1","some_id_2","some_id_3","some_id_4","some_id_5"],{})
        
        request = core._fetchPage.call_args_list[0][0][0]["request"]
        assert(request.find("some_id_1") < 0)
        assert(request.find("some_id_5") < 0)
	
    def test_getBatchDetails_should_at_most_request_50_videos_in_one_call(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core.getVideoInfo = Mock()
        core.getVideoInfo.return_value = []
        core._fetchPage.return_value = {"content":"","status":303}
        sys.modules["__main__"].cache.getMulti.return_value = []
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
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"content":"","status":303}
        core.getVideoInfo = Mock()
        core.getVideoInfo.return_value = []
        sys.modules["__main__"].cache.getMulti.return_value = []
        sys.modules["__main__"].common.parseDOM.return_value = ""
        ids = []
        i= 1
        while i < 52:
        	ids.append("some_id_"  + str(i))
        	i += 1
        
        core.getBatchDetails(ids,{})
        
        sys.modules["__main__"].common.parseDOM.assert_called_with("","batch:status",ret="code")

    def test_getBatchDetails_should_sleep_for_5_seconds_if_youtube_returns_error(self):
        patcher = patch("time.sleep")
        patcher.start()
        import time
        time.sleep = Mock()         
        core = YouTubeCore()
        core._fetchPage = Mock()
        core.getVideoInfo = Mock()
        core.getVideoInfo.return_value = []
        core._fetchPage.return_value = {"content":"","status":303}
        sys.modules["__main__"].cache.getMulti.return_value = []
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
        core = YouTubeCore()
        core._fetchPage = Mock()
        core.getVideoInfo = Mock()
        core.getVideoInfo.return_value = []
        core._fetchPage.return_value = {"content":"some_content","status":303}
        sys.modules["__main__"].cache.getMulti.return_value = ['{"videoid":"some_id_1"}',"","","",'{"videoid":"some_id_5"}']
        
        core.getBatchDetails(["some_id_1","some_id_2","some_id_3","some_id_4","some_id_5"],{"param":"some_params"})
        
        core.getVideoInfo.assert_called_with("some_content",{"param":"some_params"})
        
    def test_getBatchDetails_should_handle_collection_sizes_above_50(self):
        core = YouTubeCore()
        core._fetchPage = Mock()
        core.getVideoInfo = Mock()
        core.getVideoInfo.return_value = []
        core._fetchPage.return_value = {"content":"","status":303}
        sys.modules["__main__"].cache.getMulti.return_value = []
        sys.modules["__main__"].common.parseDOM.return_value = ""
        ids = []
        i= 1
        while i < 75:
        	ids.append("some_id_"  + str(i))
        	i += 1
        
        core.getBatchDetails(ids,{})
        
        assert(core._fetchPage.call_count == 2)
        	
    def test_fetchPage_should_return_error_status_and_empty_content_if_no_params_are_provided(self):
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
        sys.modules[ "__main__" ].settings.getSetting.side_effect = [ "3", "", "", "4", "my_token", "false", "my_token" ]
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
        sys.modules[ "__main__" ].settings.getSetting.side_effect = [ "3", "", "", "4", "my_token", "false", "my_token" ]
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
        sys.modules[ "__main__" ].settings.getSetting.assert_any_call("oauth2_access_token")
	
    def test_fetchPage_should_give_up_after_3_tries(self):
        core = YouTubeCore()
        core._getAuth = Mock()
        
        ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk", "error":"3"})
        
        sys.modules[ "__main__" ].common.log.assert_called_with("giving up")

    def test_fetchPage_should_properly_handle_quota(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3","4","", "", "false", "", "false", "", "", "", "", "", "", "", ""]
        patcher1 = patch("urllib2.urlopen")
        patcher2 = patch("time.sleep")
        patcher1.start()
        patcher2.start()

        import urllib2
        import time
        time.sleep = Mock()
        fp = Mock()
        fp.read.return_value = "<?xml version='1.0' encoding='UTF-8'?><errors><error><domain>yt:quota</domain><code>too_many_recent_calls</code></error></errors>"
        dummy_connection = Mock()
        dummy_connection.read.side_effect = urllib2.HTTPError("",403,"BOOM forbidden","",fp)
        patcher1(urllib2.urlopen).return_value = dummy_connection

        core = YouTubeCore()
        core._getAuth = Mock()
	
        ret = core._fetchPage({"auth":"true", "link":"www.somelink.dk"})

        patcher1.stop()

        time.sleep.assert_called_with(100)
        patcher2.stop()

        sys.modules[ "__main__" ].common.log.assert_any_call("Hit quota... sleeping for 100 seconds")
	
    def test_fetchPage_should_call_urllib_add_header_id_url_data_is_in_params_collection(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3","4","4", "false", "my_auth"]
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
        print repr(args)
        assert(args[0][0] == 'www.somelink.dk?oauth_token=4')
        assert(args[0][1]== 'data=some_data')
        #assert(dummy_request.add_header.call_args[0][1] == 'GoogleLogin auth=my_auth')
        #assert(dummy_request.add_header.call_args[0][0] == 'Authorization')
	
    def test_fetchPage_should_set_request_method_to_get_if_request_is_not_in_params_collection(self):
        sys.modules[ "__main__" ].settings.getSetting = Mock()
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3","4","false","false", "false", "false"]

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
        sys.modules[ "__main__" ].settings.getSetting.side_effect = [ "3", "4", "my_token", "false", "my_auth" ]
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
        #assert(dummy_request.add_header.call_args[0][1] == 'GoogleLogin auth=my_auth')
        #assert(dummy_request.add_header.call_args[0][0] == 'Authorization')
        	
    def test_fetchPage_should_append_api_key_to_headers_if_api_is_in_params(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3", "4", "", "", "false", ""]
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
        assert(args[0][0][1] == '2.1')
        assert(args[1][0][0] == "X-GData-Key")
        assert(args[1][0][1] == "key=MYKEY")

    def test_fetchPage_should_append_user_agent_and_no_language_cookie_to_headers_if_api_is_not_in_params(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3", "4", "", "", "false", ""]
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
        
        print repr(args)

        assert(args[0][0][0] == 'User-Agent')
        assert(args[0][0][1] == 'Mozilla/5.0 (MOCK)')
        assert(args[1][0][0] == 'Cookie')
        assert(args[1][0][1] == 'PREF=f1=50000000&hl=en;')
	
    def test_fetchPage_should_return_error_message_if_login_is_in_params_collection_and_plugin_is_missing_login_info(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = ["3", "4", "", "", "false", ""]
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
        settings = ["my_token", "my_token", "my_token", "my_token", "my_token", "user", "pass", "4", "", "", "3"]
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
        
        ret = core._fetchPage({"login":"true","link":"www.somelink.dk"})
        
        patcher1.stop()
        patcher2.stop()
        
        sys.modules[ "__main__" ].settings.getSetting.assert_any_call("SID")
        sys.modules[ "__main__" ].settings.getSetting.assert_any_call("login_info")
        
	
    def test_fetchPage_should_append_login_token_to_request_headers_if_login_is_in_params(self):
        settings = ["my_token", "my_token", "my_token", "my_token", "my_token", "user", "pass", "4", "", "", "3"]
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
        
        ret = core._fetchPage({"login":"true","link":"www.somelink.dk"})
        
        patcher1.stop()
        args = YouTubeCore.url2request().add_header.call_args_list
        patcher2.stop()
        
        print repr(args)
        assert(args[1][0][0] == "Cookie")
        assert(args[1][0][1] == 'PREF=f1=50000000&hl=en;LOGIN_INFO=my_token;SID=my_token;')

    def test_fetchPage_should_call_retry_if_youtube_ask_user_to_verify_age(self):
        settings = [ "3", "", "", "4", "false", "false", "false", "user", "pass", "my_token","my_token","my_token","my_token","my_token" ] 
        sys.modules[ "__main__" ].settings.getSetting.side_effect = settings
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
	
    def test_fetchPage_should_retry_on_URLError(self):
        settings = ["my_token", "my_token", "my_token", "my_token", "my_token", "user", "pass", "4", "", "", "3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        patcher1 = patch("urllib2.urlopen")
        patcher2 = patch("YouTubeCore.url2request")
        patcher3 = patch("time.sleep")
        patcher1.start()
        patcher2.start()
        patcher3.start()
        import YouTubeCore
        import urllib2
        import time
        time.sleep = Mock()
        YouTubeCore.url2request = Mock()
        dummy_connection = Mock()
        read_values = ["Nothing here\n","something verify-age-actions"]
        dummy_connection.read.side_effect = urllib2.URLError("Boom")
        patcher1(urllib2.urlopen).return_value = dummy_connection
        core = YouTubeCore.YouTubeCore()
        core._getAuth = Mock()
        
        params = {"login":"","link":"www.somelink.dk"}
        ret = core._fetchPage(params)
        
        patcher1.stop()
        args = YouTubeCore.url2request().add_header.call_args_list
        patcher2.stop()
        patcher3.stop()
        assert(params["error"] == 3)
        
    def test_fetchPage_should_refresh_token_on_invalid_token_HTTPError(self):
        settings = ["my_token", "my_token", "my_token", "my_token", "my_token", "user", "pass", "4", "", "", "3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        patcher1 = patch("urllib2.urlopen")
        patcher2 = patch("YouTubeCore.url2request")
        patcher3 = patch("time.sleep")
        patcher1.start()
        patcher2.start()
        patcher3.start()
        import YouTubeCore
        import urllib2
        import time
        time.sleep = Mock()
        YouTubeCore.url2request = Mock()
        fp = Mock()
        fp.read.return_value = "something"
        dummy_connection = Mock()
        read_values = ["Nothing here\n","something verify-age-actions"]
        dummy_connection.read.side_effect = urllib2.HTTPError("",400,"BOOM Token invalid","",fp)
        patcher1(urllib2.urlopen).return_value = dummy_connection
        core = YouTubeCore.YouTubeCore()
        core._oRefreshToken = Mock()
        core._getAuth = Mock()
        
        params = {"login":"","link":"www.somelink.dk"}
        ret = core._fetchPage(params)
        
        patcher1.stop()
        args = YouTubeCore.url2request().add_header.call_args_list
        patcher2.stop()
        patcher3.stop()
        
        core._oRefreshToken.assert_any_call()
        
    def test_fetchPage_should_log_content_on_HTTPError_if_no_known_reason_is_found(self):
        settings = ["my_token", "my_token", "my_token", "my_token", "my_token", "user", "pass", "4", "", "", "3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        patcher1 = patch("urllib2.urlopen")
        patcher2 = patch("YouTubeCore.url2request")
        patcher1.start()
        patcher2.start()
        import YouTubeCore
        import urllib2
        YouTubeCore.url2request = Mock()
        fp = Mock()
        fp.read.return_value = "something"
        dummy_connection = Mock()
        read_values = ["Nothing here\n","something verify-age-actions"]
        dummy_connection.read.side_effect = urllib2.HTTPError("",400,"BOOM","",fp)
        patcher1(urllib2.urlopen).return_value = dummy_connection
        core = YouTubeCore.YouTubeCore()
        core._oRefreshToken = Mock()
        core._getAuth = Mock()
        
        params = {"login":"","link":"www.somelink.dk"}
        ret = core._fetchPage(params)
        
        patcher1.stop()
        args = YouTubeCore.url2request().add_header.call_args_list
        patcher2.stop()
        
        fp.read.assert_any_call()
        
    def test_fetchPage_should_sleep_for_10_seconds_on_HTTPError_if_rate_limit_reason_is_found(self):
        settings = ["my_token","my_token","my_token","my_token","my_token","user","pass","4", "", "", "3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        patcher1 = patch("urllib2.urlopen")
        patcher2 = patch("YouTubeCore.url2request")
        patcher3 = patch("time.sleep")
        patcher1.start()
        patcher2.start()
        patcher3.start()
        import YouTubeCore
        import urllib2
        import time
        YouTubeCore.url2request = Mock()
        fp = Mock()
        fp.read.return_value = "something"
        sleep = Mock()
        time.sleep = sleep         
        dummy_connection = Mock()
        read_values = ["Nothing here\n","something verify-age-actions"]
        dummy_connection.read.side_effect = urllib2.HTTPError("",400,"BOOM User Rate Limit Exceeded","",fp)
        patcher1(urllib2.urlopen).return_value = dummy_connection
        core = YouTubeCore.YouTubeCore()
        core._oRefreshToken = Mock()
        core._getAuth = Mock()
        
        params = {"login":"","link":"www.somelink.dk"}
        ret = core._fetchPage(params)
        
        patcher1.stop()
        args = time.sleep.call_args_list
        patcher2.stop()
        patcher3.stop()
        
        sleep.assert_any_call(10)
	
    def test_fetchPage_should_return_content_of_link_and_proper_status_code(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = [ "3", "4", "false", "", ""]
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
        
    def test_fetchPage_should_add_proxy_when_forced_true(self):
        sys.modules[ "__main__" ].settings.getSetting.side_effect = [ "3", "true", "proxy/?browse=", "proxy/?browse=", "proxy/?browse=" ]
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
        print repr(ret)
        assert(ret['status'] == 200 and ret['content'] == "Nothing here\n")
        sys.modules[ "__main__" ].common.log.assert_any_call("got proxy: proxy/?browse=http%3A//tobiasussing.dk")
        
    def test_findErrors_should_use_parseDOM_to_look_for_errormsg_tag(self):
        input = { "content": "some_content"}
        parsedom = [ ["Mock error [" ] ] # This should probably be updated to something real.
        sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
        core = YouTubeCore()
        
        result = core._findErrors( input )
        
        sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "class": "errormsg" })
        assert(result == "Mock error")

    def test_findErrors_should_use_parseDOM_to_look_for_error_smaller(self):
        input = { "content": "some_content"}
        parsedom = [ ["Mock error ["],[] ] # This should probably be updated to something real.
        sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
        core = YouTubeCore()
        
        result = core._findErrors({"content":"some_content"})
        
        sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "class": "error smaller" })
        assert(result == "Mock error")
        
    def test_findErrors_should_use_parseDOM_to_look_for_unavailable_message(self):
        input = { "content": "some_content"}
        parsedom = [ ["Mock error ["],[],[] ] # This should probably be updated to something real.
        sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
        core = YouTubeCore()
        
        result = core._findErrors({"content":"some_content"})
        
        sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "id": "unavailable-message" })
        assert(result == "Mock error")
        
    def test_findErrors_should_use_parseDOM_to_look_for_error_if_content_contains_yt_quota(self):
        input = { "content": "some_content yt:quota"}
        parsedom = [ ["Mock error ["],[],[],[],[] ] # This should probably be updated to something real.
        sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x = "",y ="",attrs = {}: parsedom.pop()
        core = YouTubeCore()
        
        result = core._findErrors(input)
        
        assert(sys.modules[ "__main__" ].common.parseDOM.call_args_list[3][0][0] == input["content"])
        assert(sys.modules[ "__main__" ].common.parseDOM.call_args_list[3][0][1] == 'error')
        sys.modules[ "__main__" ].common.parseDOM.assert_called_with([], 'code')
        assert(result == "Mock error")

    def test_findErrors_should_return_if_error_found(self):
        input = { "content": "some_content"}
        parsedom = [ ["Mock error [" ] ] # This should probably be updated to something real.
        sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
        core = YouTubeCore()
        
        result = core._findErrors( input )
        
        assert(result == "Mock error")
	
    def test_verifyAge_should_call_fetch_page_with_correct_params(self):        
        parsedom = [ ["/verifyAgeMock"], ["http://next.com" ], ["very racy"] ] * 6
        sys.modules[ "__main__" ].common.parseDOM.side_effect = parsedom
        url_data = { "next_url": "http://next", "set_racy": "very racy", "session_token" : "MY_token"}
        sys.modules[ "__main__" ].login._httpLogin.return_value = ( { "content": "", "status": "200"} , "")
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = { "status":303,"content":'<form method="POST" action="/verify_age?action_confirm=true" id="confirm-age-form">yt.setConfig({      \'XSRF_TOKEN\': \'MY_token\',      \'XSRF_FIELD_NAME\': \'session_token\'    }); ' }
        
        result = core._verifyAge("http://mock.link","http://verify.age", { "link": "http://mock.link", "login": "true"} )
        
        core._fetchPage.assert_any_call({'login': 'true', 'link': 'http://www.youtube.com//verifyAgeMock', 'url_data': {'next_url': 'http://next.com', 'set_racy': 'very racy', 'session_token': 'MY_token'}, 'no_verify_age': 'true'})

    def test_verifyAge_should_return_if_done(self):
        settings = [ "","some_token","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        sys.modules[ "__main__" ].common.parseDOM.return_value = []
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = { "status":303,"content":'PLAYER_CONFIG' }
        
        result = core._verifyAge("http://mock.link","http://verify.age", { "link": "http://mock.link", "login": "true"} )
        
        core._fetchPage.assert_any_call({'login': 'true', 'link': 'http://verify.age', 'no_verify_age': 'true'})
        assert(result == { "status":303,"content":'PLAYER_CONFIG' })

    def test_verifyAge_should_try_assuming_it_is_logged_in(self):
        settings = [ "","some_token","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()        
        sys.modules[ "__main__" ].common.parseDOM.return_value = []
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = { "status":303,"content":'nothing here' }
        
        result = core._verifyAge("http://mock.link","http://verify.age", { "link": "http://mock.link", "login": "true"} )
        
        core._fetchPage.assert_any_call({'login': 'true', 'link': 'http://verify.age', 'no_verify_age': 'true'})
        core._fetchPage.assert_any_call({'login': 'true', 'link': 'http://mock.link', 'no_verify_age': 'true'})

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
        patcher = patch("time.time")
        patcher.start()
        import time
        time.time = Mock()
        time.time.return_value = 3600

        settings = [ "","some_token","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"status":200,"content":'{"access_token":"", "expires_in": "3600"}'}
        
        result = core._oRefreshToken()
        patcher.stop()
        
        sys.modules[ "__main__" ].settings.setSetting.assert_any_call("oauth2_access_token", "")
        sys.modules[ "__main__" ].settings.setSetting.assert_any_call("oauth2_expires_at", "7200")
        
    def test_oRefreshToken_should_log_error_if_invalid_json_structure_is_returned(self):
        settings = [ "","some_token","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        core = YouTubeCore()
        core._fetchPage = Mock()
        output = {"status":200,"content":'{"access_token"][sdlkfjfksldf"super_secrect_token"[}]'}
        core._fetchPage.return_value = output
        
        result = core._oRefreshToken()
        
        sys.modules[ "__main__" ].common.log.assert_called_with("Except: " + repr(output))

    def test_oRefreshToken_should_set_access_token_if_found(self):
        patcher = patch("time.time")
        patcher.start()
        import time
        time.time = Mock()
        time.time.return_value = 3600

        settings = [ "","some_token","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        core = YouTubeCore()
        core._fetchPage = Mock()
        core._fetchPage.return_value = {"status":200,"content":'{"access_token":"super_secrect_token", "expires_in": "3600"}'}
        
        result = core._oRefreshToken()
        patcher.stop()        
        
        sys.modules[ "__main__" ].settings.setSetting.assert_any_call("oauth2_access_token", "")
        sys.modules[ "__main__" ].settings.setSetting.assert_any_call("oauth2_access_token", "super_secrect_token")
        sys.modules[ "__main__" ].settings.setSetting.assert_any_call("oauth2_expires_at", "7200")

    def test_getAuth_should_check_token_expiration_before_calling_refresh_token(self):
        settings = [ "","some_token","3249320480292","3249320480292","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        core = YouTubeCore()
        core._oRefreshToken = Mock()
        
        result = core._getAuth()
        
        sys.modules[ "__main__" ].settings.getSetting.assert_any_call("oauth2_expires_at")
	
    def test_getAuth_should_call_oRefreshToken_to_refresh_token(self):
        settings = [ "","some_token","2", "2","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        core = YouTubeCore()
        core._oRefreshToken = Mock()
        
        result = core._getAuth()
        
        core._oRefreshToken.assert_called_with()
	
    def test_getAuth_should_fetch_token_from_settings(self):
        settings = [ "", "","32342498270492","32342498270492","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        core = YouTubeCore()
        core._oRefreshToken = Mock()
        sys.modules[ "__main__" ].login.login.return_value = ("",200)
        
        result = core._getAuth()
        
        sys.modules["__main__" ].settings.getSetting.assert_called_with("oauth2_access_token")
	
    def test_getAuth_should_call_login_if_token_isnt_found(self):
        settings = [ "","","","3"]
        sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
        sys.modules[ "__main__" ].login.login.return_value = ("",200)
        core = YouTubeCore()
        core._oRefreshToken = Mock()
        
        result = core._getAuth()
        
        sys.modules[ "__main__" ].login.login.assert_called_with()
        sys.modules[ "__main__" ].settings.getSetting.assert_called_with("oauth2_access_token")

    def test_getVideoInfo_should_call_getVideoEntries_to_get_video_items(self):
        core = YouTubeCore()
        core.getVideoEntries = Mock(return_value=[])
        core.updateVideoIDCache = Mock()
        core.addNextPageLinkIfNecessary = Mock()

        core.getVideoInfo("xml",{})

        core.getVideoEntries.assert_any_call("xml")

    def test_getVideoInfo_should_call_updateVideoIDCache_to_save_video_info_to_cache(self): # missing tests
        core = YouTubeCore()
        core.getVideoEntries = Mock(return_value=[])
        core.updateVideoIDCache = Mock()
        core.addNextPageLinkIfNecessary = Mock()

        core.getVideoInfo("xml",{})

        core.updateVideoIDCache.assert_any_call([])

    def test_getVideoInfo_should_call_addNextPageLinkIfNecessary_to_set_next_page_indicator(self):
        core = YouTubeCore()
        core.getVideoEntries = Mock(return_value=[])
        core.updateVideoIDCache = Mock()
        core.addNextPageLinkIfNecessary = Mock()

        core.getVideoInfo("xml",{})

        core.addNextPageLinkIfNecessary.assert_any_call({},"xml",[])

    def setUp_getVideoInfo_full_run(self):
        self.core.getVideoEntries = Mock(return_value=["entry"])
        self.core.updateVideoIDCache = Mock()
        self.core.addNextPageLinkIfNecessary = Mock()
        self.core.getVideoId = Mock(return_value="123")
        self.core.getVideoTitle = Mock(return_value="Title")
        self.core.getVideoDescription = Mock(return_value="Description")
        self.core.getViewCount = Mock(return_value=0)
        self.core.getVideoUploadDate = Mock(return_value=datetime.datetime.now().date())
        self.core.getVideoCreator = Mock(return_value="VideoCreator")
        self.core.getVideoRating = Mock(return_value="1")
        self.core.getVideoGenre = Mock(return_value="VideoGenre")
        self.core.getVideoDuration = Mock(return_value="2")
        self.core.getVideoEditId = Mock(return_value="editId")
        sys.modules["__main__"].storage.retrieveValue.return_value = "0"

    def test_getVideoInfo_should_call_getVideoId_to_get_video_id(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoId.assert_any_call("entry")

    def test_getVideoInfo_should_call_getNodeValue_to_get_Title(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoTitle.assert_any_call("entry")

    def test_getVideoInfo_should_call_getVideoDescription_to_get_video_Plot(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoDescription.assert_any_call("entry", datetime.datetime.now().date(), 0)

    def test_getVideoInfo_should_call_getVideoUploadDate_to_get_Date(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoUploadDate.assert_any_call("entry")

    def test_getVideoInfo_should_call_getVideoCreator_to_get_Studio(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoCreator.assert_any_call("entry")

    def test_getVideoInfo_should_call_getVideoDuration_to_get_Duration(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoDuration.assert_any_call("entry")

    def test_getVideoInfo_should_call_getVideoRating_to_get_Rating(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoRating.assert_any_call("entry")

    def test_getVideoInfo_should_call_getViewCount_to_get_view_Count(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getViewCount.assert_any_call("entry")

    def test_getVideoInfo_should_call_getVideoGenre_to_get_Genre(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoGenre.assert_any_call("entry")

    def test_getVideoDescription_should_add_date_to_plot(self):
        assert(False)

    def test_getVideoDescription_should_add_view_count_to_plot(self):
        assert(False)

    def test_getVideoInfo_should_call_getVideoEditId_to_search_for_edit_id(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        self.core.getVideoEditId.assert_any_call("entry")

    def test_getVideoInfo_should_call_storage_retrieveValue_to_get_watch_status(self):
        self.core = YouTubeCore()
        self.setUp_getVideoInfo_full_run()

        self.core.getVideoInfo("xml",{})

        sys.modules[ "__main__" ].storage.retrieveValue.assert_any_call("vidstatus-123")

    def test_getVideoInfo_should_parse_youtube_xml(self):
        sys.modules[ "__main__" ].storage.retrieveValue.return_value = "7"
        import CommonFunctions
        sys.modules["__main__"].common = CommonFunctions
        core = YouTubeCore()

        result = core.getVideoInfo(self.readTestInput("youtubeFavoritesFeed.xml", False))

        print repr(result)
        assert(result[0]["Overlay"] == 7)
        assert(result[0]["editid"] == 'some_edit_id')
        assert(result[0]["Title"] == "Aurora seen from the ISS in Orbit")
        assert(result[0]["playlist_entry_id"] == 'some_edit_id')
        assert(result[0]["Rating"] > 4.9)
        assert(result[0]["videoid"] == 'ogtKe7N05F0')
        assert(result[0]["Duration"] == "00:35")
        assert(result[0]["Genre"] == "Science & Technology")
        assert(result[0]["Studio"] == "isoeph")
        assert(result[0]["Date"] == "29-09-2011")
        assert(result[0]["thumbnail"] == "http://i.ytimg.com/vi/ogtKe7N05F0/0.jpg")

    def test_addNextPageLinkIfNecessary_should_call_parseDOM_to_find_links(self):
        core = YouTubeCore()

        core.addNextPageLinkIfNecessary({}, "xml", [])

        sys.modules["__main__"].common.parseDOM.assert_any_call("xml", "link", ret="rel")

    def test_addNextPageLinkIfNecessary_should_call_addNextFolder_if_next_link_is_found(self):
        sys.modules["__main__"].common.parseDOM.return_value = ["next"]
        core = YouTubeCore()

        core.addNextPageLinkIfNecessary({}, "xml", [])

        sys.modules["__main__"].utils.addNextFolder([],{})

    def test_addNextPageLinkIfNecessary_should_not_call_addNextFolder_if_next_link_is_not_found(self):
        sys.modules["__main__"].common.parseDOM.return_value = ["notnext"]
        core = YouTubeCore()

        result = core.addNextPageLinkIfNecessary({}, "xml", [])

        sys.modules["__main__"].utils.addNextFolder([],{})

    def test_getVideoEntries_should_call_parseDOM_to_find_video_entries(self):
        sys.modules["__main__"].common.parseDOM.return_value = ["some_entry"]
        core = YouTubeCore()

        core.getVideoEntries("xml")

        sys.modules["__main__"].common.parseDOM.assert_any_call("xml", "entry")

    def test_getVideoEntries_should_make_2nd_attempt_call_to_parseDOM_to_find_video_entries(self):
        sys.modules["__main__"].common.parseDOM.side_effect = ["","some_entry"]
        core = YouTubeCore()

        core.getVideoEntries("xml")

        sys.modules["__main__"].common.parseDOM.assert_any_call("xml", "atom:entry")

if __name__ == "__main__":
	nose.runmodule()
