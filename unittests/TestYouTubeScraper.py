# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  YouTubeScraper import YouTubeScraper 

class TestYouTubeScraper(BaseTestCase.BaseTestCase):
	
	def test_scrapeTrailersListFormat_should_call_create_url_to_get_page_url(self):
		sys.modules[ "__main__" ].common.parseDOM.return_value = []
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content"}
		scraper = YouTubeScraper()
		scraper.createUrl = Mock()
		scraper.createUrl.return_value = "some_url"
		
		scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		scraper.createUrl.assert_called_with({"scraper":"trailers"})
		
	def test_scrapeTrailersListFormat_should_call_fetchPage_to_fetch_html_contents(self):
		sys.modules[ "__main__" ].common.parseDOM.return_value = []
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content"}
		scraper = YouTubeScraper()
		scraper.createUrl = Mock()
		scraper.createUrl.return_value = "some_url"
		
		scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].core._fetchPage.assert_called_with({"link":"some_url"})
		
	def test_scrapeTrailersListFormat_should_call_parseDOM_to_find_trailers(self):
		sys.modules[ "__main__" ].common.parseDOM.return_value = []
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content"}
		scraper = YouTubeScraper()
		scraper.createUrl = Mock()
		scraper.createUrl.return_value = "some_url"
		
		scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].common.parseDOM.assert_called_with("some_content", "div", attrs={"id":"recent-trailers-container"})
	
	def test_scrapeTrailersListFormat_should_call_getBatchDetailsThumbnails_with_videoid_list(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content"}
		sys.modules["__main__"].core.getBatchDetailsThumbnails.return_value = ([{"videoid":"video_id1"},{"videoid":"video_id2"}],  200)
		container = ["some_trailers_container"]
		thumbs = ["thumb_1","thumb_2"]
		videoids = ["some_thing=video_id1","some_thing=video_id2"]
		dom = [thumbs, videoids, container]
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x = "", y = "", attrs = "", ret ="": dom.pop()
		scraper = YouTubeScraper()
		scraper.createUrl = Mock()
		scraper.createUrl.return_value = "some_url"
		
		scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].core.getBatchDetailsThumbnails.assert_called_with([("video_id1","thumb_1"),("video_id2","thumb_2")])
		
	def test_getBatchDetailsThumbnails_return_error_status_if_no_videos_are_found(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content"}
		sys.modules["__main__"].core.getBatchDetailsThumbnails.return_value = ([], 500)
		container = ["some_trailers_container"]
		thumbs = ["thumb_1","thumb_2"]
		videoids = ["some_thing=video_id1","some_thing=video_id2"]
		dom = [thumbs, videoids, container]
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x = "", y = "", attrs = "", ret ="": dom.pop()
		scraper = YouTubeScraper()
		scraper.createUrl = Mock()
		scraper.createUrl.return_value = "some_url"
		
		result, status = scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].core.getBatchDetailsThumbnails.assert_called_with([("video_id1","thumb_1"),("video_id2","thumb_2")])
		
		assert(result == [])
		assert(status == 500)
		
	
	
if __name__ == '__main__':
	nose.runmodule()
