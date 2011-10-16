import BaseTestCase
import unittest2
import nose, sys
from mock import Mock, patch


class YouTubeScraperTests(BaseTestCase.BaseTestCase):
	
	def ttest_scrapeTrailersListFormat_should_scraper_latest_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"latest_trailers","path":"/root/explore/trailers/latest"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		
	def test_scrapeTrailersListFormat_should_scraper_current_trailers_correctly(self):
		self.navigation.listMenu({"scraper":"current_trailers","path":"/root/explore/trailers/current"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		assert(False)

if __name__ == "__main__":
	nose.run()