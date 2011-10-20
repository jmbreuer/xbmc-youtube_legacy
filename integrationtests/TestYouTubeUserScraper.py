import BaseTestCase
import nose


class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
	
	def ttest_plugin_should_scrape_user_recommendations_video_list_correctly(self):
		
		self.navigation.listMenu({"scraper":"recommended", "login":"true", "path":"/root/explore/disco/new"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		
				
	def ttest_plugin_should_scrape_liked_videos_list_correctly(self):
		
		self.navigation.listMenu({"scraper":"liked_videos", 'login':'true', "path":"/root/explore/disco/popular"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
if __name__ == "__main__":
	nose.runmodule()