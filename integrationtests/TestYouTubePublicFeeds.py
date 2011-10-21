import BaseTestCase
import nose, sys

class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
	
	def ttest_plugin_should_list_search_video_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"search", "search":"Star Craft 2", "path":"/root/favorites"})
		
		self.assert_directory_count_greater_than_or_equals(5)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def ttest_plugin_should_list_related_video_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"related", "videoid":"", "path":"/root/favorites"})
		
		self.assert_directory_count_greater_than_or_equals(5)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()

if __name__ == "__main__":
	nose.runmodule()
