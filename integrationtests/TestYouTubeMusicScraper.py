import BaseTestCase
import nose


class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
	
	def test_plugin_should_scrape_music_hits_category_listing_correctly(self):
		self.navigation.listMenu({"scraper":"music_hits", "category":"dance", "path":"/root/explore/music/hits"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("category")
		
	def ttest_plugin_should_scrape_music_artist_category_listing_correctly(self):
		self.navigation.listMenu({"scraper":"music_artist", "category":"dance",  "path":"/root/explore/music/artists"})
		
		self.assert_directory_count_greater_than_or_equals(1)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()

	def ttest_plugin_should_scrape_music_artist_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"music_artist", "artist":"lady gaga",  "path":"/root/explore/music/artists"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
	
	def ttest_plugin_should_scrape_similar_artist_listing_correctly(self):
		self.navigation.listMenu({"scraper":"similar_artists", "folder":"true", "artist":"lady gaga", "path":"/root/explore/music/artists"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
		self.assert_directory_should_have_next_folder()

	def ttest_plugin_should_scrape_youtube_top_100_video_list_correctly(self):
		self.navigation.listMenu({"scraper":"music_top100", "path":"/root/explore/music/top100"})
		
		assert(False)
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_thumbnails()
		self.assert_directory_items_should_have_poster_thumbnails()
		
	def ttest_plugin_should_remeber_recently_viewed_artist_and_present_them_correctly(self):
		assert(False)
	
if __name__ == "__main__":
	nose.runmodule()