import BaseTestCase
import nose


class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
	
	def ttest_plugin_should_scrape_categories_folder_list_correctly(self):
		self.navigation.listMenu({"scraper":"categories", "folder":"true", "path":"/root/explore/categories"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("category")
		
				
	def tvtest_plugin_should_scrape_category_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"categories", 'category':'cars', "path":"/root/explore/categories"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
if __name__ == "__main__":
	nose.runmodule()