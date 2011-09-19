import nose
import BaseTestCase
from mock import Mock, patch
import sys, io
import MockYouTubeDepends
from YouTubeCore import YouTubeCore
import inspect
class TestYouTubeCore(BaseTestCase.BaseTestCase):
	def popSetting(self, *args, **kwargs):
		#print repr(self) + " - " + repr(args) + " - " + repr(kwargs)
		#print repr(inspect.stack()) 

		val = self.settings.pop()
		return val

	def test_delete_favorite_should_call_fetchPage_with_correct_fetch_options(self):
		settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = lambda x: settings.pop()
		core = YouTubeCore()
		core._fetchPage = Mock()
		core._fetchPage.return_value = {"content":"success", "status":200}

		core.delete_favorite({ "editid": "test" })
		
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/favorites/test" 
		core._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})

	def remove_contact(self):
		core = YouTubeCore()
		result = core.remove_contact({})
		assert(result == [])

	def remove_subscription(self):
		core = YouTubeCore()
		result = core.remove_subscription({})
		assert(result == [])

	def add_contact(self):
		core = YouTubeCore()
		result = core.add_contact({})
		assert(result == [])

	def add_favorite(self):
		core = YouTubeCore()
		result = core.add_favorite({})
		assert(result == [])

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
		self.settings = ["4","3" ]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = self.popSetting
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
		self.settings = [ "3"]
		input = { "content": "<div class='errormsg'>Mock Error</div>"}
		sys.modules[ "__main__" ].settings.getSetting.side_effect = self.popSetting
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
