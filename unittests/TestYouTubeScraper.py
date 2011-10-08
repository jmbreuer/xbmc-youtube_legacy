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
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
	
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
		
	def ttest_scrapeCategoriesGrid_should_call_parseDOM_to_find_paginator(self):
		assert(False)
	
	def ttest_scrapeCategoriesGrid_should_call_createUrl_to_get_correct_url(self):
		assert(False)
		
	def ttest_scrapeCategoriesGrid_should_call_core_fetchPage_to_get_html_content(self):
		assert(False)
		
	def ttest_scrapeCategoriesGrid_should_call_parseDOM_to_get_videos_container(self):
		assert(False)
		
	def ttest_scrapeCategoriesGrid_should_call_parseDOM_on_videos_to_find_links(self):
		assert(False)
		
	def ttest_scrapeMusicCategories_should_call_createUrl_to_get_proper_url(self):
		assert(False)
	
	def ttest_scrapeMusicCategories_should_call_core_fetchPage_to_get_html_conten(self):
		assert(False)
		
	def ttest_scrapeMusicCategories_should_call_utils_makeAscii_to_encode_title(self):
		assert(False)
		
	def ttest_scrapeMusicCategories_should_call_replaceHtmlCodes_to_remove_html_formating(self):
		assert(False)
		
	def ttest_scrapeMusicCategories_should_retur_properly_formated_structure(self):
		assert(False)
		
	def ttest_scrapeArtist_should_call_saveStoredArtist_if_artist_name_is_present(self):
		assert(False)
	
	def ttest_scrapeArtist_should_call_createUrl_to_get_correct_url(self):
		assert(False)
		
	def ttest_scrapeArtist_should_call_fetchPage_to_get_html_contents(self):
		assert(False)
		
	def ttest_scrapeArtist_should_call_parseDOM_to_get_vidoes(self):
		assert(False)
		
	def ttest_scrapeArtist_should_return_list_of_video_ids(self):
		assert(False)
	
	def ttest_scrapeSimilarArtists_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeSimilarArtists_should_call_core_fetchPage_to_get_html_content(self):
		assert(False)
		
	def ttest_scrapeSimilarArtists_should_call_parseDOM_to_get_artists(self):
		assert(False)
		
	def ttest_scrapeSimilarArtists_should_call_utils_makeAscii_to_encode_title(self):
		assert(False)
		
	def ttest_scrapeSimilarArtists_should_call_replaceHtmlCodes_to_remove_html_formating(self):
		assert(False)

	def ttest_scrapeMusicCategoryArtists_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryArtists_should_call_core_fetchPage_to_get_html_content(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryArtists_should_call_parseDOM_to_get_categories(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryArtists_should_call_utils_makeAscii_to_encode_title(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryArtists_should_call_replaceHtmlCodes_to_remove_html_formating(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryArtists_should_return_proper_structure(self):
		assert(False)

	def ttest_scrapeMusicCategoryHits_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryHits_should_call_core_fetchPage_to_get_html_content(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryHits_should_call_parseDOM_to_get_videos(self):
		assert(False)
		
	def ttest_scrapeMusicCategoryHits_should_return_list_of_video_ids(self):
		assert(False)
		
	def ttest_searchDisco_should_call_createUrl_to_get_seach_url(self):
		assert(False)
		
	def ttest_searchDisco_should_call_createUrl_to_get_mixlist_url(self):
		assert(False)
		
	def ttest_searchDisco_should_call_fetchPage_to_get_search_result(self):
		assert(False)
		
	def ttest_searchDisco_should_call_fetchPage_to_get_mix_list_content(self):
		assert(False)
		
	def ttest_searchDisco_should_call_parseDOM_to_get_video_list(self):
		assert(False)
		
	def ttest_searchDisco_should_return_list_of_videoids(self):
		assert(False)
		
	def ttest_scrapeDiscoTopArtist_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeDiscoTopArtist_should_call_fetchPage_to_get_page_content(self):
		assert(False)

	def ttest_scrapeDiscoTopArtist_should_call_parseDOM_to_find_artist_list(self):
		assert(False)
		
	def ttest_scrapeDiscoTopArtist_should_call_utils_makeAscii_to_encode_title(self):
		assert(False)
		
	def ttest_scrapeDiscoTopArtist_should_call_storage_retrieve_to_get_thumbnail(self):
		assert(False)
		
	def ttest_scrapeDiscoTopArtist_should_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationCategories_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeEducationCategories_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeEducationCategories_should_call_parseDOM_to_find_categories(self):
		assert(False)
		
	def ttest_scrapeEducationCategories_should_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_parseDOM_to_find_categories(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_call_replaceHtmlCodes_to_remove_html_chars_from_title(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_parseDOM_to_find_categories(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_replaceHtmlCodes_to_remove_html_chars_from_title(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_prepend_a_a_courses_link(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_call_parseDOM_to_find_pagination(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_call_parseDOM_to_find_videos(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_call_utils_replaceHtmlCodes_to_remove_html_chars_from_title(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_return_list_of_videos(self):
		assert(False)

	def ttest_scrapeEducationVideos_should_return_proper_structure(self):
		assert(False)
	
	def ttest_scrapeRecommended_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeRecommended_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeRecommended_should_parseDOM_to_get_video_ids(self):
		assert(False)
		
	def ttest_scrapeRecommended_should_return_list_of_video_ids(self):
		assert(False)
		
	def ttest_scrapeWatchLater_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeWatchLater_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeWatchLater_should_call_parseDOM_to_find_redirect_to_playlist(self):
		assert(False)
		
	def ttest_scrapeWatchLater_should_call_feeds_list_if_playlist_is_found(self):
		assert(False)
		
	def ttest_scrapeShowEpisodes_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def ttest_scrapeShowEpisodes_should_call_fetchPage_to_get_page_content(self):
		assert(False)
		
	def ttest_scrapeShowEpisodes_should_call_parseDOM_to_find_videoids(self):
		assert(False)
		
	def ttest_scrapeShowEpisodes_should_call_parseDOM_to_find_next_url(self):
		assert(False)
		
	def ttest_scrapeShowEpisodes_should_fetch_entire_list(self):
		assert(False)
		
	def ttest_scrapeShow_should_call_createUrl_to_get_proper_url(self):
	def ttest_scrapeShow_should_call_fetchPage_to_get_page_content(self):
	def ttest_scrapeShow_should_parseDOM_to_find_videoids(self):
	def ttest_scrapeShow_should_
	def ttest_scrapeShow_should_
	def ttest_scrapeShow_should_
	
		
if __name__ == '__main__':
	nose.runmodule()
