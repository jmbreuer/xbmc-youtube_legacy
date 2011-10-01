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
'''
	def ttest_createUrl_should_2
		assert(False)

	def ttest_createUrl_should_3
		assert(False)

	def ttest_createUrl_should_4
		assert(False)

	def ttest_createUrl_should_5
		assert(False)

	def ttest_createUrl_should_6
		assert(False)

	def ttest_createUrl_should_7
		assert(False)

	def ttest_createUrl_should_8
		assert(False)
'''
if __name__ == "__main__":
	nose.runmodule()
