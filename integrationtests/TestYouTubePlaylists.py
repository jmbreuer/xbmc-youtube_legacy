import BaseTestCase
import nose, sys

class TestYouTubePlayer(BaseTestCase.BaseTestCase):
	
	def test_plugin__should_queue_playlist_and_start_playback_if_user_selects_play_all_in_playlist(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "videoid": "Q7GVSx7yMaA","playlist":"E3E0C28746217FA6"})
		
		self.assert_playlist_count_greater_than_or_equals(30)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
		self.assert_playlist_videos_does_not_contain("6CaawfTDBM8")
		self.assert_playlist_videos_contain("Q7GVSx7yMaA")
	
	def test_plugin__should_queue_playlist_and_start_playback_if_user_selects_play_all_outside_playlist(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "playlist":"E3E0C28746217FA6"})
		
		self.assert_playlist_count_greater_than_or_equals(30)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
		
	def test_plugin__should_queue_disco_search_and_start_playback_if_user_selects_play_all_outside_disco_search(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"search_disco","search":"Linkin+Park"})
		
		self.assert_playlist_count_greater_than_or_equals(30)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
	
	def test_plugin__should_queue_disco_search_and_start_playback_if_user_selects_play_all_in_disco_search(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"search_disco","search":"Linkin+Park", "videoid":"8sgycukafqQ"})
		
		self.assert_playlist_count_greater_than_or_equals(30)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
		self.assert_playlist_videos_contain("8sgycukafqQ")
		self.assert_playlist_videos_does_not_contain("ysSxxIqKNN0")
	
	def test_plugin__should_queue_youtube_top_100_and_start_playback_if_user_selects_play_all_outside_list(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"music_top100"})
		
		self.assert_playlist_count_greater_than_or_equals(80)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
		
	def test_plugin__should_queue_user_watch_later_feed_if_user_selects_play_all_outside_list(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "user_feed":"watch_later"})
		
		self.assert_playlist_count_greater_than_or_equals(10)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
		
	def test_plugin__should_queue_user_new_subscriptions_feed_if_user_selects_play_all_on_external_user_outside_list(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "contact":"TobiasTheViking", "user_feed":"newsubscriptions"})
		
		self.assert_playlist_count_greater_than_or_equals(10)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
	
	def test_plugin__should_queue_users_liked_videos_if_user_selects_play_all_outside_list(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"liked_videos", "login":"true"})
		
		self.assert_playlist_count_greater_than_or_equals(10)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
		
	def test_plugin__should_queue_artist_video_list_if_user_selects_play_all_outside_list(self):
		
		self.navigation.executeAction({"action":"play_all", "scraper":"music_artist", "artist":"GxdCwVVULXewLzmGzHQKeUHShvQYOHQH"})
		
		self.assert_playlist_count_greater_than_or_equals(20)
		self.assert_directory_items_should_have_thumbnails()
		self.assert_playlist_contains_only_unique_video_items()
	
if __name__ == "__main__":
	nose.runmodule()