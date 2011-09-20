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
	
	def test_apiLogin_should_clear_auth_value_in_settings_before_doing_anything_else(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		login._apiLogin()
		
		sys.modules["__main__"].settings.setSetting.assert_called_with("auth","")
	
	def test_apiLogin_should_call_oauth2_login_url_only_one_time_if_url_fails(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		login._apiLogin()

		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
	
	def test_apiLogin_should_call_fetchPage_with_correct_params(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		login._apiLogin()
		
		args = sys.modules["__main__"].core._fetchPage.call_args
		assert(args[0][0].has_key("link"))
		assert(args[0][0].has_key("no-language-cookie"))
		
	def test_apiLogin_should_search_for_state_wrapper_and_new_url(self):
		dom_values = ["","","","some_state_wrapper","some_new_url"]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "", y ="",attrs = {},ret = {}: dom_values.pop()
		login = YouTubeLogin()
		
		login._apiLogin()
		
		args = sys.modules["__main__"].common.parseDOM.call_args
		assert(args[0] == ("","textarea"))
		assert(args[1].has_key("attrs"))
		assert(args[1]["attrs"].has_key("id"))
		assert(args[1]["attrs"]["id"] == "code")
		
	def test_apiLogin_should_follow_redirect_if_statewrapper_present(self):
		dom_values = ["","","",["some_state_wrapper"],["some_new_url"]]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "", y ="",attrs = {},ret = {}: dom_values.pop()
		login = YouTubeLogin()
		
		login._apiLogin()
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
			
	def test_apiLogin_should_call_fetchPage_with_correct_params_on_redirect(self):
		dom_values = ["","","",["some_state_wrapper"],["some_new_url"]]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "", y ="",attrs = {},ret = {}: dom_values.pop()
		login = YouTubeLogin()
		
		login._apiLogin()
		
		args = sys.modules["__main__"].core._fetchPage.call_args
		assert(args[0][0]["link"] == "some_new_url")
		assert(args[0][0]["no-language-cookie"] == "true")
		assert(args[0][0]["url_data"]["submit_access"] == "true" )
		assert(args[0][0]["url_data"]["state_wrapper"] == "some_state_wrapper" )
		
		
	def test_apiLogin_should_request_token_if_code_present(self):
		dom_values = ["","","",["some_code"],"",""]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "", y ="",attrs = {},ret = {}: dom_values.pop()
		login = YouTubeLogin()
		
		login._apiLogin()
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
	
	def test_apiLogin_should_call_fetchPage_with_correct_params_when_fetching_request_token(self):
		dom_values = ["","","",["some_code"],"",""]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "", y ="",attrs = {},ret = {}: dom_values.pop()
		login = YouTubeLogin()
		
		login._apiLogin()
		
		args = sys.modules["__main__"].core._fetchPage.call_args
		assert(args[0][0]["link"] == "https://accounts.google.com/o/oauth2/token")
		assert(args[0][0].has_key("url_data"))
		assert(args[0][0]["url_data"]["code"] == "some_code" )
		assert(args[0][0]["url_data"]["grant_type"] == "authorization_code" )
		
	def test_apiLogin_should_set_oauth_specific_values_on_success(self):
		fetch_values = [{"content":""},{"content":'{"expires_in":"12", "access_token":"my_favorite_access_token", "refresh_token":"my_favorite_refresh_token" }'}]
		sys.modules["__main__"].core._fetchPage.side_effect = lambda x: fetch_values.pop()
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		login._apiLogin()
		
		args = sys.modules["__main__"].settings.setSetting.call_args_list
		#print repr(args)
		assert(args[1][0][0] == "oauth2_expires_at")
		assert(len(args[1][0][1]) > 1)
		assert(args[2][0][0] == "oauth2_access_token")
		assert(args[2][0][1] == "my_favorite_access_token")
		assert(args[3][0][0] == "auth")
		assert(args[3][0][1] == "my_favorite_access_token")
		assert(args[4][0][0] == "oauth2_refresh_token")
		assert(args[4][0][1] == "my_favorite_refresh_token")
		
	def test_apiLogin_should_provide_correct_message_and_success_status_code_on_success(self):
		fetch_values = [{"content":""},{"content":'{"expires_in":"12", "access_token":"my_favorite_access_token", "refresh_token":"my_favorite_refresh_token" }'}]
		sys.modules["__main__"].core._fetchPage.side_effect = lambda x: fetch_values.pop()
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._apiLogin()
		
		sys.modules["__main__"].language.assert_called_with(30030)
		assert(result[1] == 200)
		
	def test_apiLogin_should_provide_correct_message_and_failure_status_code_on_failure(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":""}
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._apiLogin()
		
		sys.modules["__main__"].language.assert_called_with(30609)
		assert(result[1] == 303)	
	
	def test_httpLogin_should_check_if_new_is_in_params_collection_before_resetting_login_info(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"false"})
		
		assert(sys.modules["__main__"].settings.setSetting.call_count == 0)
		assert(sys.modules["__main__"].core._fetchPage.call_count == 0)
		
	def test_httpLogin_should_return_existing_http_login_info_if_new_is_not_in_params(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin()
		
		sys.modules["__main__"].settings.getSetting.assert_called_with("login_info")
		assert(sys.modules["__main__"].core._fetchPage.call_count == 0)
		assert(result[1] == 200)
		assert(result[0] == "smokey")

	def test_httpLogin_should_call_fetchPage_with_proper_fetch_options_on_first_run(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})
		
		args = sys.modules["__main__"].core._fetchPage.call_args
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[0][0] == {"link":"http://www.youtube.com/"})

	def test_httpLogin_should_use_parseDOM_to_check_for_login_button_link(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[0][0] == ("","a"))
		assert(args[0][1] == {'attrs': {'class': 'end'}, 'ret': 'href'})

#	def test_httpLogin_should_call_fetchPage_with_proper_redirect_url_if_login_link_is_found(self):
#		assert(False)
	
	def test_httpLogin_should_use_parseDOM_to_check_for_login_form(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[1][0] == ("","form"))
		assert(args[1][1] == {'attrs': {'id': 'gaia_loginform'}, 'ret': 'action'})

#	def test_httpLogin_should_call_fillLoginInfo_if_login_form_present(self):
#		assert(False)

#	def test_httpLogin_should_call_fetchPage_with_proper_fetch_options_if_fillLoginInfo_succeded(self):
#		assert(False)
	
	def test_httpLogin_should_use_parseDOM_to_check_for_new_url_redirects(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[2][0] == ('', 'meta'))
		assert(args[2][1] == {'attrs': {'http-equiv': 'refresh'}, 'ret': 'content'})


#	def test_httpLogin_should_call_fetchPage_with_proper_redirect_url(self):
#		assert(False)

'''
	def test_httpLogin_should_use_parseDOM_to_chceck_for_2factor_login(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		print repr(args[3])
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[2][0] == ('', 'meta'))
		assert(args[2][1] == {'attrs': {'http-equiv': 'refresh'}, 'ret': 'content'})
		assert(False)

	def test_httpLogin_should_call_fillUserPin_if_2factor_login_needs_smsUserPin(self):
		assert(False)
		
	def test_httpLogin_should_call_fetchPage_with_correct_fetch_options_if_fillUserPin_succeded(self):
		assert(False)

	def test_httpLogin_should_use_parseDOM_to_find_smsToken(self):
		assert(False)
	
	def test_httpLogin_should_call_fetchPage_with_correct_fetch_options_if_smsToken_is_found(self):
		assert(False)
		
	def test_httpLogin_should_look_for_user_name_to_indicate_login_success(self):
		assert(False)
		
	def test_httpLogin_should_call_findErrors_on_login_failure(self):
		assert(False)
		
	def test_httpLogin_should_call_getLoginInfo_on_login_success(self):
		assert(False)
		'''
if __name__ == '__main__':
	nose.run()
