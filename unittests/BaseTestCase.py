import sys
import unittest2, io
from mock import Mock
import MockYouTubeDepends

# Shield us from XBMC
sys.modules["xbmc"] = __import__("mock")
sys.modules["xbmc"].getSkinDir = Mock()
sys.modules["xbmc"].getSkinDir.return_value = "testSkinPath"
sys.modules["xbmcgui"] = __import__("mock")
sys.modules["xbmcgui"].WindowXMLDialog = Mock()
sys.modules["xbmcgui"].WindowXMLDialog.return_value = "testWindowXML"
sys.modules["xbmcvfs"] = __import__("mock")
sys.modules["xbmcvfs"].rename = Mock()
sys.modules["xbmcplugin"] = __import__("mock")
sys.modules["xbmc"].translatePath = Mock()
sys.modules["xbmc"].translatePath.return_value = "testing"

sys.path.append('../plugin/')

class BaseTestCase(unittest2.TestCase):		
		
	def setUp(self):
		MockYouTubeDepends.MockYouTubeDepends().mock()
	
	def readTestInput(self, filename, should_eval = True):
		testinput = io.open("resources/" + filename)
		inputdata = testinput.read()
		if should_eval:
			inputdata = eval(inputdata)
		return inputdata