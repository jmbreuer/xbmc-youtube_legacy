import BaseTestCase
import nose


class TestYouTubeTrailersScraper(BaseTestCase.BaseTestCase):
	
	def test_plugin_should_scrape_movie_category_listing_correctly(self):
		self.navigation.listMenu({"scraper":"movies", "folder":"true", "path":"/root/explore/movies"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_item_urls_contain("category")
	
	def test_plugin_should_scrape_movie_sub_category_listing_correctly(self):
		self.navigation.listMenu({"scraper":"movies", "folder":"true", "category":"indian_cinema", "subcategory":"true", "path":"/root/explore/movies"})
		
		self.assert_directory_count_greater_than_or_equals(1)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
	
	def test_plugin_should_scrape_movie_category_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"movies", "category":"comedy", "path":"/root/explore/movies"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
		self.assert_directory_should_have_next_folder()
	
	def test_plugin_should_scrape_movie_sub_category_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"movies", "category":"indian-cinema?fl=f&l=te&pt=g&st=f", "path":"/root/explore/movies"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
		self.assert_directory_should_have_next_folder()

	def ttest_plugin_should_scrape_us_rental_movie_listing_correctly(self):
		self.navigation.listMenu({"scraper":"movies", "path":"/root/explore/movies"})
		
		assert(False) # broken until further notice :D
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
	
if __name__ == "__main__":
	nose.runmodule()