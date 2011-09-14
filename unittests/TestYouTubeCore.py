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

        def delete_favorite(self):
		# length = 9
                self.settings = ["4","3" ] #, "user", "pass", "true", "true", "true", "true", "true", "true", "true", "true", "true", "true" "true", "true", "true", "true", "true", "true", "true", "true", "true", "true"]
		self.settings = []

		sys.modules[ "__main__" ].settings.getSetting.side_effect = self.popSetting

		core = YouTubeCore()
		core.delete_favorite({ "editid": "test" })
		delete_url = "http://gdata.youtube.com/feeds/api/users/default/favorites/%s/asdfsdfsdf" % "EDIT_ID"
		sys.modules["xbmc"]._fetchPage.assert_called_with({"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"})


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


        def test_fetchPage(self):
                self.settings = ["4","3" ]

		sys.modules[ "__main__" ].settings.getSetting.side_effect = self.popSetting
		sys.modules[ "urllib2" ].urlopen.return_value = { "content": "Nothing here", "new_url": "", "header": "Mock header"}

		core = YouTubeCore()
		#params = {"link": delete_url, "api": "true", "login": "true", "auth": "true", "method": "DELETE"}
		params = {"link": "http://tobiasussing.dk" }
		result = core._fetchPage(params)
		assert(result['content'] == "Nothing here\n")

        def test_findErrors(self):
		self.settings = [ "3"]
		sys.modules[ "__main__" ].settings.getSetting.side_effect = self.popSetting
		parsedom = [ ["Mock error [" ] ] # This should probably be updated to something real.
		def popParseDOM(self, *args, **kwargs):
			#print repr(self) + " - " + repr(args) + " - " + repr(kwargs)
			val = parsedom.pop()
			return val
		sys.modules[ "__main__" ].common.parseDOM.side_effect = popParseDOM

		core = YouTubeCore()
		result = core._findErrors( { "content": "<div class='errormsg'>Mock Error</div>"} )
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
