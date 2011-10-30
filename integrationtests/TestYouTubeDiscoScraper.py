import BaseTestCase
import nose


class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
	
	def test_plugin_should_scrape_disco_search_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"search_disco", "search":"Lady Gaga", "path":"/root/explore/disco/new"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_almost_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		
				
	def test_plugin_should_scrape_disco_popular_artist_listing_correctly(self):
		self.navigation.listMenu({"scraper":"disco_top_artist", 'folder':'true', "path":"/root/explore/disco/popular"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_item_urls_contain("search")
	
if __name__ == "__main__":
	nose.runmodule()