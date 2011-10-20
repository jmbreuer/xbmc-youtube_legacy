import BaseTestCase
import nose, sys

class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
       	def test_plugin_should_list_user_favorites_video_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"favorites", "login":"true", "path":"/root/favorites"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_list_user_favorites_video_list_page_2_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"favorites", "login":"true", "page":"2","path":"/root/favorites"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_list_user_playlists_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"favorites", "login":"true","path":"/root/playlists"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("playlist")
	
	def test_plugin_should_list_user_playlists_page_2_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"favorites", "login":"true", "page":"1","path":"/root/playlists"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("playlist")
	
	def test_plugin_should_list_user_uploads_videos_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"uploads", 'login':'true', "path":"/root/uploads"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		
	def test_plugin_should_list_user_uploads_videos_list_page_2_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"uploads", 'login':'true', "page":"1", "path":"/root/uploads"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()

	def test_plugin_should_list_user_watch_later_video_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")

		self.navigation.listMenu({"feed":"watch_later", 'login':'true', "path":"/root/watch_later"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		self.assert_directory_items_contain("playlist_entry_id")
		
	def test_plugin_should_list_user_watch_later_video_list_page_2_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"watch_later", 'login':'true', "page":"1", "path":"/root/watch_later"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
		self.assert_directory_items_contain("playlist_entry_id")
	
	def test_plugin_should_list_user_contacts_folder_list_correctly_(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")

		self.navigation.listMenu({"feed":"contacts", 'login':'true', "path":"/root/contacts/smokey"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("contact")
		self.assert_directory_items_contain("options")

	def test_plugin_should_list_user_contact_folder_list_correctly_(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")

		self.navigation.listMenu({"options":"contact", "Tobuscus" 'login':'true', "path":"/root/contacts/smokey"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("contact")
		
	def test_plugin_should_list_user_subscriptions_folder_list_correctly_(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		
		self.navigation.listMenu({"feed":"subscriptions", 'login':'true', "path":"/root/subscriptions/something/smokey"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("playlist")
		
	def test_plugin_should_list_newsubscriptions_video_list_correctly(self):	
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"newsubscriptions", "login":"true", "path":"/root/subscriptions/new"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_list_subscription_favorties_video_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"subscription_favorites", "channel":"Chuggaconroy", "path":"/root/subscriptions"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()

	def test_plugin_should_list_subscription_favorties_video_list_page_2_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"subscription_favorites", "channel":"Chuggaconroy", "page":"1", "path":"/root/subscriptions"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_list_subscription_playlist_folder_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"subscription_playlists", "channel":"Chuggaconroy", "path":"/root/subscriptions"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_folder_list()
		self.assert_directory_items_contain("playlist")
	
	def test_plugin_should_list_subscription_uploads_video_list_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"subscription_uploads", "channel":"Chuggaconroy", "path":"/root/subscriptions"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
	def test_plugin_should_list_subscription_uploads_video_list_page_2_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		self.navigation.listMenu({"feed":"subscription_uploads", "channel":"Chuggaconroy", "page":"1", "path":"/root/subscriptions"})
		
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(51)
		self.assert_directory_is_a_video_list()
		self.assert_directory_contains_only_unique_video_items()
		self.assert_directory_items_should_have_external_thumbnails()
	
if __name__ == "__main__":
	nose.runmodule()
