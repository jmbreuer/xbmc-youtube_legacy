# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys, io

from  YouTubeLogin import YouTubeLogin 

class TestYouTubeUtils(BaseTestCase.BaseTestCase):
	
	def test_login_should_call_xbmc_open_settings(self):
		login = YouTubeLogin()
		
		login.login()
		
		sys.modules["__main__"].settings.openSettings.assert_called_with()
	
	def test_login_reset_oauth2_data_when_refreshing(self):
		settings = ["password","","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		login = YouTubeLogin()
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		sys.modules["xbmc"].executebuiltin = Mock()
		
		login.login()
		
		calls = sys.modules["__main__"].settings.setSetting.call_args_list
		assert(calls[0] == (("oauth2_access_token",""),{}))
		assert(calls[1] == (("oauth2_refresh_token",""),{}))
		assert(calls[2] == (("oauth2_expires at",""),{}))
		assert(calls[3] == (("nick",""),{}))
		
	def test_login_should_call_xbmc_execute_builtin(self):
		settings = ["password","","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		login = YouTubeLogin()
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		sys.modules["xbmc"].executebuiltin = Mock()
		
		login.login()
		
		sys.modules["xbmc"].executebuiltin.assert_called_with("Container.Refresh")
	
	def test_login_should_call_oRefreshToken(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		login = YouTubeLogin()
		sys.modules["__main__"].core._oRefreshToken.return_value = True
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		sys.modules["xbmc"].executebuiltin = Mock()
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
	
	def test_login_should_call_httpLogin_if_refresh_token_didnt_work(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		login = YouTubeLogin()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		sys.modules["xbmc"].executebuiltin = Mock()
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		login._httpLogin.assert_called_with({ "new": "true"})
	
	def test_login_should_call_apiLogin_if_refresh_token_didnt_work(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
		sys.modules["xbmc"].executebuiltin = Mock()
		login = YouTubeLogin()
		login._apiLogin = Mock()
		login._apiLogin.return_value = ("",200)
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",200)
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		login._httpLogin.assert_called_with({ "new": "true"})
		login._apiLogin.assert_called_with()
	
	def test_login_should_not_show_refreshing_folder_message_on_token_refresh_success(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		login = YouTubeLogin()
		sys.modules["__main__"].core._oRefreshToken.return_value = True
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		sys.modules["xbmc"].executebuiltin = Mock()
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		assert(sys.modules["__main__"].utils.showMessage.call_count == 0)
		assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)
	
	def test_login_should_show_error_message_on_failure(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		language = ["string1", "string2"]
		sys.modules["__main__"].language.side_effect = lambda x: language.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
		sys.modules["xbmc"].executebuiltin = Mock()
		login = YouTubeLogin()
		login._apiLogin = Mock()
		login._apiLogin.return_value = ("",303)
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",200)
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		login._httpLogin.assert_called_with({ "new": "true"})
		login._apiLogin.assert_called_with()
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("string2","",303)
		sys.modules["__main__"].language.assert_called_with(30609)
	
	def test_login_should_show_refreshing_folder_message_on_login_success(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		language = ["string1", "string2"]
		sys.modules["__main__"].language.side_effect = lambda x: language.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
		sys.modules["xbmc"].executebuiltin = Mock()
		login = YouTubeLogin()
		login._apiLogin = Mock()
		login._apiLogin.return_value = ("",200)
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",200)
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		login._httpLogin.assert_called_with({ "new": "true"})
		login._apiLogin.assert_called_with()
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("string2","",303)
		sys.modules["__main__"].language.assert_called_with(30031)
	
if __name__ == '__main__':
	nose.run()
