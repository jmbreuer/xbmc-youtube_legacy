import BaseTestCase
import nose, sys

class TestYouTubeMusicScraper(BaseTestCase.BaseTestCase):
	
	def test_plugin_should_list_advanced_folder_structure_when_user_is_logged_in(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-logged-in.xml")
		sys.modules["__main__"].settings.setSetting("oauth2_access_token","some_token")
		
		self.navigation.listMenu()
		
		#we probably need some better asserts here
		self.assert_directory_count_greater_than_or_equals(10)
		self.assert_directory_count_less_than_or_equals(50)
		self.assert_directory_is_a_folder_list()
	
	def test_plugin_should_list_basic_folder_structure_when_user_is_not_logged_in(self):
		
		self.navigation.listMenu()
		
		#we probably need some better asserts here
		self.assert_directory_count_greater_than_or_equals(3)
		self.assert_directory_count_less_than_or_equals(10)
		self.assert_directory_is_a_folder_list()
		
	def test_plugin_should_list_subfolders_when_user_navigates_to_a_folder(self):
		
		self.navigation.listMenu({"path":"/root/explore"})
		
		#we probably need some better asserts here
		self.assert_directory_count_greater_than_or_equals(8)
		self.assert_directory_count_less_than_or_equals(10)
		self.assert_directory_is_a_folder_list()
	
if __name__ == "__main__":
	nose.runmodule()