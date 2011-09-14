import nose
import BaseTestCase
from mock import Mock, patch
import sys, io
import MockYouTubeDepends
from  YouTubeUtils import YouTubeUtils 

class TestYouTubeUtils(BaseTestCase.BaseTestCase):
	
	def test_getUserInput_should_xbmc_keyboard_to_recieve_text_input(self):
		utils = YouTubeUtils()
		sys.modules["xbmc"].Keyboard = Mock()
		
		utils.getUserInput()
		
		sys.modules["xbmc"].Keyboard.assert_called_with("","Input")
		
	def test_getUserInput_should_set_title_and_default_text_if_set(self):
		utils = YouTubeUtils()
		sys.modules["xbmc"].Keyboard = Mock()
		sys.modules["xbmc"].Keyboard().getText.return_value = "user_result"
		
		result = utils.getUserInput("SomeTitle","SomeDefault")
		
		sys.modules["xbmc"].Keyboard.assert_called_with("SomeDefault","SomeTitle")
		sys.modules["xbmc"].Keyboard().setHiddenInput.assert_called_with(False)
		sys.modules["xbmc"].Keyboard().doModal.assert_called_with()
		sys.modules["xbmc"].Keyboard().isConfirmed.assert_called_with()
		assert(result == "user_result")
		
	def test_getParameters_should_parse_param_string(self):
		params_string = "/Some/parth?key1=value1&key2=value2&"
		utils = YouTubeUtils()
		
		result = utils.getParameters(params_string)
		
		assert(result["key1"] == "value1")
		assert(result["key2"] == "value2")
		
	def test_getParameters_should_handle_params_with_missing_value(self):
		params_string = "/Some/parth?key1=value1&key2=&"
		utils = YouTubeUtils()
		
		result = utils.getParameters(params_string)
		
		assert(result["key1"] == "value1")
		assert(result["key2"] == "")
		
		
	def test_getParameters_should_handle_missing_question_mark(self):
		params_string = "key1=value1&key2=value2&"
		utils = YouTubeUtils()
		
		result = utils.getParameters(params_string)
		
		assert(result["key1"] == "value1")
		assert(result["key2"] == "value2")
	
	def test_replaceHtmlCodes_should_handle_ampersand(self):
		input = "&amp;"
		utils = YouTubeUtils()
		
		result = utils.replaceHtmlCodes(input)
		
		assert(result=="&")
		
	def test_replaceHtmlCodes_should_handle_quotationmark(self):
		input = "&quot;"
		utils = YouTubeUtils()
		
		result = utils.replaceHtmlCodes(input)
		
		assert(result=='"')

	def test_replaceHtmlCodes_should_handle_hellip(self):
		input = "&hellip;"
		utils = YouTubeUtils()
		
		result = utils.replaceHtmlCodes(input)
		
		assert(result=="...")

	def test_replaceHtmlCodes_should_handle_greater_than_and_less_than(self):
		input = "&gt;&lt;"
		utils = YouTubeUtils()
		
		result = utils.replaceHtmlCodes(input)
		
		assert(result=="><")

	def test_replaceHtmlCodes_should_handle_hyphen(self):
		input = "&#39;"
		utils = YouTubeUtils()
		
		result = utils.replaceHtmlCodes(input)
		
		assert(result=="'")

		
if __name__ == '__main__':
	nose.run()
