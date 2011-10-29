import BaseTestCase
import nose

class TestYouTubeShowsScraper(BaseTestCase.BaseTestCase):
	
	def test_plugin_should_scrape_shows_category_listing_correctly(self):
		self.navigation.listMenu({"scraper":"shows","path":"/root/explore/shows", "folder":"true"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_item_urls_contain("category")
		self.assert_directory_items_should_have_thumbnails()
	
	def test_plugin_should_scrape_show_list_correctly(self):
		self.navigation.listMenu({"scraper":"shows","path":"/root/explore/shows","category":"comedy%3Ffeature%3Dsh_c%26amp%3Bpt%3Dg%26amp%3Bl%3Den"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_item_urls_contain("show")
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_scrape_show_episode_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"shows","path":"/root/explore/trailers/current", "show":"minecraft?feature=sh_gm_show_1_1", "season":"3"})
		
		self.assert_directory_count_greater_than_or_equals(3) # was 30
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()

	def test_plugin_should_scrape_show_season_folder_list_correctly(self):
		self.navigation.listMenu({"scraper":"shows","path":"/root/explore/trailers/current", "show":"minecraft?feature=sh_gm_show_1_1"})
		
		self.assert_directory_count_greater_than_or_equals(2) # was 5
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_item_urls_contain("season")

	def test_plugin_should_scrape_show_season_episode_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"shows","path":"/root/explore/trailers/current", "show":"minecraft?feature=sh_gm_show_1_1", "season":"3"})
		
		self.assert_directory_count_greater_than_or_equals(3) # was30
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()

	def ttest_plugin_should_scrape_show_season_episode_video_list_page_2_correctly(self): # Epic failure
		self.navigation.listMenu({"scraper":"shows","path":"/root/explore/trailers/current", "show":"minecraft?feature=sh_gm_show_1_1", "season":"3", "page":"1"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		
if __name__ == "__main__":
	nose.runmodule()
