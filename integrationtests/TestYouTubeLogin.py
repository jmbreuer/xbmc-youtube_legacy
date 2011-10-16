import BaseTestCase
import unittest2
import nose, sys
from mock import Mock, patch


class TestYouTubeLogin(BaseTestCase.BaseTestCase):
	
	def test_login_should_perform_basic_login_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")
		
		self.navigation.executeAction({"action":"settings"})
		
		print "nick: " + sys.modules["__main__"].settings.getSetting("nick")
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		assert(False)
	
if __name__ == "__main__":
	nose.runmodule()