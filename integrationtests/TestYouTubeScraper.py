import BaseTestCase
import unittest2
import nose, sys
from mock import Mock, patch


class YouTubeScraperTests(BaseTestCase.BaseTestCase):
	
	def test_scrapeTrailersListFormat_should_scrape_latest_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"latest_trailers","path":"/root/explore/trailers/latest"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()

		
	def test_scrapeTrailersListFormat_should_scrape_current_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"current_trailers","path":"/root/explore/trailers/current"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()

	def test_scrapeTrailersListFormat_should_scrape_upcoming_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"upcoming_trailers","path":"/root/explore/trailers/upcoming"})
		
		self.assert_directory_count_greater_than_or_equals(1)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()

	def test_scrapeTrailersListFormat_should_scrape_popular_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"popular_trailers","path":"/root/explore/trailers/popular"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
		self.assert_directory_should_have_next_folder()

	def test_scrapeTrailersListFormat_should_scrape_latest_game_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"latest_game_trailers","path":"/root/explore/trailers/popular"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()

	def test_scrapeTrailersListFormat_should_scrape_popular_game_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"popular_game_trailers","path":"/root/explore/trailers/popular"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
		self.assert_directory_should_have_next_folder()
	
if __name__ == "__main__":
	nose.run()