import BaseTestCase
import nose


class TestYouTubeTrailersScraper(BaseTestCase.BaseTestCase):
	def test_plugin_should_scrape_live_list_correctly(self):
		self.navigation.listMenu({"feed":"feed_live", "folder":"true", "path":"/root/explore/movies"})

		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_contain("category")	
	
if __name__ == "__main__":
	nose.runmodule()
