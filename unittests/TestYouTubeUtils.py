# -*- coding: utf-8 -*-
import nose
import BaseTestCase
from mock import Mock, patch
import sys
from  YouTubeUtils import YouTubeUtils 

class TestYouTubeUtils(BaseTestCase.BaseTestCase):
	
	def test_getUserInput_should_xbmc_keyboard_to_recieve_text_input(self):
		utils = YouTubeUtils()
		
		utils.getUserInput()
		
		sys.modules["__main__"].xbmc.Keyboard.assert_called_with("","Input")
		
	def test_getUserInput_should_set_title_and_default_text_if_set(self):
		utils = YouTubeUtils()
		sys.modules["__main__"].xbmc.Keyboard().getText.return_value = "user_result"
		
		result = utils.getUserInput("SomeTitle","SomeDefault")
		
		sys.modules["__main__"].xbmc.Keyboard.assert_called_with("SomeDefault","SomeTitle")
		sys.modules["__main__"].xbmc.Keyboard().setHiddenInput.assert_called_with(False)
		sys.modules["__main__"].xbmc.Keyboard().doModal.assert_called_with()
		sys.modules["__main__"].xbmc.Keyboard().isConfirmed.assert_called_with()
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

	
	def test_makeAscii_should_do_nothing_on_python_2_6(self):
		input = "æøåa"
		utils = YouTubeUtils()
		
		result = utils.makeAscii(input)

		assert(result==input)		
	
	def test_makeAscii_should_convert_to_ascii(self):
		hexversion = sys.hexversion 
		sys.hexversion = 0x02040000
		utils = YouTubeUtils()
		input = "æøåa"
		print "input " + repr(input)
				
		result = utils.makeAscii(input)
		print "result " + repr(result)
		
		sys.hexversion = hexversion
		assert(result=="a")
		
	def test_showMessage_should_call_xbmc_execute_builtin_correctly(self):
		sys.modules["__main__"].settings.getSetting.return_value = "3"
		utils = YouTubeUtils()
		
		utils.showMessage("someHeading","someMessage")

		sys.modules["__main__"].xbmc.executebuiltin.assert_called_with('XBMC.Notification("someHeading", "someMessage", 4000)')
		
	def test_getThumbnail_should_call_xbmc_skinHasImage(self):
		sys.modules["__main__"].xbmc.skinHasImage = Mock()
		utils = YouTubeUtils()
		
		result = utils.getThumbnail("someTeading")

		sys.modules["__main__"].xbmc.skinHasImage.assert_called_with('YouTube - Unittest/someTeading.png')
		
	def test_getThumbnail_should_user_default_folder_image_if_no_title_is_given(self):
		sys.modules["__main__"].xbmc.skinHasImage.return_value = False
		utils = YouTubeUtils()
		
		result = utils.getThumbnail("")
		
		sys.modules["__main__"].xbmc.skinHasImage.assert_called_with('YouTube - Unittest/DefaultFolder.png')
		assert(result == "DefaultFolder.png")
		
	
	def test_getThumbnail_should_user_thumbnail_path_to_resolve_file_paths(self):
		sys.modules["__main__"].settings.getAddonInfo.return_value = "testingPath/"
		sys.modules["__main__"].xbmc.skinHasImage.return_value = False		
		patcher = patch("os.path")
		patcher.start()
		import os
		utils = YouTubeUtils()
		
		result = utils.getThumbnail("")
		call = os.path.join.call_args_list[0]
		patcher.stop()
		
		assert(call == (('testingPath/', 'thumbnails'), {}))
		
	def test_showErrorMessage_should_call_showMessage(self):
		sys.modules["__main__"].language.return_value = "ERROR"
		utils = YouTubeUtils()
		utils.showMessage = Mock()	
		
		result = utils.showErrorMessage("someTitle","someResult")
		
		utils.showMessage.assert_called_with("someTitle","ERROR")
	
	def test_buildItemUrl_should_ignore_items_in_blacklist(self):
		input = {"path":"FAIL","thumbnail":"FAIL", "Overlay":"FAIL", "icon":"FAIL", "next":"FAIL", "content":"FAIL" , "editid":"FAIL", "summary":"FAIL", "published":"FAIL","count":"FAIL","Rating":"FAIL","Plot":"FAIL","Title":"FAIL","new_results_function":"FAIL","some_other_param":"some_value"}
		utils = YouTubeUtils()
		
		result = utils.buildItemUrl(input)
		
		assert(result.find("FAIL") < 0)
		
	def test_buildItemUrl_should_build_url_from_params_collection(self):
		input = {"some_other_param":"some_value", "some_param":"some_other_value"}
		utils = YouTubeUtils()
		
		result = utils.buildItemUrl(input)
		
		assert(result == "some_param=some_other_value&some_other_param=some_value&")

	def test_buildItemUrl_should_append_to_existing_url(self):
		input = {"some_other_param":"some_value", "some_param":"some_other_value"}
		utils = YouTubeUtils()
		
		result = utils.buildItemUrl(input, "myfirst_url?")
		
		assert(result == "myfirst_url?some_param=some_other_value&some_other_param=some_value&")
		
	def test_addNextFolder_should_ignore_item_Title_thumbnail_page_and_new_results_funtion(self):
		sys.modules["__main__"].language.return_value = "Next"
		input = {"some_other_param":"some_value", "some_param":"some_other_value","page":"1","Title":"My annoying Title", "thumbnail":"someThumbnail","new_results_function":"functionPointer"}
		utils = YouTubeUtils()
		result = []
		
		utils.addNextFolder(result, input)
		
		assert(result[0]["Title"] == "Next")
		assert(result[0]["some_other_param"] == "some_value")
		assert(result[0]["some_param"] == "some_other_value")
		assert(result[0]["page"] == "2")
		assert(result[0]["thumbnail"] == "next")
		assert(result[0]["next"] == "true")
		
	def test_addNextFolder_should_increment_current_page(self):
		sys.modules["__main__"].language.return_value = "Next"
		input = {"some_other_param":"some_value", "some_param":"some_other_value","page":"45"}
		utils = YouTubeUtils()
		result = []
		
		utils.addNextFolder(result, input)
		
		assert(result[0]["page"] == "46")
		
if __name__ == '__main__':
	nose.runmodule()
