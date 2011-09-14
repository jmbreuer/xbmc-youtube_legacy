import nose
import BaseTestCase
from mock import Mock, patch
import sys, io
import MockYouTubeDepends
from CommonFunctions import CommonFunctions

class TestCommonFunctions(BaseTestCase.BaseTestCase):
	link_html = "<a href='bla.html'>Link Test</a>"
	img_html = "<img src='bla.png' alt='Thumbnail' />"
	sys.modules["xbmc"].log = Mock()
	sys.modules["xbmc"].LOGNOTICE = 0
	sys.modules["inspect"].stack = Mock()
	sys.modules["inspect"].stack.return_value = [0, 1, [0, 1, 2, "Mock"]]
		
	def test_log_(self):
		description = "Logging"
		common  = CommonFunctions()
		common.log(description)

		sys.modules["xbmc"].log.assert_called_with("[%s] %s : '%s'" % ( sys.modules[ "__main__" ].plugin, 
										"Mock", 
										description), 
							   sys.modules["xbmc"].LOGNOTICE)

	def test_fetchPage_link(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common._fetchPage({ "link": "http://tobiasussing.dk"})
		assert(ret['status'] == 200 and ret['content'] == "Nothing here\n")

	def test_fetchPage_broken_link(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common._fetchPage({ "link": "http://tobiasussing.dk/DoesNotExist.html"})
		print repr(ret)
		assert(ret['status'] == 500 and ret['content'] == "")
		
	def test_stripTags_link(self):
		common = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = self.link_html
		ret = common.stripTags(inp)
		print repr(ret)
		assert(ret == "Link Test")

	def test_parseDOM_link_href(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.link_html, "a", ret = "href")
		print repr(ret)
		assert(ret[0] == "bla.html")

	def test_parseDOM_link_content(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.link_html, "a", attrs = { "href": "bla.html" })
		print repr(ret)
		assert(ret[0] == "Link Test")

	def test_parseDOM_img_src(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.img_html, "img", attrs = { "alt": "Thumbnail" }, ret = "src" )
		print repr(ret)
		assert(ret[0] == "bla.png")

	def test_parseDOM_img_alt(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.img_html, "img", ret = "alt")
		print repr(ret)
		assert(ret[0] == "Thumbnail")

	def test_parseDOM_flashvars(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.readTestInput("watch-gyzlwNvf8ss-standard.html", False), "embed", attrs = {"id": "movie_player" }, ret = "flashvars")
		print repr(ret)
		assert(ret[0].strip() == self.readTestInput("watch-gyzlwNvf8ss-flashvars.txt", False).strip())

	def test_parseDOM_flashvars_src(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.readTestInput("watch-gyzlwNvf8ss-standard.html", False), "embed", attrs = {"id": "movie_player"}, ret = "src")
		print repr(ret)
		assert(ret[0] == "http://s.ytimg.com/yt/swfbin/watch_as3-vflCwc_mi.swf")

	def test_getDOMContent_link(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = self.link_html
		ret = common.getDOMContent(inp, "a", "<a href='bla.html'>")
		print repr(ret)
		assert(ret == "Link Test")

	def test_getDOMContent_link_fail(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = "<a href='bla2.html'>Link Test</a>"
		ret = common.getDOMContent(inp, "a", "<a href='bla.html'>")
		print repr(ret)
		assert(ret == "")

if __name__ == "__main__":
	nose.run()
