import BaseTestCase
import nose, sys

class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
        def test_plugin_should_scrape_live_list_correctly(self):
                self.navigation.listMenu({"feed":"feed_live", "path":"/root/explore/movies"})

                self.assert_directory_count_greater_than_or_equals(10)
                self.assert_directory_count_less_than_or_equals(51)
                self.assert_directory_is_a_video_list()
		self.assert_directory_items_should_have_external_thumbnails()
                self.assert_directory_items_contain("category")
                #assert(False)
	
	def test_plugin_should_list_search_video_list_correctly(self):
		self.navigation.listMenu({"feed":"search", "search":"Star Craft 2", "path":"/root/favorites"})
		
		self.assert_directory_count_greater_than_or_equals(5)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_list_related_video_list_correctly(self):
		self.navigation.listMenu({"feed":"related", "videoid":"byv-wpqDydI", "path":"/root/favorites"})
		
		self.assert_directory_count_greater_than_or_equals(5)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()

if __name__ == "__main__":
	nose.runmodule()
