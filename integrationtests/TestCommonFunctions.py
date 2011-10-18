import BaseTestCase
import unittest2
import nose, sys, os
from mock import Mock, patch


class TestYouTubePlayer(BaseTestCase.BaseTestCase):
	def test_parseDOM_thingy(self):
		common = sys.modules[ "__main__" ].common
		player = sys.modules[ "__main__" ].player
		page = common._fetchPage({ "link": "http://www.youtube.com/show/roosterteethshorts?feature=sh_co_show_1_17?hl=en"})
		print "Page : " + repr(page)
		seasons = common.parseDOM(page["content"], "div", attrs = {"class": "seasons-list"})
		print "Seasons: " + repr(seasons)
		season_list = common.parseDOM(seasons, "span", attrs = {"class": "yt-uix-button-content"})
		print "Season List: " + repr(season_list)

		assert(season_list == ['3', '2', '1'])

if __name__ == "__main__":
	nose.runmodule()
