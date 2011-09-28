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
		
		core.getFolderInfo(xml, {})
		calls = xml.dom.minidom.parseString().getElementsByTagName.call_args_list

		patcher.stop("")
		
		print repr(calls[1][0][0])
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
		
		core.getFolderInfo(xml, {})

		patcher.stop("")
		sys.modules["__main__"].utils.addNextFolder.assert_called_with([], {})
	
	def test_getFolderInfo_should_find_edit_id_in_xml_structure_if_id_tag_is_present(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		input = self.readTestInput("getFolderInfoPlaylistTest.xml", False)
		core = YouTubeCore()
		
		result = core.getFolderInfo(input, {})

		assert(result[0]["editid"] == "some_playlist_id")


	def ttest_getFolderInfo_should_find_edit_id_in_xml_structure_if_link_tag_is_present(self):
		core = YouTubeCore()
		xml = ""
		core._getFolderInfo(xml, {})

		assert(False)

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

	def ttest_getFolderInfo_should_call_storage_retrieve_to_find_thumbnail(self):
		core = YouTubeCore()
		xml = ""
		core._getFolderInfo(xml, {})

		assert(False)
	
	def ttest_getFolderInfo_should_call_utils_addNextFolder_to_set_default_next_folder_on_feed(self):
		assert(False)
	def ttest_getBatchDetailsOverride_should_call_getBatchDetails_with_list_of_video_ids(self):
		core = YouTubeCore()
		result = core.getBatchDetailsOverride(items, params={})
		assert(result == [])

	def ttest_getBatchDetailsOverride_should_override_specified_properties_in_output_from_getBatchDetails(self):
		core = YouTubeCore()
		result = core.getBatchDetailsOverride(items, params={})
		assert(result == [])

	def ttest_getBatchDetailsThumbnails_should_call_getBatchDetails_with_list_of_video_ids(self):
		core = YouTubeCore()
		result = core.getBatchDetailsThumbnails(items, params={})
		assert(result == [])

	def ttest_getBatchDetailsThumbnails_should_override_thumbnails_in_output_from_getBatchDetails(self):
		core = YouTubeCore()
		result = core.getBatchDetailsThumbnails(items, params={})
		assert(result == [])
		
	def ttest_getBatchDetailsThumbnails_should_fill_out_missing_videos_in_collection_from_getBatchDetails_to_maintain_collection_size(self):
		core = YouTubeCore()
		result = core.getBatchDetailsThumbnails(items, params={})
		assert(result == [])

	def ttest_getBatchDetailsOverride_should_fill_out_missing_videos_in_collection_from_getBatchDetails_to_maintain_collection_size(self):
		core = YouTubeCore()
		result = core.getBatchDetailsOverride(items, params={})
		assert(result == [])
		
	def getBatchDetails(self):
		core = YouTubeCore()
		result = core._fetchPage(params={})
		assert(result == [])


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
		input = { "content": "<div class='errormsg'>Mock Error</div>"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		parsedom = [ ["Mock error [" ] ] # This should probably be updated to something real.
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x,y,attrs: parsedom.pop()
		core = YouTubeCore()
		
		result = core._findErrors( input )
		
		sys.modules[ "__main__" ].common.parseDOM.assert_called_with(input["content"], 'div', attrs={ "class": "errormsg" })
		assert(result == "Mock error")

	def _verifyAge(self):
		core = YouTubeCore()
		result = core._verifyAge(result, new_url, params={})
		assert(result == [])

	def _oRefreshToken(self):
		core = YouTubeCore()
		result = core._oRefreshToken()
		assert(result == True)

	def _getAuth(self):
		core = YouTubeCore()
		result = core.getAuth()
		assert(result != False)

	def _getNodeAttribute(self):
		core = YouTubeCore()
		result = core._getNodeAttribute(node, tag, default="")
		assert(result == [])
		print "test"

	def _getNodeValue(self):
		core = YouTubeCore()
		result = core._getNodeValue(node, tag, default="")
		assert(result == [])
		print "test"

	def _getVideoInfo(self):
		core = YouTubeCore()
		result = core.delete_favorite( xml, {})
		assert(result == [])

if __name__ == "__main__":
	nose.runmodule()