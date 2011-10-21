import BaseTestCase
import nose, sys

class TestYouTubePlayer(BaseTestCase.BaseTestCase):
	
	def ttest_plugin_should_queue_playlist_and_start_playback_if_user_select_play_all_in_playlist(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "videoid": "54VJWHL2K3I","playlist":"some_playlist"})

		assert(False)
	
	def ttest_plugin_should_queue_playlist_and_start_playback_if_user_select_play_all_outside_playlist(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "playlist":"some_playlist"})
		
		assert(False)
		
	def ttest_plugin_should_queue_disco_search_and_start_playback_if_user_selects_play_all_outside_disco_search(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"search_disco","search":"Lady Gaga"})
		
		assert(False)
	
	def ttest_plugin_should_queue_disco_search_and_start_playback_if_user_selects_play_all_in_disco_search(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"search_disco","search":"Lady Gaga", "videoid":"some_id"})
		
		assert(False)
	
	def ttest_plugin_should_queue_youtube_top_100_and_start_playback_if_user_selects_play_all_outside_list(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"music_top100"})
		
		assert(False)
		
	def ttest_plugin_should_queue_youtube_top_100_and_start_playback_if_user_selects_play_all_in_list(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"play_all", "scraper":"music_top100", "videoid":"some_id"})
		
		assert(False)

if __name__ == "__main__":
	nose.runmodule()
