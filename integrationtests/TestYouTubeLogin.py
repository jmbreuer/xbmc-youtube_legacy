import BaseTestCase
import unittest2
import nose, sys, os
from mock import Mock, patch

class TestYouTubeLogin(BaseTestCase.BaseTestCase):
	def test_plugin_should_perform_basic_login_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings.xml")

		assert(sys.modules["__main__"].settings.getSetting("nick") == "")
		assert(sys.modules["__main__"].settings.getSetting("auth") == "")
		assert(sys.modules["__main__"].settings.getSetting("oauth2_access_token") == "")

		print "nick: " + sys.modules["__main__"].settings.getSetting("nick")
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		print "oauth2_access_token: " + sys.modules["__main__"].settings.getSetting("oauth2_access_token")

		self.navigation.executeAction({"action":"settings"})
		
		nick = sys.modules["__main__"].settings.getSetting("nick")
		oauth2_access_token = sys.modules["__main__"].settings.getSetting("oauth2_access_token")
		print "nick: " + nick + " - " + str(len(nick))
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		print "oauth2_access_token: " + oauth2_access_token + " - " + str(len(oauth2_access_token))
		assert(len(nick.strip()) > 0 )
		assert(len(oauth2_access_token) > 40)

	def test_plugin_should_perform_unlinked_login_correctly(self):
		sys.modules["__main__"].settings.load_strings("./resources/unlinked-login-settings.xml")

		assert(sys.modules["__main__"].settings.getSetting("nick") == "")
		assert(sys.modules["__main__"].settings.getSetting("auth") == "")
		assert(sys.modules["__main__"].settings.getSetting("oauth2_access_token") == "")

		print "nick: " + sys.modules["__main__"].settings.getSetting("nick")
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		print "oauth2_access_token: " + sys.modules["__main__"].settings.getSetting("oauth2_access_token")

		self.navigation.executeAction({"action":"settings"})
		
		nick = sys.modules["__main__"].settings.getSetting("nick")
		oauth2_access_token = sys.modules["__main__"].settings.getSetting("oauth2_access_token")
		print "nick: " + nick + " - " + str(len(nick))
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		print "oauth2_access_token: " + oauth2_access_token + " - " + str(len(oauth2_access_token))
		assert(len(nick.strip()) > 0 )
		assert(len(oauth2_access_token) > 40)

	def test_plugin_should_perform_basic_2factor_login_correctly(self):
		import pyotp, time
		totp = pyotp.TOTP("fbfkkk27ffmaihzg")
		userpin1 = totp.at(time.time())
		userpin2 = totp.at(time.time() + 60)
		userpin3 = totp.at(time.time() + 120)
		print "OTP1: " + str(userpin1)
		print "OTP2: " + str(userpin2)
		print "OTP3: " + str(userpin3)
		sys.modules["__main__"].settings.load_strings("./resources/2factor-login-settings.xml")
		sys.modules["__main__"].xbmc.Keyboard().getText.side_effect = [ [str(userpin1)], [str(userpin2)], [str(userpin3)] ]

		assert(sys.modules["__main__"].settings.getSetting("nick") == "")
		assert(sys.modules["__main__"].settings.getSetting("auth") == "")
		assert(sys.modules["__main__"].settings.getSetting("oauth2_access_token") == "")

		print "nick: " + sys.modules["__main__"].settings.getSetting("nick")
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		print "oauth2_access_token: " + sys.modules["__main__"].settings.getSetting("oauth2_access_token")

		self.navigation.executeAction({"action":"settings"})
		
		nick = sys.modules["__main__"].settings.getSetting("nick")
		oauth2_access_token = sys.modules["__main__"].settings.getSetting("oauth2_access_token")
		print "nick: " + nick + " - " + str(len(nick))
		print "username: " + sys.modules["__main__"].settings.getSetting("username")
		print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
		print "oauth2_access_token: " + oauth2_access_token + " - " + str(len(oauth2_access_token))
		assert(len(nick.strip()) > 1 )
		assert(len(oauth2_access_token) > 40)

	
if __name__ == "__main__":
	nose.runmodule()
