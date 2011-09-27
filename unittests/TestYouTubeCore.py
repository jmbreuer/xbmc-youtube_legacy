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

	def test_add_favorite_shouldcall_fetchPage_with_correct_fetch_options(self):
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

	def add_subscription(self):
		core = YouTubeCore()
		result = core.add_subscription({})
		assert(result == [])

	def add_playlist(self):
		core = YouTubeCore()
		result = core.add_playlist({})
		assert(result == [])

	def del_playlist(self):
		core = YouTubeCore()
		result = core.del_playlist({})
		assert(result == [])

	def add_to_playlist(self):
		core = YouTubeCore()
		result = core.add_to_playlist({})
		assert(result == [])

	def remove_from_playlist(self):
		core = YouTubeCore()
		result = core.remove_from_playlist({})
		assert(result == [])

	def getFolderInfo(self):
		core = YouTubeCore()
		result = core.getBatchDetailsOverride(items, params={})
		assert(result == [])

	def getBatchDetailsOverride(self):
		core = YouTubeCore()
		result = core.getBatchDetailsOverride(items, params={})
		assert(result == [])

	def getBatchDetailsThumbnails(self):
		core = YouTubeCore()
		result = core.getBatchDetailsThumbnails(items, params={})
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
	nose.run()
