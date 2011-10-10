# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  YouTubeScraper import YouTubeScraper 

class TestYouTubeScraper(BaseTestCase.BaseTestCase):
	scraper = ""
	
	def setUp(self):
		super(self.__class__,self).setUp()
		sys.modules["__main__"].common.parseDOM.return_value = ["some_string"]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content","status":200}
		sys.modules["__main__"].utils.makeAscii.return_value = "some_ascii_string"
		sys.modules["__main__"].utils.replaceHtmlCodes.return_value = "some_html_free_string"
		sys.modules["__main__"].utils.extractVID.return_value = ["some_video_id"]
		
		self.scraper = YouTubeScraper()
		self.scraper.createUrl = Mock()
		self.scraper.createUrl.return_value = "some_url"
		
		
	def test_scrapeTrailersListFormat_should_call_create_url_to_get_page_url(self):
		
		self.scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		self.scraper.createUrl.assert_called_with({"scraper":"trailers"})
		
	def test_scrapeTrailersListFormat_should_call_fetchPage_to_fetch_html_contents(self):
		
		self.scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].core._fetchPage.assert_called_with({"link":"some_url"})
		
	def test_scrapeTrailersListFormat_should_call_parseDOM_to_find_trailers(self):
		
		self.scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
	
	def test_scrapeTrailersListFormat_should_call_getBatchDetailsThumbnails_with_videoid_list(self):
		sys.modules["__main__"].core.getBatchDetailsThumbnails.return_value = ([{"videoid":"video_id1"},{"videoid":"video_id2"}],  200)
		container = ["some_trailers_container"]
		thumbs = ["thumb_1","thumb_2"]
		videoids = ["some_thing=video_id1","some_thing=video_id2"]
		dom = [thumbs, videoids, container]
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x = "", y = "", attrs = "", ret ="": dom.pop()
		
		self.scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].core.getBatchDetailsThumbnails.assert_called_with([("video_id1","thumb_1"),("video_id2","thumb_2")])
		
	def test_getBatchDetailsThumbnails_return_error_status_if_no_videos_are_found(self):
		sys.modules["__main__"].core.getBatchDetailsThumbnails.return_value = ([], 500)
		container = ["some_trailers_container"]
		thumbs = ["thumb_1","thumb_2"]
		videoids = ["some_thing=video_id1","some_thing=video_id2"]
		dom = [thumbs, videoids, container]
		sys.modules[ "__main__" ].common.parseDOM.side_effect = lambda x = "", y = "", attrs = "", ret ="": dom.pop()
		
		result, status = self.scraper.scrapeTrailersListFormat({"scraper":"trailers"})
		
		sys.modules["__main__"].core.getBatchDetailsThumbnails.assert_called_with([("video_id1","thumb_1"),("video_id2","thumb_2")])
		
		assert(result == [])
		assert(status == 500)
		
	def test_scrapeCategoriesGrid_should_call_parseDOM_to_find_paginator(self):
		
		result, status = self.scraper.scrapeCategoriesGrid()
		
		sys.modules["__main__"].common.parseDOM.assert_any_call('some_content', 'div', attrs={'class': 'yt-uix-pager'})
	
	def test_scrapeCategoriesGrid_should_call_createUrl_to_get_correct_url(self):
		
		result, status = self.scraper.scrapeCategoriesGrid()
		
		self.scraper.createUrl.assert_any_call({})
		
	def test_scrapeCategoriesGrid_should_call_core_fetchPage_to_get_html_content(self):
		
		result, status = self.scraper.scrapeCategoriesGrid()
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeCategoriesGrid_should_call_parseDOM_to_get_videos_container(self):
		
		result, status = self.scraper.scrapeCategoriesGrid()
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)
				
	def test_scrapeMusicCategories_should_call_createUrl_to_get_proper_url(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		self.scraper.createUrl.assert_any_call({})
			
	def test_scrapeMusicCategories_should_call_core_fetchPage_to_get_html_conten(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeMusicCategories_should_call_utils_makeAscii_to_encode_title(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		sys.modules["__main__"].utils.makeAscii.assert_any_call("some_string")
		
	def test_scrapeMusicCategories_should_call_replaceHtmlCodes_to_remove_html_formating(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		sys.modules["__main__"].utils.replaceHtmlCodes.assert_any_call("some_ascii_string")
		
	def test_scrapeMusicCategories_should_retur_properly_formated_structure(self):
		
		result, status = self.scraper.scrapeMusicCategories()		
		
		assert(result[0].has_key("category"))
		assert(result[0].has_key("icon"))
		assert(result[0].has_key("scraper"))
		assert(result[0].has_key("thumbnail"))
		assert(result[0].has_key("Title"))
		
	def test_scrapeArtist_should_call_saveStoredArtist_if_artist_name_is_present(self):
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist","artist_name":"some_artist_name"})		
		
		sys.modules["__main__"].storage.saveStoredArtist.assert_any_call({"artist":"some_artist","artist_name":"some_artist_name"})
	
	def test_scrapeArtist_should_call_createUrl_to_get_correct_url(self):
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist"})		
		
		self.scraper.createUrl.assert_any_call({"artist":"some_artist"})
		
	def test_scrapeArtist_should_call_fetchPage_to_get_html_contents(self):
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist","artist_name":"some_artist_name"})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
		
	def test_scrapeArtist_should_call_parseDOM_to_get_vidoes(self):
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist"})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeArtist_should_return_list_of_video_ids(self):
		sys.modules["__main__"].utils.extractVID.return_value = ["some_id_1","some_id_2","some_id_3"]
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist"})
		
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_2")
		assert(result[2] == "some_id_3")
		
	def test_scrapeArtist_should_remove_duplicate_video_entries(self):
		sys.modules["__main__"].utils.extractVID.return_value = ["some_id_1","some_id_3","some_id_2","some_id_3"]
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist"})
		
		assert(len(result) == 3)
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_3")
		assert(result[2] == "some_id_2")
	
	def test_scrapeSimilarArtists_should_call_createUrl_to_get_proper_url(self):
		
		result, status = self.scraper.scrapeSimilarArtists({"artist":"some_artist"})		
		
		self.scraper.createUrl.assert_any_call({"artist":"some_artist"})
		
	def test_scrapeSimilarArtists_should_call_core_fetchPage_to_get_html_content(self):
		
		result, status = self.scraper.scrapeSimilarArtists({"artist":"some_artist"})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeSimilarArtists_should_call_parseDOM_to_get_artists(self):
		
		result, status = self.scraper.scrapeSimilarArtists({"artist":"some_artist"})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeSimilarArtists_should_call_utils_makeAscii_to_encode_title(self):
		
		result, status = self.scraper.scrapeSimilarArtists({"artist":"some_artist"})		
		
		sys.modules["__main__"].utils.makeAscii.assert_any_call("some_string")
		
	def test_scrapeSimilarArtists_should_call_replaceHtmlCodes_to_remove_html_formating(self):
		
		result, status = self.scraper.scrapeSimilarArtists({"artist":"some_artist"})		
		
		sys.modules["__main__"].utils.replaceHtmlCodes.assert_any_call("some_ascii_string")

	def test_scrapeMusicCategoryArtists_should_call_createUrl_to_get_proper_url(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		self.scraper.createUrl.assert_any_call({"category":"some_category"})
		
	def test_scrapeMusicCategoryArtists_should_call_core_fetchPage_to_get_html_content(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		sys.modules["__main__"].core._fetchPage({"link":"some_url"})
		
	def test_scrapeMusicCategoryArtists_should_call_parseDOM_to_get_categories(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeMusicCategoryArtists_should_call_utils_makeAscii_to_encode_title(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		sys.modules["__main__"].utils.makeAscii.assert_any_call("some_string")
		
	def test_scrapeMusicCategoryArtists_should_call_replaceHtmlCodes_to_remove_html_formating(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		sys.modules["__main__"].utils.replaceHtmlCodes.assert_any_call("some_ascii_string")
		
	def test_scrapeMusicCategoryArtists_should_return_proper_structure(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		assert(result[0].has_key("artist"))
		assert(result[0].has_key("Title"))
		assert(result[0].has_key("scraper"))
		assert(result[0].has_key("artist_name"))
		assert(result[0].has_key("thumbnail"))
		assert(result[0].has_key("icon"))

	def test_scrapeMusicCategoryHits_should_call_createUrl_to_get_proper_url(self):
		
		result, status = self.scraper.scrapeMusicCategoryHits({"category":"some_category"})		
		
		self.scraper.createUrl.assert_any_call({"category":"some_category","batch":"true"})
		
	def test_scrapeMusicCategoryHits_should_call_core_fetchPage_to_get_html_content(self):
		
		result, status = self.scraper.scrapeMusicCategoryHits({"category":"some_category"})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeMusicCategoryHits_should_call_parseDOM_to_get_videos(self):
		
		result, status = self.scraper.scrapeMusicCategoryHits({"category":"some_category"})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeMusicCategoryHits_should_return_list_of_video_ids(self):
		sys.modules["__main__"].utils.extractVID.return_value = ["some_id_1","some_id_2","some_id_3"]
		
		result, status = self.scraper.scrapeMusicCategoryHits({"category":"some_category"})
		
		assert(len(result) == 3)
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_2")
		assert(result[2] == "some_id_3")
		
	def test_searchDisco_should_call_createUrl_to_get_seach_url(self):
		
		result, status = self.scraper.searchDisco({"search":"some_search"})		
		
		self.scraper.createUrl.assert_any_call({"search":"some_search"})
		
	def test_searchDisco_should_call_createUrl_to_get_mixlist_url(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content&v=some_video_id&list=some_mix_list&blablabla","status":200}
		
		result, status = self.scraper.searchDisco({"search":"some_search"})		
		
		self.scraper.createUrl.assert_any_call({'mix_list_id': 'some_mix_list', 'search': 'some_search', 'videoid': 'some_video_id'})
		
	def test_searchDisco_should_call_fetchPage_to_get_search_result(self):
		
		self.scraper.searchDisco({"search":"some_search"})
				
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_searchDisco_should_call_fetchPage_to_get_mix_list_content(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content&v=some_video_id&list=some_mix_list&blablabla","status":200}
		
		self.scraper.searchDisco({"search":"some_search"})		
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_searchDisco_should_call_parseDOM_to_get_video_list(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content&v=some_video_id&list=some_mix_list&blablabla","status":200}
		
		self.scraper.searchDisco({"search":"some_search"})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_searchDisco_should_return_list_of_videoids(self):
		sys.modules["__main__"].common.parseDOM.return_value = ["some_id_1,some_id_2,some_id_3"]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content&v=some_video_id&list=some_mix_list&blablabla","status":200}
		
		result, status = self.scraper.searchDisco({"search":"some_search"})		
		
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_2")
		assert(result[2] == "some_id_3")
		
	def test_scrapeDiscoTopArtist_should_call_createUrl_to_get_proper_url(self):
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		self.scraper.createUrl.assert_any_call({"thumb":"true"})
		
	def test_scrapeDiscoTopArtist_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})

	def test_scrapeDiscoTopArtist_should_call_parseDOM_to_find_artist_list(self):
		sys.modules["__main__"].common.parseDOM.return_value = ["some_id_1,some_id_2,some_id_3,some_id_4"]
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeDiscoTopArtist_should_call_utils_makeAscii_to_encode_title(self):
		sys.modules["__main__"].common.parseDOM.return_value = ["some_artist"]
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		sys.modules["__main__"].utils.makeAscii.assert_any_call("some_artist")
		
	def test_scrapeDiscoTopArtist_should_call_storage_retrieve_to_get_thumbnail(self):
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		assert(sys.modules["__main__"].storage.retrieve.call_count > 0)
		
	def test_scrapeDiscoTopArtist_should_return_proper_structure(self):
		
		result, status = self.scraper.scrapeDiscoTopArtist({})		
		
		print repr(result)
		assert(result[0].has_key("Title"))
		assert(result[0]["scraper"] == "search_disco")
		assert(result[0].has_key("path"))
		assert(result[0].has_key("search"))
		assert(result[0].has_key("thumbnail"))
		
	def test_scrapeEducationCategories_should_call_createUrl_to_get_proper_url(self):
		
		self.scraper.scrapeEducationCategories({})		
		
		self.scraper.createUrl.assert_any_call({})
				
	def test_scrapeEducationCategories_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationCategories({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationCategories_should_call_parseDOM_to_find_categories(self):
		
		self.scraper.scrapeEducationCategories({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def ttest_scrapeEducationCategories_should_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def test_scrapeEducationSubCategories_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationSubCategories({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationSubCategories_should_parseDOM_to_find_categories(self):
		
		self.scraper.scrapeEducationSubCategories({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def ttest_scrapeEducationSubCategories_should_call_replaceHtmlCodes_to_remove_html_chars_from_title(self):
		assert(False)
		
	def ttest_scrapeEducationSubCategories_should_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def test_scrapeEducationCourses_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationCourses({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationCourses_should_call_parseDOM_to_find_categories(self):
		
		self.scraper.scrapeEducationCourses({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def ttest_scrapeEducationCourses_should_call_replaceHtmlCodes_to_remove_html_chars_from_title(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_call_return_proper_structure(self):
		assert(False)
		
	def ttest_scrapeEducationCourses_should_prepend_a_a_courses_link(self):
		assert(False)
		
	def ttest_scrapeEducationVideos_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def test_scrapeEducationVideos_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationVideos({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationVideos_should_call_parseDOM_to_find_pagination(self):
		
		self.scraper.scrapeEducationVideos({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
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
		
	def test_scrapeRecommended_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeRecommended({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url","login":"true"})
		
	def test_scrapeRecommended_should_parseDOM_to_get_video_ids(self):
		
		self.scraper.scrapeRecommended({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def ttest_scrapeRecommended_should_return_list_of_video_ids(self):
		assert(False)
		
	def ttest_scrapeWatchLater_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def test_scrapeWatchLater_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeWatchLater({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url","get_redirect":"true","login":"true"})
		
	def ttest_scrapeWatchLater_should_call_parseDOM_to_find_redirect_to_playlist(self):
		assert(False)
		
	def ttest_scrapeWatchLater_should_call_feeds_list_if_playlist_is_found(self):
		assert(False)
		
	def ttest_scrapeShowEpisodes_should_call_createUrl_to_get_proper_url(self):
		assert(False)
		
	def test_scrapeShowEpisodes_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeShowEpisodes({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeShowEpisodes_should_call_parseDOM_to_find_videoids(self):
		
		self.scraper.scrapeShowEpisodes({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeShowEpisodes_should_call_parseDOM_to_find_next_url(self):
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)
		
	def ttest_scrapeShowEpisodes_should_fetch_entire_list(self):
		assert(False)
		'''
	def ttest_scrapeShow_should_call_createUrl_to_get_proper_url(self):
	def ttest_scrapeShow_should_call_fetchPage_to_get_page_content(self):
	def ttest_scrapeShow_should_parseDOM_to_find_videoids(self):
	def ttest_scrapeShow_should_cacheFunction_with_scrape_show_episodes_pointer_if_season_list_isnt_found(self):
	def ttest_scrapeShow_should_cacheFunction_with_scrape_show_seasons_pointer_if_season_list_is_found(self):
		
	def ttest_scrapeShowSeasons_should_call_parseDOM_to_find_seasons(self):
	def ttest_scrapeShowSeasons_should_call_language_to_get_seasons_string(self):
	def ttest_scrapeShowSeasons_should_return_proper_structure(self):
		
	def ttest_scrapeShowsGrid_should_call_createUrl_to_get_proper_url(self):
	def ttest_scrapeShowsGrid_should_call_fetchPage_to_get_page_content(self):
	def ttest_scrapeShowsGrid_should_call_parseDOM_to_find_next_url(self):
	def ttest_scrapeShowsGrid_should_call_parseDOM_to_find_videoids(self):
	def ttest_scrapeShowsGrid_should_call_common_striptags_to_remove_html_tags_from_episode_count(self):
	def ttest_scrapeShowsGrid_should_call_utils_replaceHtmlCodes_to_remove_html_chars_from_title(self):
	
	def ttest_scrapeYouTubeTop100_should_call_createUrl_to_get_proper_url(self):
	def ttest_scrapeYouTubeTop100_should_call_fetchPage_to_get_page_content(self):
	def ttest_scrapeYouTubeTop100_should_call_parseDOM_to_find_video_ids(self):
	
	def ttest_scrapeMovieSubCategory_should_call_createUrl_to_get_proper_url(self):
	def ttest_scrapeMovieSubCategory_should_call_fetchPage_to_get_page_content(self):
	def ttest_scrapeMovieSubCategory_should_call_utils_replaceHtmlCodes_to_remove_html_chars_from_title(self):
	def ttest_scrapeMovieSubCategory_should_return_proper_structure(self):
	
	def ttest_scrapeMoviesGrid_should_call_createUrl_to_get_proper_url(self):
	def ttest_scrapeMoviesGrid_should_call_fetchPage_to_get_page_content(self):
	def ttest_scrapeMoviesGrid_should_call_parseDOM_to_find_next_url(self):
	def ttest_scrapeMoviesGrid_should_call_parseDOM_to_find_videoids(self):
	def ttest_scrapeMoviesGrid_should_call_parseDOM_to_find_thumbnails(self):
	def ttest_scrapeMoviesGrid_should_return_list_of_videoid_and_thumbnail_tuples(self):
	
	def ttest_getNewResultsFunction_should_set_proper_params_for_searchDisco_if_search_diso_is_in_params(self):

	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeLikedVideos_if_liked_videos_is_in_params(self):

	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeDiscoTop50_if_disco_top_50_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeRecommended_if_recommended_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeYouTubeTop100_if_search_diso_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeDiscoTopArtist_if_disco_top_artist_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeArtist_if_music_artist_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersListFormat_if_trailers_scraper_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeSimilarArtists_if_similar_artist_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategoryHits_if_music_hits_and_category_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategoryArtists_if_music_artist_and_category_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategories_if_music_hits_or_music_artist_is_in_params_and_category_is_not(self):							
	
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeCategoryList_if_scraper_is_categories_and_category_is_not_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeCategoryList_if_scraper_is_movies_and_category_is_not_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeCategoryList_if_scraper_is_shows_and_category_is_not_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeShowsGrid_if_scraper_is_shows_and_category_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeShow_if_scraper_is_shows_and_show_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeMoviesGrid_if_scraper_is_movies_and_category_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeMovieSubCategory_if_scraper_is_movies_and_subcategory_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeEducationCategories_if_scraper_is_education(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeEducationSubCategories_if_scraper_is_education_and_category_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeEducationCourses_if_scraper_is_education_and_course_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeEducationVideos_if_scraper_is_education_and_playlist_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeCategoriesGrid_if_scraper_is_categories_and_category_is_in_params(self):
	def ttest_getNewResultsFunction_should_set_proper_params_for_scrapeGridFormat_if_trailer_is_in_params(self):
	
	def ttest_createUrl_should_return_proper_url_for_scraper_param(self):
	def ttest_createUrl_should_return_proper_url_for_categories_scraper(self):
	def ttest_createUrl_should_return_proper_url_for_shows_scraper(self):
	def ttest_createUrl_should_return_proper_url_for_shows_scraper_with_show(self):
	def ttest_createUrl_should_return_proper_url_for_shows_scraper_with_season(self):
	def ttest_createUrl_should_return_proper_url_for_education_scraper(self):
	def ttest_createUrl_should_return_proper_url_for_movies_scraper(self):
	def ttest_createUrl_should_return_proper_url_for_movies_scraper_with_category(self):
	def ttest_createUrl_should_return_proper_url_for_music_top_100_scraper(self):
'''	
if __name__ == '__main__':
	nose.runmodule()
