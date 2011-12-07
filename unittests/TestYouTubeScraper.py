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
		sys.modules["__main__"].common.parseDOM.return_value = ["some_string","some_string","some_string"]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content","status":200}
		sys.modules["__main__"].common.makeAscii.return_value = "some_ascii_string"
		sys.modules["__main__"].common.replaceHTMLCodes.return_value = "some_html_free_string"
		sys.modules["__main__"].utils.extractVID.return_value = ["some_id_1","some_id_2","some_id_3"]
		sys.modules["__main__"].language.return_value = "some_language_string %s"
		sys.modules["__main__"].common.stripTags.return_value = "some_tag_less_string"
		sys.modules["__main__"].settings.getSetting.return_value = "1"
		sys.modules["__main__"].cache.cacheFunction.return_value = (["some_cached_string"], 200)
		
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
	
	def test_scrapeTrailersGridFormat_should_call_createUrl_to_get_proper_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		self.scraper.scrapeTrailersGridFormat()		
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeTrailersGridFormat_should_call_fetchPage_to_get_page_content(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		self.scraper.scrapeTrailersGridFormat()		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
	
	def test_scrapeTrailersGridFormat_should_call_parseDOM_to_find_next_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		self.scraper.scrapeTrailersGridFormat()		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeTrailersGridFormat_should_call_parseDOM_to_find_video_elements(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		self.scraper.scrapeTrailersGridFormat()		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)
				
	def test_scrapeTrailersGridFormat_should_call_extractVID_to_get_video_ids(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		result, status = self.scraper.scrapeTrailersGridFormat()
		
		assert(sys.modules["__main__"].utils.extractVID.call_count > 0)
		
	def test_scrapeTrailersGridFormat_should_return_list_of_video_id_and_thumbnail_touples(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]

		result, status = self.scraper.scrapeTrailersGridFormat({"artist":"some_artist"})
		
		assert(result[0][0] == "some_id_1")
		assert(result[0][1] == "some_string")
		assert(result[1][0] == "some_id_2")
		assert(result[1][1] == "some_string")
		assert(result[2][0] == "some_id_3")
		assert(result[2][1] == "some_string")

	def test_scrapeMusicCategories_should_call_createUrl_to_get_proper_url(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		self.scraper.createUrl.assert_any_call({})
	
	def test_scrapeMusicCategories_should_call_core_fetchPage_to_get_html_conten(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeMusicCategories_should_call_utils_makeAscii_to_encode_title(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		sys.modules["__main__"].common.makeAscii.assert_any_call("some_string")
		
	def test_scrapeMusicCategories_should_call_replaceHTMLCodes_to_remove_html_formating(self):
		
		result, status = self.scraper.scrapeMusicCategories()
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call("some_ascii_string")
		
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
		
	
	def test_scrapeArtist_should_call_extractVID_to_get_video_ids(self):
		
		result, status = self.scraper.scrapeArtist({"artist":"some_artist"})
		
		assert(sys.modules["__main__"].utils.extractVID.call_count > 0)
	
	def test_scrapeArtist_should_return_list_of_video_ids(self):
		
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
		
		sys.modules["__main__"].common.makeAscii.assert_any_call("some_string")
		
	def test_scrapeSimilarArtists_should_call_replaceHTMLCodes_to_remove_html_formating(self):
		
		result, status = self.scraper.scrapeSimilarArtists({"artist":"some_artist"})		
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call("some_ascii_string")

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
		
		sys.modules["__main__"].common.makeAscii.assert_any_call("some_string")
		
	def test_scrapeMusicCategoryArtists_should_call_replaceHTMLCodes_to_remove_html_formating(self):
		
		result, status = self.scraper.scrapeMusicCategoryArtists({"category":"some_category"})		
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call("some_ascii_string")
		
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
		
	def test_scrapeMusicCategoryHits_should_call_extractVID_to_get_list_of_video_ids(self):
		
		result, status = self.scraper.scrapeMusicCategoryHits({"category":"some_category"})
		
		assert(sys.modules["__main__"].utils.extractVID.call_count > 0)
		
	def test_scrapeMusicCategoryHits_should_return_list_of_video_ids(self):
		
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
		
		self.scraper.createUrl.assert_any_call({'mix_list_id': 'some_mix_list', 'search': 'some_search', 'disco_videoid': 'some_video_id'})
		
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
		
		sys.modules["__main__"].common.makeAscii.assert_any_call("some_artist")
		
	def test_scrapeDiscoTopArtist_should_call_storage_retrieve_to_get_thumbnail(self):
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		assert(sys.modules["__main__"].storage.retrieve.call_count > 0)
		
	def test_scrapeDiscoTopArtist_should_return_proper_structure(self):
		
		result, status = self.scraper.scrapeDiscoTopArtist({})		
		
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
		
	def test_scrapeEducationCategories_should_return_proper_structure(self):
				
		result, status = self.scraper.scrapeEducationCategories({})

		assert(result[0].has_key("category"))
		assert(result[0].has_key("icon"))
		assert(result[0]["scraper"] == "education")
		assert(result[0].has_key("Title"))
				
	def test_scrapeEducationSubCategories_should_call_createUrl_to_get_proper_url(self):
		
		self.scraper.scrapeEducationSubCategories({})		
		
		self.scraper.createUrl.assert_any_call({})
		
	def test_scrapeEducationSubCategories_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationSubCategories({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationSubCategories_should_parseDOM_to_find_categories(self):
		
		self.scraper.scrapeEducationSubCategories({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeEducationSubCategories_should_call_replaceHTMLCodes_to_remove_html_chars_from_title(self):
		
		self.scraper.scrapeEducationSubCategories({})
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call("some_string")
		
	def test_scrapeEducationSubCategories_should_return_proper_structure(self):
		
		result , status = self.scraper.scrapeEducationSubCategories({})
		
		assert(result[0].has_key("icon"))
		assert(result[0].has_key("videos"))
		assert(result[0]["scraper"] == "education")
		assert(result[0].has_key("Title"))
		assert(result[1].has_key("icon"))
		assert(result[1].has_key("courses"))
		assert(result[1]["scraper"] == "education")
		assert(result[1].has_key("Title"))
		
	def test_scrapeEducationCourses_should_call_createUrl_to_get_proper_url(self):
		
		self.scraper.scrapeEducationCourses({})
		
		self.scraper.createUrl.assert_any_call({})
		
	def test_scrapeEducationCourses_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationCourses({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationCourses_should_call_parseDOM_to_find_categories(self):
		
		self.scraper.scrapeEducationCourses({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeEducationCourses_should_call_replaceHTMLCodes_to_remove_html_chars_from_title(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"]]
		
		self.scraper.scrapeEducationCourses({})
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call("some_title2")
		
	def test_scrapeEducationCourses_should_call_return_proper_structure(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"]]
		
		result, status = self.scraper.scrapeEducationCourses({})
		
		assert(result[1].has_key("thumbnail"))
		assert(result[1].has_key("playlist"))
		assert(result[1].has_key("icon"))
		assert(result[1].has_key("scraper"))
		assert(result[1].has_key("Title"))
		
	def test_scrapeEducationCourses_should_prepend_a_a_courses_link(self):

		result, status = self.scraper.scrapeEducationCourses({})
		
		assert(result[0].has_key("videos"))
		assert(result[0].has_key("Title"))
		assert(result[0].has_key("icon"))
		assert(result[0]["scraper"] == "education")
		
	def test_scrapeEducationVideos_should_call_createUrl_to_get_proper_url(self):

		self.scraper.scrapeEducationVideos({})		
		
		self.scraper.createUrl.assert_any_call({})
		
	def test_scrapeEducationVideos_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeEducationVideos({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeEducationVideos_should_call_parseDOM_to_find_pagination(self):
		
		self.scraper.scrapeEducationVideos({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeEducationVideos_should_call_parseDOM_to_find_videos(self):
		
		self.scraper.scrapeEducationVideos({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
				
	def test_scrapeEducationVideos_should_call_extractVID_to_get_list_of_video_ids(self):
		
		result, status = self.scraper.scrapeEducationVideos({})
		
		assert(sys.modules["__main__"].utils.extractVID.call_count > 0)

	def test_scrapeEducationVideos_should_return_list_of_video_ids(self):
		
		result, status = self.scraper.scrapeEducationVideos({})
		
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_2")
		assert(result[2] == "some_id_3")
				
	def test_scrapeLikedVideos_should_call_createUrl_to_get_proper_url(self):
		#sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content_&p=some_playlist&_blabal", "status":200}
		
		self.scraper.scrapeLikedVideos({})
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeLikedVideos_should_call_core_fetchPage_to_get_page_content(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content_&p=some_playlist&_blabal", "status":200}
		
		self.scraper.scrapeLikedVideos({})
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url","login":"true"})

	def test_scrapeLikedVideos_should_call_parseDOM_to_find_playlist(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"some_content_&p=some_playlist&_blabal", "status":200}
		
		self.scraper.scrapeLikedVideos({})
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeShowEpisodes_should_call_createUrl_to_get_proper_url(self):
		
		self.scraper.scrapeShowEpisodes({})		
		
		self.scraper.createUrl.assert_any_call({})
		
	def test_scrapeShowEpisodes_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeShowEpisodes({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeShowEpisodes_should_call_parseDOM_to_find_video_elements(self):
		
		self.scraper.scrapeShowEpisodes({})
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
	
	def test_scrapeShowEpisodes_should_return_list_of_video_ids(self):
		sys.modules["__main__"].common.parseDOM.return_value = ["some_id_1","some_id_2","some_id_3"]
				
		result, status = self.scraper.scrapeShowEpisodes({})		
		
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_2")
		assert(result[2] == "some_id_3")
	
	def test_scrapeShowEpisodes_should_call_parseDOM_to_find_next_url(self):
		
		self.scraper.scrapeDiscoTopArtist({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)
		
	def test_scrapeShowEpisodes_should_fetch_entire_list(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string start=20"],["some_string"],["some_string"],["some_string"],["some_string"],[],[]]
		
		self.scraper.scrapeShowEpisodes({})		
		
		assert(sys.modules["__main__"].core._fetchPage.call_count > 1)
		
	def test_scrapeShow_should_call_createUrl_to_get_proper_url(self):

		self.scraper.scrapeShow({})		
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeShow_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeShow({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
				
	def test_scrapeShow_should_call_cacheFunction_with_scrape_show_episodes_pointer_if_season_list_isnt_found(self):
		
		self.scraper.scrapeShow({})
		
		sys.modules["__main__"].cache.cacheFunction.assert_called_with(self.scraper.scrapeShowEpisodes, {})
	
	def test_scrapeShow_should_call_cacheFunction_with_scrape_show_seasons_pointer_if_season_list_is_found(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":'something class="seasons "',"status":200}
		
		self.scraper.scrapeShow({"batch":"something"})
		
		sys.modules["__main__"].cache.cacheFunction.assert_called_with(self.scraper.scrapeShowSeasons, 'something class="seasons "', {"folder":"true"})
		
	def test_scrapeShowSeasons_should_call_parseDOM_to_find_seasons(self):
		
		self.scraper.scrapeShowSeasons({})
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeShowSeasons_should_call_language_to_get_seasons_string(self):
		
		self.scraper.scrapeShowSeasons({})
		
		sys.modules["__main__"].language.assert_called_with(30058)
	
	def test_scrapeShowsGrid_should_call_createUrl_to_get_proper_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"],["some_string","some_title4"],[],[]]
		
		self.scraper.scrapeShowsGrid({})		
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeShowsGrid_should_call_fetchPage_to_get_page_content(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"],["some_string","some_title4"],[],[]]
		
		self.scraper.scrapeShowsGrid({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
	
	def test_scrapeShowsGrid_should_call_parseDOM_to_find_next_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"],["some_string","some_title4"],[],[]]
		
		self.scraper.scrapeShowsGrid({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeShowsGrid_should_call_parseDOM_to_find_videoids(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"],["some_string","some_title4"],[],[]]
		
		self.scraper.scrapeShowsGrid({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)
		
	def test_scrapeShowsGrid_should_call_common_stripTags_to_remove_html_tags_from_episode_count(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"],["some_string","some_title4"],[],[]]
		
		self.scraper.scrapeShowsGrid({})		
		
		sys.modules["__main__"].common.stripTags.assert_called_with("some_title4")
		
	def test_scrapeShowsGrid_should_call_utils_replaceHTMLCodes_to_remove_html_chars_from_title(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],["some_string","some_title3"],["some_string","some_title4"],[],[]]
		
		self.scraper.scrapeShowsGrid({})		
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call('some_string (some_tag_less_string)')
		
	def test_scrapeYouTubeTop100_should_call_createUrl_to_get_proper_url(self):
		self.scraper.scrapeYouTubeTop100({})		
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeYouTubeTop100_should_call_fetchPage_to_get_page_content(self):
		self.scraper.scrapeYouTubeTop100({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeYouTubeTop100_should_call_parseDOM_to_find_video_elements(self):		
		
		self.scraper.scrapeYouTubeTop100({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
				
	def test_scrapeYouTubeTop100_should_return_list_of_video_ids(self):
		sys.modules["__main__"].common.parseDOM.return_value = ["some_id_1","some_id_2","some_id_3"]
		
		result , status = self.scraper.scrapeYouTubeTop100({})		
		
		assert(result[0] == "some_id_1")
		assert(result[1] == "some_id_2")
		assert(result[2] == "some_id_3")
		
	def test_scrapeMovieSubCategory_should_call_createUrl_to_get_proper_url(self):
		
		self.scraper.scrapeMovieSubCategory({})		
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeMovieSubCategory_should_call_fetchPage_to_get_page_content(self):
		
		self.scraper.scrapeMovieSubCategory({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})

	def test_scrapeMovieSubCategory_should_call_utils_replaceHTMLCodes_to_remove_html_chars_from_title(self):

		self.scraper.scrapeMovieSubCategory({})		
		
		sys.modules["__main__"].common.replaceHTMLCodes.assert_any_call('some_string')
		
	def test_scrapeMovieSubCategory_should_return_proper_structure(self):

		result, status = self.scraper.scrapeMovieSubCategory({})		
		
		assert(result[0].has_key("category"))
		assert(result[0].has_key("Title"))
		assert(result[0].has_key("thumbnail"))
		assert(result[0]["scraper"] == "movies")
		
	def test_scrapeMoviesGrid_should_call_createUrl_to_get_proper_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["0"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],[],[]]
		
		self.scraper.scrapeMoviesGrid({})
		
		self.scraper.createUrl.assert_any_call({})

	def test_scrapeMoviesGrid_should_call_fetchPage_to_get_page_content(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["0"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],[],[]]
		
		self.scraper.scrapeMoviesGrid({})		
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
				
	def test_scrapeMoviesGrid_should_call_parseDOM_to_find_next_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["0"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],[],[]]
		
		self.scraper.scrapeMoviesGrid({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
		
	def test_scrapeMoviesGrid_should_call_parseDOM_to_find_videoids(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["0"],["some_string"],["some_string","some_title1"],["some_string","some_title2"],[],[]]
		
		self.scraper.scrapeMoviesGrid({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)

	def test_scrapeMoviesGrid_should_call_parseDOM_to_find_thumbnails(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["0"],["some_string"],["some_string"],["some_string","some_title2"],[],[]]
		
		self.scraper.scrapeMoviesGrid({})		
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 2)
		
	def test_scrapeMoviesGrid_should_return_list_of_videoid_and_thumbnail_tuples(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_video_id"],["some_thumb"],[],[]]
		
		result, status = self.scraper.scrapeMoviesGrid({})		
		
		assert(result[0][0] == "some_video_id")
		assert(result[0][1] == "some_thumb")
	

	def test_getNewResultsFunction_should_set_proper_params_for_searchDisco_if_scraper_is_search_diso(self):
		params = {"scraper":"search_disco"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["batch"] == "true")
		assert(params["new_results_function"] == self.scraper.searchDisco)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeLikedVideos_if_scraper_is_liked_videos(self):
		params = {"scraper":"liked_videos"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["batch"] == "true")
		assert(params["new_results_function"] == self.scraper.scrapeLikedVideos)
	
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeYouTubeTop100_if_scraper_is_music_top100(self):
		params = {"scraper":"music_top100"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["batch"] == "true")
		assert(params["new_results_function"] == self.scraper.scrapeYouTubeTop100)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeDiscoTopArtist_if_scraper_is_disco_top_artist(self):
		params = {"scraper":"disco_top_artist"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["folder"] == "true")
		assert(params["new_results_function"] == self.scraper.scrapeDiscoTopArtist)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeArtist_if_scraper_is_music_artist(self):
		params = {"scraper":"music_artist"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["batch"] == "true")
		assert(params["new_results_function"] == self.scraper.scrapeArtist)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersListFormat_if_scraper_is_latest_trailers(self):
		params = {"scraper":"latest_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersListFormat)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersListFormat_if_scraper_is_latest_game_trailers(self):
		params = {"scraper":"latest_game_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersListFormat)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeSimilarArtists_if_scraper_is_similar_artist(self):
		params = {"scraper":"similar_artist"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["folder"] == "true")
		assert(params["new_results_function"] == self.scraper.scrapeSimilarArtists)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategoryHits_if_scraper_is_music_hits_and_category_is_in_params(self):
		params = {"scraper":"music_hits","category":"some_category"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeMusicCategoryHits)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategoryArtists_if_scraper_is_music_artists_and_category_is_in_params(self):
		params = {"scraper":"music_artists","category":"some_category"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeMusicCategoryArtists)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategories_if_scraper_is_music_artist_and_category_is_not_in_params(self):
		params = {"scraper":"music_artists"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeMusicCategories)
	
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeMusicCategories_if_scraper_is_music_hits_and_category_is_not_in_params(self):
		params = {"scraper":"music_hits"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeMusicCategories)
				
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategoryList_if_scraper_is_movies_and_category_is_not_in_params(self):
		params = {"scraper":"movies"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeCategoryList)
	
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeCategoryList_if_scraper_is_shows_and_category_is_not_in_params(self):
		params = {"scraper":"shows"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeCategoryList)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeShowsGrid_if_scraper_is_shows_and_category_is_in_params(self):
		params = {"scraper":"shows","category":"some_category"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeShowsGrid)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeShow_if_scraper_is_shows_and_show_is_in_params(self):
		params = {"scraper":"shows","show":"some_show"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeShow)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeMoviesGrid_if_scraper_is_movies_and_category_is_in_params(self):
		params = {"scraper":"movies", "category":"some_category"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeMoviesGrid)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeMovieSubCategory_if_scraper_is_movies_and_subcategory_is_in_params(self):
		params = {"scraper":"movies","subcategory":"some_subcategory","category":"some_category"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeMovieSubCategory)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeEducationCategories_if_scraper_is_education(self):
		params = {"scraper":"education"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeEducationCategories)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeEducationSubCategories_if_scraper_is_education_and_category_is_in_params(self):
		params = {"scraper":"education","category":"some_category"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeEducationSubCategories)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeEducationCourses_if_scraper_is_education_and_course_is_in_params(self):
		params = {"scraper":"education","courses":"some_course"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeEducationCourses)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeEducationVideos_if_scraper_is_education_and_playlist_is_in_params(self):
		params = {"scraper":"education","playlist":"some_playlist"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeEducationVideos)
			
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersGridFormat_if_scraper_is_current_trailers(self):
		params = {"scraper":"current_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)
		
	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersGridFormat_if_scraper_is_game_trailers(self):
		params = {"scraper":"game_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersGridFormat_if_scraper_is_popular_game_trailers(self):
		params = {"scraper":"popular_game_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeGridFormat_if_scraper_is_popular_trailers(self):
		params = {"scraper":"popular_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersGridFormat_if_scraper_is_trailers(self):
		params = {"scraper":"trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersGridFormat_if_scraper_is_upcoming_game_trailers(self):
		params = {"scraper":"upcoming_game_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)

	def test_getNewResultsFunction_should_set_proper_params_for_scrapeTrailersGridFormat_if_scraper_is_upcoming_trailers(self):
		params = {"scraper":"upcoming_trailers"}
		
		self.scraper.getNewResultsFunction(params)
		
		assert(params["new_results_function"] == self.scraper.scrapeTrailersGridFormat)
				
	def test_createUrl_should_return_proper_url_for_shows_scraper(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"shows"})
		
		assert(url[:url.rfind("?")] == self.scraper.urls["shows"])
				
	def test_createUrl_should_return_proper_url_for_shows_scraper_with_category(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"shows","category":"some_category"})

		assert(url[:url.rfind("/")] == self.scraper.urls["shows"])
		assert(url.find("some_category") > 0)

	def test_createUrl_should_return_proper_url_for_shows_scraper_with_show(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"shows","show":"some_show"})
		
		assert(url[:url.rfind("/")] == self.scraper.urls["shows"].replace("shows","show"))
		assert(url.find("some_show") > 0)
		
	def test_createUrl_should_return_proper_url_for_shows_scraper_with_season(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"shows","show":"some_show","season":"24"})
		
		assert(url[:url.rfind("/")] == self.scraper.urls["shows"].replace("shows","show"))
		assert(url.find("some_show") > 0)
		assert(url.find("s=") > 0)

	def test_createUrl_should_return_proper_url_for_education_scraper(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"education"})
		
		assert(url == self.scraper.urls["education"])
		
	def test_createUrl_should_return_proper_url_for_education_scraper_with_category(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"education", "category":"some_category"})
		
		assert(url == self.scraper.urls["education_category"] % "some_category")
		
	def test_createUrl_should_return_proper_url_for_education_scraper_with_subcategory(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"education", "subcategory":"some_subcategory"})
		
		assert(url == self.scraper.urls["education_category"] % "some_subcategory")
		
	def test_createUrl_should_return_proper_url_for_education_scraper_with_videos(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"education", "videos":"some_videos"})
		
		assert(url == self.scraper.urls["education_category"] % "some_videos")
		
	def test_createUrl_should_return_proper_url_for_education_scraper_with_courses(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"education", "courses":"some_courses"})
		
		assert(url == self.scraper.urls["education_category"] % "some_courses")
		
	def test_createUrl_should_return_proper_url_for_education_scraper_with_playlist(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"education", "playlist":"some_playlist"})
		
		assert(url == self.scraper.urls["playlist"] % "some_playlist")
	
	def test_createUrl_should_return_proper_url_for_movies_scraper(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"movies"})
		assert(url[:url.rfind("?")] == self.scraper.urls["movies"] )
		
	def test_createUrl_should_return_proper_url_for_movies_scraper_with_category(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"movies", "category":"some_category"})
		
		assert(url[:url.rfind("?")] == self.scraper.urls["main"] + "/movies/some_category")

	def test_createUrl_should_return_proper_url_for_movies_scraper_with_subcategory_and_category(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"movies", "subcategory":"true","category":"some_category"})
		
		assert(url[:url.rfind("?")] == self.scraper.urls["main"] + "/movies/some_category")
		assert(url.rfind("p=") < 0)
	
	def test_createUrl_should_return_proper_url_for_music_artist_with_artist(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"music_artist", "artist":"some_artist"})
		
		assert(url == self.scraper.urls["artist"] % "some_artist")
		
	def test_createUrl_should_return_proper_url_for_similar_artist_with_artist(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"similar_artist", "artist":"some_artist"})
		
		assert(url == self.scraper.urls["artist"] % "some_artist")
		
	def test_createUrl_should_return_proper_url_for_music_artists_with_category(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"music_artist","category":"some_category"})
		
		assert(url == self.scraper.urls["music"] + "some_category")
	
	def test_createUrl_should_return_proper_url_for_music_top_100(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"music_top100"})

		assert(url == self.scraper.urls["music"])		

	def test_createUrl_should_return_proper_url_for_search_disco(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"search_disco", "search":"some_search"})
		
		assert(url == self.scraper.urls["disco_search"] % "some_search")
	
	def test_createUrl_should_return_proper_url_for_search_disco_with_mix_list_and_videoid(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"search_disco", "search":"some_search", "mix_list_id":"some_mix_list_id", "disco_videoid":"some_videoid"})
		
		assert(url ==  self.scraper.urls["disco_mix_list"] % ("some_videoid", "some_mix_list_id"))
	
	def test_createUrl_should_return_proper_url_for_disco_top_artists(self):
		self.scraper = YouTubeScraper()
		
		url = self.scraper.createUrl({"scraper":"disco_top_artist"})
		
		assert(url == self.scraper.urls["disco_main"])
	
	def test_scrapeCategoriesList_should_call_parseDOM_to_find_categories(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		result, status = self.scraper.scrapeCategoryList()
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 0)
	
	def test_scrapeCategoryList_should_call_createUrl_to_get_correct_url(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		result, status = self.scraper.scrapeCategoryList()
		
		self.scraper.createUrl.assert_any_call({})
		
	def test_scrapeCategoryList_should_call_core_fetchPage_to_get_html_content(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		result, status = self.scraper.scrapeCategoryList()
		
		sys.modules["__main__"].core._fetchPage.assert_any_call({"link":"some_url"})
		
	def test_scrapeCategoryList_should_call_parseDOM_to_get_videos_container(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		result, status = self.scraper.scrapeCategoryList()
		
		assert(sys.modules["__main__"].common.parseDOM.call_count > 1)
		
	def test_scrapeCategoryList_should_return_proper_structure(self):
		sys.modules["__main__"].common.parseDOM.side_effect = [["some_string"],["some_string"],["some_string"],["some_string1","some_string2","some_string3"],["some_string"],["some_string"],["some_string"],[],[]]
		
		result, status = self.scraper.scrapeCategoryList()
		
		assert(result[0].has_key("category"))
		assert(result[0].has_key("thumbnail"))
		assert(result[0].has_key("Title"))
		assert(result[0]["scraper"] == "movies")		
	
	def test_paginator_should_call_cache_function_with_pointer_to_new_results_function_if_scraper_is_not_show(self):
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer"})
		
		sys.modules["__main__"].cache.cacheFunction.assert_called_with("some_function_pointer",{"scraper":"some_scraper","new_results_function":"some_function_pointer"})

	def test_paginator_should_call_new_results_function_pointer_if_scraper_is_show_and_show_is_in_params(self):
		self.scraper.scrapeShow = Mock()
		self.scraper.scrapeShow.return_value = (["some_string"],200)
		params = {"scraper":"show","new_results_function":self.scraper.scrapeShow, "show":"some_show"}

		result, status = self.scraper.paginator(params)
		
		sys.modules["__main__"].cache.cacheFunction.assert_called_with(self.scraper.scrapeShow,params)

	def test_paginator_should_return_error_if_no_results_are_found(self):
		sys.modules["__main__"].cache.cacheFunction.return_value = ([],303)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer"})
		
		assert(status == 303)
		assert(result == [])
		
	def test_paginator_should_not_return_error_when_no_results_are_found_if_scraper_is_youtube_top100(self):
		sys.modules["__main__"].storage.retrieve.return_value = ["some_store_value"]
		sys.modules["__main__"].cache.cacheFunction.return_value = ([],303)
		
		result, status = self.scraper.paginator({"scraper":"music_top100","new_results_function":"some_function_pointer"})
		
		assert(status == 200)
		assert(result == ["some_store_value"])

	def test_paginator_should_call_storage_retrieve_when_no_results_are_found_if_scraper_is_youtube_top100(self):
		sys.modules["__main__"].storage.retrieve.return_value = ["some_store_value"]
		sys.modules["__main__"].cache.cacheFunction.return_value = ([],303)
		
		result, status = self.scraper.paginator({"scraper":"music_top100","new_results_function":"some_function_pointer"})
		
		assert(sys.modules["__main__"].storage.retrieve.call_count > 0)
			
	def test_paginator_should_call_getBatchDetailsThumbnails_if_batch_is_thumbnails(self):
		sys.modules["__main__"].core.getBatchDetailsThumbnails.return_value = ([],200)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer", "batch":"thumbnails"})
		
		assert(sys.modules["__main__"].core.getBatchDetailsThumbnails.call_count > 0)
		
	def test_paginator_should_call_getBatchDetails_if_batch_is_set_but_not_thumbnails(self):
		sys.modules["__main__"].core.getBatchDetails.return_value = ([],200)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer", "batch":"true"})
		
		assert(sys.modules["__main__"].core.getBatchDetails.call_count > 0)
		
	def test_paginator_should_call_utils_addNextFolder_if_item_list_is_longer_than_per_page_count(self):
		sys.modules["__main__"].core.getBatchDetails.return_value = ([],200)
		videos = []
		i = 0
		while i < 50:
			videos.append("some_cached_string_" + str(i))
			i += 1
			
		sys.modules["__main__"].cache.cacheFunction.return_value = (videos, 200)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer", "batch":"true"})
		
		assert(sys.modules["__main__"].utils.addNextFolder.call_count > 0)
		
	def test_paginator_should_store_thumbnail_if_scraper_is_search_disco(self):
		sys.modules["__main__"].cache.cacheFunction.return_value = ([{"thumbnail":"some_cached_string"}], 200)
		
		result, status = self.scraper.paginator({"scraper":"search_disco","new_results_function":"some_function_pointer"})
		
		sys.modules["__main__"].storage.store.assert_called_with({'new_results_function': 'some_function_pointer', 'scraper': 'search_disco'}, 'some_cached_string', 'thumbnail')
		
	def test_paginator_should_store_thumbnail_if_scraper_is_music_artist(self):
		sys.modules["__main__"].cache.cacheFunction.return_value = ([{"thumbnail":"some_cached_string"}], 200)
		
		result, status = self.scraper.paginator({"scraper":"music_artist","new_results_function":"some_function_pointer"})
		
		sys.modules["__main__"].storage.store.assert_called_with({'new_results_function': 'some_function_pointer', 'scraper': 'music_artist'}, 'some_cached_string', 'thumbnail')
		
	def test_paginator_should_limit_list_length_if_its_longer_than_perpage(self):
		videos = []
		i = 0
		while i < 50:
			videos.append("some_cached_string_" + str(i))
			i += 1
			
		sys.modules["__main__"].cache.cacheFunction.return_value = (videos, 200)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer"})
		
		assert(len(result) == 15)
		
	def test_paginator_should_not_limit_list_length_if_fetch_all_is_set(self):
		videos = []
		i = 0
		while i < 50:
			videos.append("some_cached_string_" + str(i))
			i += 1
			
		sys.modules["__main__"].cache.cacheFunction.return_value = (videos, 200)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer","fetch_all":"true"})
		
		assert(len(result) == 50)
	
	def test_paginator_should_begin_list_at_correct_count_if_page_is_set(self):
		videos = []
		i = 0
		while i < 50:
			videos.append("some_cached_string_" + str(i))
			i += 1
			
		sys.modules["__main__"].cache.cacheFunction.return_value = (videos, 200)
		
		result, status = self.scraper.paginator({"scraper":"some_scraper","new_results_function":"some_function_pointer","page":"1"})
		
		assert(result[0] == "some_cached_string_15")
		assert(result[14] == "some_cached_string_29")
			
	def test_scrape_should_call_getNewResultsFunction(self):
		self.scraper.getNewResultsFunction = Mock()
		self.scraper.paginator = Mock()
		
		self.scraper.scrape()
		
		self.scraper.getNewResultsFunction.assert_called_with({})

	def test_scrape_should_call_paginator(self):
		self.scraper.getNewResultsFunction = Mock()
		self.scraper.paginator = Mock()
		
		self.scraper.scrape()
		
		self.scraper.paginator.assert_called_with({})
		
if __name__ == '__main__':
	nose.runmodule()
