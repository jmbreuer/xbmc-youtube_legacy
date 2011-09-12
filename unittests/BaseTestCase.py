import sys
import unittest2, io
sys.path.append('../plugin/')

class BaseTestCase(unittest2.TestCase):
		
	def readTestInput(self, filename, should_eval = True):
		testinput = io.open("resources/" + filename)
		inputdata = testinput.read()
		if should_eval:
			inputdata = eval(inputdata)
		return inputdata