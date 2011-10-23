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
		import pyotp
		totp = pyotp.TOTP("fbfkkk27ffmaihzg")
		userpin = totp.now()
		print "OTP: " + str(userpin)
		sys.modules["__main__"].settings.load_strings("./resources/2factor-login-settings.xml")
		sys.modules["__main__"].xbmc.Keyboard().getText.return_value = [str(userpin)]

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
