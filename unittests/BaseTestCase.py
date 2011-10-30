import sys
import unittest2, io
from mock import Mock
import MockYouTubeDepends

MockYouTubeDepends.MockYouTubeDepends().mockXBMC()

sys.path.append('../plugin/')
sys.path.append('../xbmc-mocks/')

class BaseTestCase(unittest2.TestCase):
	
	def setUp(self):
		MockYouTubeDepends.MockYouTubeDepends().mockXBMC()
		MockYouTubeDepends.MockYouTubeDepends().mock()
	
	def readTestInput(self, filename, should_eval = True):
		testinput = io.open("resources/" + filename)
		inputdata = testinput.read()
		if should_eval:
			inputdata = eval(inputdata)
		return inputdata
