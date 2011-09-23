import sys
import unittest2, io
from mock import Mock
import MockYouTubeDepends

MockYouTubeDepends.MockYouTubeDepends().mockXBMC()

sys.path.append('../plugin/')

class BaseTestCase(unittest2.TestCase):		
		
	def setUp(self):
		MockYouTubeDepends.MockYouTubeDepends().mock()
		MockYouTubeDepends.MockYouTubeDepends().mockXBMC()
	
	def readTestInput(self, filename, should_eval = True):
		testinput = io.open("resources/" + filename)
		inputdata = testinput.read()
		if should_eval:
			inputdata = eval(inputdata)
		return inputdata
	
	def raiseError(self, exception):
		raise exception