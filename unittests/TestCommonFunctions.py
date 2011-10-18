import nose
import BaseTestCase
from mock import Mock, patch
import sys
from CommonFunctions import CommonFunctions

class TestCommonFunctions(BaseTestCase.BaseTestCase):
	link_html = "<a href='bla.html'>Link Test</a>"
	false_positive_link_html = "<a href='fake.html' id='link'>Link Test fake</a><a href='real.html' id='link' class='real'>Link Test real</a><a href='reallyfake.html' id='link' class='really fake'>Link Test really fake</a>"
	link_artist_html = '<a href="/watch?v=bla-id&amp;feature=artist">Link Test</a>'
	img_html = "<img src='bla.png' alt='Thumbnail' />"
		
	def test_log_should_call_xbmc_with_properly_formated_message(self):
		description = "Logging"
		sys.modules["__main__"].xbmc.LOGNOTICE = 0
		common  = CommonFunctions()
		common.log(description)
		sys.modules["__main__"].xbmc.log.assert_called_with("[%s] %s : '%s'" % ( sys.modules[ "__main__" ].plugin, "test_log_should_call_xbmc_with_properly_formated_message", description), sys.modules["__main__"].xbmc.LOGNOTICE)

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
		
		assert(ret['status'] == 200)
		assert(ret['content'] == "Nothing here\n")

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
		
		assert(ret['status'] == 500)
		assert(ret['content'] == "")
	
	def test_stripTags_should_correctly_extract_the_text_content_of_a_link_tag(self):
		common = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = self.link_html
		
		ret = common.stripTags(inp)
		
		assert(ret == "Link Test")

	def test_parseDOM_should_correctly_extract_the_href_attribute_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", ret = "href")
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "bla.html")

	def test_parseDOM_should_correctly_extract_the_href_attribute_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.false_positive_link_html, "a", attrs = { "id": "link", "class": "real" }, ret = "href")
		assert(len(ret) == 1 )	
		assert(ret[0] == "real.html")

	def test_parseDOM_should_correctly_extract_the_href_attribute_of_a_link_tag_with_wildcard_search(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_artist_html, "a", attrs = { "href": ".*feature=artist" }, ret = "href")
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "/watch?v=bla-id&amp;feature=artist")
	
	def test_parseDOM_should_call_getDOMContent_when_extracting_content_of_a_link_tag(self):
		common  = CommonFunctions()
		common.getDOMContent = Mock()
		common.getDOMContent.return_value = "Link Test"
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", attrs = { "href": "bla.html" })
		
		common.getDOMContent.assert_called_with("<a href='bla.html'>Link Test</a>", 'a', "<a href='bla.html'>",)

	def test_parseDOM_should_call_getDOMAttribute_when_extracting_attributes(self):
		common  = CommonFunctions()
		common.getDOMAttributes = Mock()
		common.getDOMAttributes.return_value = "bla.html"
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", attrs = { "href": "bla.html" }, ret = "href")
		
		common.getDOMAttributes.assert_called_with(["'bla.html'"])
	
	def test_getDOMAttributes_should_handle_double_quotation_marks(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.getDOMAttributes(['"                                 "3 Minutes In Hell" - Gary Anthony Williams                     "'])
		print repr(ret)
		assert(len(ret) == 1 )	
		assert(ret[0] == '"3 Minutes In Hell" - Gary Anthony Williams')

	def test_parseDOM_should_correctly_extract_the_text_conten_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.link_html, "a", attrs = { "href": "bla.html" })
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "Link Test")

	def test_parseDOM_should_correctly_extract_the_src_attribute_of_an_img_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.img_html, "img", attrs = { "alt": "Thumbnail" }, ret = "src" )
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "bla.png")

	def test_parseDOM_should_not_extract_the_src_attribute_of_an_img_tag_with_wrong_alt(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.img_html, "img", attrs = { "alt": "Thumb broken" }, ret = "src" )
		
		assert(len(ret) == 0 )	
		assert(ret == [])

	def test_parseDOM_should_correctly_extract_the_alt_attribute_of_an_img_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.img_html, "img", ret = "alt")
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "Thumbnail")

	def test_parseDOM_should_be_able_to_extract_flashvars_content_from_a_youtube_video_page(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.readTestInput("watch-gyzlwNvf8ss-standard.html", False), "embed", attrs = {"id": "movie_player" }, ret = "flashvars")
		
		assert(len(ret) == 1 )	
		assert(ret[0].strip() == self.readTestInput("watch-gyzlwNvf8ss-flashvars.txt", False).strip())

	def test_parseDOM_should_be_able_to_extract_the_src_attribute_of_a_flashvars_element_from_a_youtube_video_page(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.readTestInput("watch-gyzlwNvf8ss-standard.html", False), "embed", attrs = {"id": "movie_player"}, ret = "src")
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "http://s.ytimg.com/yt/swfbin/watch_as3-vflCwc_mi.swf")


	def test_parseDOM_should_correctly_extract_double_quotation_marks(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		
		ret = common.parseDOM(self.readTestInput("parse-title-with-quotation-marks.html", False), "span", attrs = { "class":"Title"}, ret = "title")
		print repr(ret)
		assert(len(ret) == 1 )	
		assert(ret[0] == '"3 Minutes In Hell" - Gary Anthony Williams')

	def test_parseDOM_should_be_able_to_handle_line_breaks(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		ret = common.parseDOM(self.readTestInput("2-factor.html", False), "input", attrs= { "id": "uilel" }, ret= "value")
		
		assert(len(ret) == 1 )	
		assert(ret[0] == "3")

	def test_getDOMContent_should_correctly_extract_the_text_content_of_a_link_tag(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = self.link_html
		
		ret = common.getDOMContent(inp, "a", "<a href='bla.html'>")
		
		assert(ret == "Link Test")

	def test_getDOMContent_should_properly_remove_matched_content(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		seasons = ['<div class="seasons-label">S\xc3\xa6soner</div><div class="seasons "><div class="yt-uix-slider" data-slider-slides="1" data-slider-slide-selected="0"><div class="yt-uix-slider-body "><div class="yt-uix-slider-slides yt-uix-button-group"><span class="yt-uix-slider-slide"><button type="button" class="start yt-uix-button yt-uix-button-toggled yt-uix-tooltip" onclick=";return false;" title="Afsnit: 27" data-clip-count="0" data-clips-url="/show/roosterteethshorts?s=3&amp;clips=1" data-season-number="3" data-clips-by-default="" data-episodes-ajax-url="/show?clips=0&amp;start=0&amp;action_ajax=1&amp;season_id=GL7C5ICYWXM&amp;p=0EPG3GK-VK8" data-clips-ajax-url="/show?clips=1&amp;start=0&amp;action_ajax=1&amp;season_id=GL7C5ICYWXM&amp;p=0EPG3GK-VK8" data-slide-index="0" data-episode-count="27" data-episodes-url="/show/roosterteethshorts?s=3" data-button-action="yt.www.browse.show.onShowSeasonSelect" role="button"><span class="yt-uix-button-content">3</span></button><button type="button" class=" yt-uix-button yt-uix-tooltip" onclick=";return false;" title="Afsnit: 23" data-clip-count="0" data-clips-url="/show/roosterteethshorts?s=2&amp;clips=1" data-season-number="2" data-clips-by-default="" data-episodes-ajax-url="/show?clips=0&amp;start=0&amp;action_ajax=1&amp;season_id=867QvtFJT1A&amp;p=0EPG3GK-VK8" data-clips-ajax-url="/show?clips=1&amp;start=0&amp;action_ajax=1&amp;season_id=867QvtFJT1A&amp;p=0EPG3GK-VK8" data-slide-index="0" data-episode-count="23" data-episodes-url="/show/roosterteethshorts?s=2" data-button-action="yt.www.browse.show.onShowSeasonSelect" role="button"><span class="yt-uix-button-content">2</span></button><button type="button" class=" end yt-uix-button yt-uix-tooltip" onclick=";return false;" title="Afsnit: 20" data-clip-count="0" data-clips-url="/show/roosterteethshorts?s=1&amp;clips=1" data-season-number="1" data-clips-by-default="" data-episodes-ajax-url="/show?clips=0&amp;start=0&amp;action_ajax=1&amp;season_id=zO2WBW2LQyU&amp;p=0EPG3GK-VK8" data-clips-ajax-url="/show?clips=1&amp;start=0&amp;action_ajax=1&amp;season_id=zO2WBW2LQyU&amp;p=0EPG3GK-VK8" data-slide-index="0" data-episode-count="20" data-episodes-url="/show/roosterteethshorts?s=1" data-button-action="yt.www.browse.show.onShowSeasonSelect" role="button"><span class="yt-uix-button-content">1</span></button></span></div></div></div></div>']
                season_list = common.parseDOM(seasons, "span", attrs = {"class": "yt-uix-button-content"})
                print "Season List: " + repr(season_list)

                assert(season_list == ['3', '2', '1'])

	def test_getDOMContent_should_not_extract_the_content_of_a_link_tag_that_doesnt_match_the_search_string(self):
		common  = CommonFunctions()
		common.log = sys.modules[ "__main__" ].log_override.log
		inp = "<a href='bla2.html'>Link Test</a>"
		
		ret = common.getDOMContent(inp, "a", "<a href='bla.html'>")
		
		assert(ret == "")

        def test_getDOMContent_should_extract_dom_correctly(self):
                common  = CommonFunctions()
                common.log = sys.modules[ "__main__" ].log_override.log
                inp = "<div class='match'>Here is an: <div>Inner div</div>!</div>"

                ret = common.getDOMContent(inp, "div", "<div class='match'>")
		print ret
		assert(ret == "Here is an: <div>Inner div</div>!")

if __name__ == "__main__":
	nose.runmodule()
