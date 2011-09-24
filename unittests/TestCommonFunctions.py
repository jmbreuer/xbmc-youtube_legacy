import nose
import BaseTestCase
from mock import Mock, patch
import sys
from CommonFunctions import CommonFunctions

class TestCommonFunctions(BaseTestCase.BaseTestCase):
	link_html = "<a href='bla.html'>Link Test</a>"
	img_html = "<img src='bla.png' alt='Thumbnail' />"
		
	def test_log_should_call_xbmc_with_properly_formated_message(self):
		description = "Logging"
		sys.modules["__main__"].xbmc.LOGNOTICE = 0
		common  = CommonFunctions()
		common.log(description)
		sys.modules["__main__"].xbmc.log.assert_called_with("[%s] %s : '%s'" % ( sys.modules[ "__main__" ].plugin, 
										"run", 
										description), 
							   sys.modules["__main__"].xbmc.LOGNOTICE)

	def test_fetchPage_should_return_content_and_success_return_code_on_valid_link(self):
		patcher = patch("urllib2.urlopen")
		patcher.start()
		import urllib2
		dummy_connection = Mock()
		dummy_connection.read.return_value = "Nothing here\n"
		patcher(urllib2.urlopen).return_value = dummy_connection
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common._fetchPage({ "link": "http://tobiasussing.dk"})
		patcher.stop()
		
		assert(ret['status'] == 200 and ret['content'] == "Nothing here\n")

	def test_fetchPage__should_return_failing_error_code_on_broken_link(self):
		patcher = patch("urllib2.urlopen")
		patcher.start()
		import urllib2
		fp = Mock()
		fp.read.return_value = ""
		patcher(urllib2.urlopen).side_effect = urllib2.HTTPError("http://tobiasussing.dk/DoesNotExist.html",500,"","",fp)
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common._fetchPage({ "link": "http://tobiasussing.dk/DoesNotExist.html"})
		patcher.stop()
		
		print repr(ret)
		assert(ret['status'] == 500 and ret['content'] == "")
	
	def test_stripTags_should_correctly_extract_the_text_content_of_a_link_tag(self):
		common = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = self.link_html
		
		ret = common.stripTags(inp)
		
		print repr(ret)
		assert(ret == "Link Test")

	def test_parseDOM_should_correctly_extract_the_href_attribute_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", ret = "href")
		
		print repr(ret)
		assert(ret[0] == "bla.html")
	
	def test_parseDOM_should_call_getDOMContent_when_extracting_content_of_a_link_tag(self):
		common  = CommonFunctions()
		common.getDOMContent = Mock()
		common.getDOMContent.return_value = "Link Test"
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", attrs = { "href": "bla.html" })
		
		print repr(ret)
		common.getDOMContent.assert_called_with("<a href='bla.html'>Link Test</a>", 'a', "<a href='bla.html'>",)
	
	def test_parseDOM_should_correctly_extract_the_text_conten_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", attrs = { "href": "bla.html" })
		
		print repr(ret)
		assert(ret[0] == "Link Test")

	def test_parseDOM_should_correctly_extract_the_src_attribute_of_an_img_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.img_html, "img", attrs = { "alt": "Thumbnail" }, ret = "src" )
		
		print repr(ret)
		assert(ret[0] == "bla.png")

	def test_parseDOM_should_correctly_extract_the_alt_attribute_of_an_img_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.img_html, "img", ret = "alt")
		
		print repr(ret)
		assert(ret[0] == "Thumbnail")

	def test_parseDOM_should_be_able_to_extract_flashvars_content_from_a_youtube_video_page(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.readTestInput("watch-gyzlwNvf8ss-standard.html", False), "embed", attrs = {"id": "movie_player" }, ret = "flashvars")
		
		print repr(ret)
		assert(ret[0].strip() == self.readTestInput("watch-gyzlwNvf8ss-flashvars.txt", False).strip())

	def test_parseDOM_should_be_able_to_extract_the_src_attribute_of_a_flashvars_element_from_a_youtube_video_page(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.readTestInput("watch-gyzlwNvf8ss-standard.html", False), "embed", attrs = {"id": "movie_player"}, ret = "src")
		
		print repr(ret)
		assert(ret[0] == "http://s.ytimg.com/yt/swfbin/watch_as3-vflCwc_mi.swf")

	def test_getDOMContent_should_correctly_extract_the_text_content_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = self.link_html
		
		ret = common.getDOMContent(inp, "a", "<a href='bla.html'>")
		
		print repr(ret)
		assert(ret == "Link Test")

	def test_getDOMContent_should_not_extract_the_content_of_a_link_tag_that_doesnt_match_the_search_string(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = "<a href='bla2.html'>Link Test</a>"
		
		ret = common.getDOMContent(inp, "a", "<a href='bla.html'>")
		
		print repr(ret)
		assert(ret == "")

if __name__ == "__main__":
	nose.run()
