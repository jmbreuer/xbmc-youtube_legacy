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
		
	
if __name__ == '__main__':
	nose.run()
