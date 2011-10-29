# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock
import sys

from  YouTubeLogin import YouTubeLogin 

class TestYouTubeLogin(BaseTestCase.BaseTestCase):
	
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
		
		login.login()
		
		calls = sys.modules["__main__"].settings.setSetting.call_args_list
		assert(calls[0] == (("oauth2_access_token",""),{}))
		assert(calls[1] == (("oauth2_refresh_token",""),{}))
		assert(calls[2] == (("oauth2_expires_at",""),{}))
		assert(calls[3] == (("nick",""),{}))
		
	def test_login_should_call_xbmc_execute_builtin(self):
		settings = ["password","","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		login = YouTubeLogin()
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		
		login.login()
		
		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with("Container.Refresh")
	
	def test_login_should_call_oRefreshToken(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = True
		login = YouTubeLogin()
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
	
	def test_login_should_call_httpLogin_if_refresh_token_didnt_work(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
		login = YouTubeLogin()
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		login._httpLogin.assert_called_with({ "new": "true"})
	
	def test_login_should_call_apiLogin_if_refresh_token_didnt_work(self):
		settings = ["password","some_token","true","username","password","username"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
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
		sys.modules["__main__"].core._oRefreshToken.return_value = True
		login = YouTubeLogin()
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",303)
		
		login.login()
		
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		assert(sys.modules["__main__"].utils.showMessage.call_count == 0)
		assert(sys.modules["__main__"].utils.showErrorMessage.call_count == 0)
	
	def test_login_should_show_error_message_on_failure(self):
		settings = ["password","some_token","true","username","password","username"]
		language = ["string1", "string2"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules["__main__"].language.side_effect = lambda x: language.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
		login = YouTubeLogin()
		login._apiLogin = Mock()
		login._apiLogin.return_value = ("",303)
		login._httpLogin = Mock()
		login._httpLogin.return_value = ("",200)
		
		login.login()
		
		login._httpLogin.assert_called_with({ "new": "true"})
		login._apiLogin.assert_called_with()
		sys.modules["__main__"].core._oRefreshToken.assert_called_with()
		sys.modules["__main__"].utils.showErrorMessage.assert_called_with("string2","",303)
		sys.modules["__main__"].language.assert_called_with(30609)
	
	def test_login_should_show_refreshing_folder_message_on_login_success(self):
		settings = ["password","some_token","true","username","password","username"]
		language = ["string1", "string2"]
		sys.modules["__main__"].settings.getSetting.side_effect = lambda x: settings.pop()
		sys.modules["__main__"].language.side_effect = lambda x: language.pop()
		sys.modules["__main__"].core._oRefreshToken.return_value = False
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
		
		sys.modules["__main__"].settings.setSetting.assert_any_call("oauth2_access_token","")
	
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
		print repr(args)
		assert(args[3][0][0] == "oauth2_expires_at")
		assert(len(args[3][0][1]) > 1)
		assert(args[4][0][0] == "oauth2_access_token")
		assert(args[4][0][1] == "my_favorite_access_token")
		assert(args[5][0][0] == "oauth2_refresh_token")
		assert(args[5][0][1] == "my_favorite_refresh_token")
		
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

	def test_httpLogin_should_call_fetchPage_with_proper_redirect_url_if_login_link_is_found(self):
		dom_values = ["","","","","","","","","",["someURL"]]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})
		
		sys.modules["__main__"].core._fetchPage.assert_called_with({"link":"someURL"})
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
	
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

	def test_httpLogin_should_call_fillLoginInfo_if_login_form_present(self):
		dom_values = ["","","","","","","","",["someURL"],""]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"somePage","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()
		login = YouTubeLogin()
		login._fillLoginInfo = Mock()
		login._fillLoginInfo.return_value = ("",{})
		
		result = login._httpLogin({"new":"true"})
		
		login._fillLoginInfo.assert_called_with("somePage")

	def test_httpLogin_should_call_fetchPage_with_proper_fetch_options_if_fillLoginInfo_succeded(self):
		dom_values = ["","","","","","","","",["someURL"],""]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"somePage","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()
		login = YouTubeLogin()
		login._fillLoginInfo = Mock()
		login._fillLoginInfo.return_value = ("some_galx_value",{"some_key":"some_value"})
		
		result = login._httpLogin({"new":"true"})
		
		login._fillLoginInfo.assert_called_with("somePage")
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
		sys.modules["__main__"].core._fetchPage.assert_called_with({'link': 'someURL', 'no-language-cookie': 'true', 'url_data': {'some_key': 'some_value'}, "hidden": "true"})
	
	def test_httpLogin_should_use_parseDOM_to_check_for_new_url_redirects(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		print repr(args[2])
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[2][0] == ('', 'meta'))
		assert(args[2][1] == {'attrs': {'http-equiv': 'refresh'}, 'ret': 'content'})

	def test_httpLogin_should_call_fetchPage_with_proper_redirect_url(self):
		dom_values = ["","","","","","","",["&#39;someURL&#39;"],"",""]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"somePage","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()
		login = YouTubeLogin()
		login._fillLoginInfo = Mock()
		login._fillLoginInfo.return_value = ("some_galx_value",{"some_key":"some_value"})
		
		result = login._httpLogin({"new":"true"})
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
		sys.modules["__main__"].core._fetchPage.assert_called_with({'link': 'someURL', 'no-language-cookie': 'true'})
		
	def test_httpLogin_should_search_fetchPage_result_to_check_for_2factor_login(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		page_values = [ {"content":"","status":200}, {"content":dummy_content,"status":200}]
		sys.modules["__main__"].core._fetchPage.side_effect = lambda x: page_values.pop() 
		sys.modules["__main__"].core._fetchPage.return_value = {"content":dummy_content,"status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})
		
		args = dummy_content.find.call_args_list

		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		print repr(args)
		assert(args[1][0] == ("smsUserPin",))

	def test_httpLogin_should_call_fillUserPin_if_2factor_login_needs_smsUserPin(self):
		page_values = [ {"content":"captcha","status":200}, { "new_url": "http://www.mock.com/", "content":"something,smsUserPin,somethingElse","status":200}]
		sys.modules["__main__"].core._fetchPage.side_effect = lambda x: page_values.pop() 
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		dom_values = [["Login"], [], [], []]
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()

		login = YouTubeLogin()
		login._fillUserPin = Mock()
		
		result = login._httpLogin({"new":"true"})
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
		login._fillUserPin.assert_called_with("something,smsUserPin,somethingElse")
		
	def test_httpLogin_should_call_fetchPage_with_correct_fetch_options_if_fillUserPin_succeded(self):
		page_values = [ {"content":"captcha","status":200}, { "new_url": "http://www.mock.com", "content":"something,smsUserPin,somethingElse","status":200}]
		sys.modules["__main__"].core._fetchPage.side_effect = lambda x: page_values.pop() 
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		dom_values = [["Login"], [], [], []]
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()
		login = YouTubeLogin()
		login._fillUserPin = Mock()
		login._fillUserPin.return_value = "some_url_data"
		
		result = login._httpLogin({"new":"true"})
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 2)
		sys.modules["__main__"].core._fetchPage.assert_called_with({'link': 'http://www.mock.com/Login', 'no-language-cookie': 'true', 'url_data': 'some_url_data'})

		
	def test_httpLogin_should_use_parseDOM_to_find_smsToken(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[3][0] == ('', 'input'))
		assert(args[3][1] == {'attrs': {'name': 'smsToken'}, 'ret': 'value'})

	def test_httpLogin_should_use_parseDOM_to_find_cont_value_for_smsToken(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		assert(args[4][0] == ('', 'input'))
		assert(args[4][1] == {'attrs': {'name': 'continue'}, 'ret': 'value'})

	def test_httpLogin_should_call_fetchPage_with_correct_fetch_options_if_smsToken_is_found(self):
		dom_values = [[], [],[],[],[],["http://www.mock.com"],["some cont"],["some smsToken"],[],[],[],["galx"],[]]
		login_values = [("",""),("some_galx", "some_url_data")]
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.side_effect = lambda x = "",y = "",attrs = {},ret = "": dom_values.pop()
		login = YouTubeLogin()
		login._fillLoginInfo = Mock()
		login._fillLoginInfo.side_effect = lambda x: login_values.pop()
		
		result = login._httpLogin({"new":"true"})

		assert(sys.modules["__main__"].core._fetchPage.call_count == 3)
		sys.modules["__main__"].core._fetchPage.assert_called_with({'link': 'http://www.mock.com', 'no-language-cookie': 'true', 'url_data': {'service': 'youtube', 'continue': 'some cont', 'GALX': 'some_galx', 'PersistentCookie': 'yes', 'smsToken': 'some smsToken'}})
				
	def test_httpLogin_should_look_for_user_name_to_indicate_login_success(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		page_values = [ {"content":"","status":200}, {"content":dummy_content,"status":200}]
		sys.modules["__main__"].core._fetchPage.side_effect = lambda x: page_values.pop() 
		sys.modules["__main__"].core._fetchPage.return_value = {"content":dummy_content,"status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._httpLogin({"new":"true"})
		
		assert(sys.modules["__main__"].core._fetchPage.call_count == 1)
		args = dummy_content.find.call_args_list
		#dummy_content.find.assert_called_with("USERNAME', ")
		print repr(args[2][0][0])
		assert(args[2][0][0] == "USERNAME', ")

	def test_httpLogin_should_call_findErrors_on_login_failure(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		login._getLoginInfo = Mock()
		
		result = login._httpLogin({"new":"true"})

		sys.modules["__main__"].core._findErrors.assert_called_with({'content': '', 'status': 200})
		
	def test_httpLogin_should_call_getLoginInfo_on_login_success(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"something USERNAME', ","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		login._getLoginInfo = Mock()
		login._getLoginInfo.return_value = 200
		
		result = login._httpLogin({"new":"true"})

		login._getLoginInfo.assert_called_with( "something USERNAME', ")
		assert(result == ("smokey",200))
		sys.modules["__main__"].settings.getSetting.assert_called_with("login_info")

	def test_httpLogin_should_fail_with_captcha(self):
		sys.modules["__main__"].core._fetchPage.return_value = {"content":"captcha","status":200}
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		result = login._httpLogin({"new":"true"})
		print repr(result)
		assert(result == ("",500))

	def test_fillLoginInfo_should_call_parseDOM_to_find_rmShow(self):
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillLoginInfo("new")

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(args[0][0] == ("new","input"))
		assert(args[0][1] == {'attrs': {'name': 'rmShown'}, 'ret': 'value'})

	def test_fillLoginInfo_should_call_parseDOM_twice_to_find_uilel(self):
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillLoginInfo("new")

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(args[2][0] == ("new","input"))
		assert(args[2][1] == {'attrs': {'name': 'uilel'}, 'ret': 'value'})
		assert(args[3][0] == ("new","input"))
		assert(args[3][1] == {'attrs': {'id': 'uilel'}, 'ret': 'value'})

	def test_fillLoginInfo_should_call_parseDOM_twice_to_find_dsh(self):
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillLoginInfo("new")

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(args[4][0] == ("new","input"))
		assert(args[4][1] == {'attrs': {'name': 'dsh'}, 'ret': 'value'})
		assert(args[5][0] == ("new","input"))
		assert(args[5][1] == {'attrs': {'id': 'dsh'}, 'ret': 'value'})

	def test_fillLoginInfo_should_call_parseDOM_to_get_galx(self):
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillLoginInfo("new")

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(args[6][0] == ("new","input"))
		assert(args[6][1] == {'attrs': {'name': 'GALX'}, 'ret': 'value'})

	def test_fillLoginInfo_should_get_username_and_passwords_from_settings(self):
		sys.modules["__main__"].settings.getSetting.return_value = "smokey" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillLoginInfo("new")

		sys.modules["__main__"].settings.getSetting.assert_any_call("username")
		sys.modules["__main__"].settings.getSetting.assert_any_call("user_password")


	def test_fillLoginInfo_should_ask_user_for_password_if_not_set(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		sys.modules["__main__"].language.return_value = "someTitle"
		sys.modules["__main__"].utils.getUserInput.return_value = "somePword"
		login = YouTubeLogin()
		
		result = login._fillLoginInfo("new")

		sys.modules["__main__"].utils.getUserInput.assert_any_call('someTitle', hidden=True)

	def test_fillLoginInfo_should_return_login_info_if_all_values_are_found(self):
		sys.modules["__main__"].settings.getSetting.return_value = "value1" 
		sys.modules["__main__"].common.parseDOM.return_value = ["value2"]
		sys.modules["__main__"].language.return_value = "someTitle"
		sys.modules["__main__"].utils.getUserInput.return_value = "somePword"
		login = YouTubeLogin()
		
		(galx, url_data) = login._fillLoginInfo("new")
		
		assert(galx == "value2")
		assert(url_data["uilel"] == "value2")
		assert(url_data["dsh"] == "value2")
		assert(url_data["rmShown"] == "value2")
		assert(url_data["GALX"] == "value2")
		assert(url_data["Passwd"] == "value1")
		assert(url_data["Email"] == "value1")

	def test_fillLoginInfo_should_not_return_login_info_if_values_are_missing(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		sys.modules["__main__"].language.return_value = "someTitle"
		sys.modules["__main__"].utils.getUserInput.return_value = "somePword"
		login = YouTubeLogin()
		
		(galx, url_data) = login._fillLoginInfo("new")

		assert(galx == "")		
		assert(url_data == {})
		
	def test_fillUserPin_should_call_parseDOM_for_smsToken(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].utils.getUserInput.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillUserPin("new")

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(args[0][0] == ("new","input"))
		assert(args[0][1] == {'attrs': {'name': 'smsToken'}, 'ret': 'value'})
		
	def test_fillUserPin_should_call_parseDOM_for_email(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].utils.getUserInput.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillUserPin("new")

		args = sys.modules["__main__"].common.parseDOM.call_args_list
		assert(args[1][0] == ("new","input"))
		assert(args[1][1] == {'attrs': {'name': 'email'}, 'ret': 'value'})
		
	def test_fillUserPin_should_ask_user_for_user_pin(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		sys.modules["__main__"].language.return_value = "someTitle"
		sys.modules["__main__"].utils.getUserInput.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillUserPin("new")
		
		sys.modules["__main__"].utils.getUserInput.assert_called_with('someTitle')
		
	def test_fillUserPin_should_return_url_data_structure_if_all_values_are_found(self):
		sys.modules["__main__"].settings.getSetting.return_value = "value1" 
		sys.modules["__main__"].common.parseDOM.return_value = ["value2"]
		sys.modules["__main__"].language.return_value = "someTitle"
		sys.modules["__main__"].utils.getUserInput.return_value = "value3"
		login = YouTubeLogin()
		
		result = login._fillUserPin("new")
		
		assert(result["smsUserPin"] == "value3")
		assert(result["smsToken"] == "value2")
		assert(result["email"] == "value2")
		
	def test_fillUserPin_should_not_return_url_data_structure_if_values_are_missing(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		sys.modules["__main__"].language.return_value = ""
		sys.modules["__main__"].utils.getUserInput.return_value = ""
		login = YouTubeLogin()
		
		result = login._fillUserPin("new")

		assert(result == {})
		
	def test_getLoginInfo_should_search_input_for_username(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		sys.modules[ "__main__" ].cookiejar = Mock()
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._getLoginInfo(dummy_content)
		
		dummy_content.find.assert_called_with("USERNAME', ")
		
	def test_getLoginInfo_should_call_setSetting_to_save_nick(self):
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._getLoginInfo("   USERNAME', 'some_value" + '")')
		
		sys.modules["__main__"].settings.setSetting.assert_any_call("nick","some_value")
		
	def test_getLoginInfo_should_search_cookie_jar_for_login_info(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		sys.modules[ "__main__" ].cookiejar = Mock()
		sys.modules[ "__main__" ].cookiejar = "   name='LOGIN_INFO', value='honk honk', port=None  "
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._getLoginInfo("   USERNAME', 'some_value" + '")')
		
		sys.modules["__main__"].settings.setSetting.assert_called_with("login_info","honk honk")
		
	def test_getLoginInfo_should_call_setSetting_to_save_login_info(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		sys.modules[ "__main__" ].cookiejar = Mock()
		sys.modules[ "__main__" ].cookiejar = "   name='LOGIN_INFO', value='honk honk', port=None  "
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._getLoginInfo("")
		
		assert(sys.modules["__main__"].settings.setSetting.call_count == 1)
		sys.modules["__main__"].settings.setSetting.assert_called_with("login_info","honk honk")
		
	def test_getLoginInfo_should_return_error_status_on_failure(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		sys.modules[ "__main__" ].cookiejar = Mock()
		sys.modules[ "__main__" ].cookiejar = ""
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		
		result = login._getLoginInfo("")
		
		assert(result == 303)
		
	def test_getLoginInfo_should_return_proper_status_on_success(self):
		dummy_content = Mock()
		dummy_content.find.return_value = -1
		sys.modules[ "__main__" ].cookiejar = Mock()
		sys.modules[ "__main__" ].cookiejar = "   name='LOGIN_INFO', value='honk honk', port=None  "		
		sys.modules["__main__"].settings.getSetting.return_value = "" 
		sys.modules["__main__"].common.parseDOM.return_value = ""
		login = YouTubeLogin()
		result = login._getLoginInfo("")
		
		assert(result == 200)
				
if __name__ == '__main__':
	nose.runmodule()
