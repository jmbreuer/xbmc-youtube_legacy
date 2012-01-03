import BaseTestCase
import nose
import sys
from mock import Mock


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

        self.navigation.executeAction({"action": "settings"})

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

        self.navigation.executeAction({"action": "settings"})

        nick = sys.modules["__main__"].settings.getSetting("nick")
        oauth2_access_token = sys.modules["__main__"].settings.getSetting("oauth2_access_token")
        print "nick: " + nick + " - " + str(len(nick))
        print "username: " + sys.modules["__main__"].settings.getSetting("username")
        print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth2_access_token: " + oauth2_access_token + " - " + str(len(oauth2_access_token))
        assert(len(nick.strip()) > 0 )
        assert(len(oauth2_access_token) > 40)

    def test_plugin_should_perform_basic_2factor_login_correctly(self):
        import time
        import pyotp
        totp = pyotp.TOTP("fbfkkk27ffmaihzg")
        self.lastpin = False

        def generatePin():
            userpin = totp.at(time.time())
            print "GENERATED PIN : " + str(userpin)
            if userpin == self.lastpin or len(str(userpin)) < 6:
                time.sleep(15)
                return generatePin()
            return userpin

        sys.modules["__main__"].settings.load_strings("./resources/2factor-login-settings.xml")

        sys.modules["__main__"].xbmcgui.Dialog().numeric.return_value = str(generatePin())

        assert(sys.modules["__main__"].settings.getSetting("nick") == "")
        assert(sys.modules["__main__"].settings.getSetting("auth") == "")
        assert(sys.modules["__main__"].settings.getSetting("oauth2_access_token") == "")

        print "nick: " + sys.modules["__main__"].settings.getSetting("nick")
        print "username: " + sys.modules["__main__"].settings.getSetting("username")
        print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth2_access_token: " + sys.modules["__main__"].settings.getSetting("oauth2_access_token")

        self.navigation.executeAction({"action": "settings"})

        nick = sys.modules["__main__"].settings.getSetting("nick")
        oauth2_access_token = sys.modules["__main__"].settings.getSetting("oauth2_access_token")
        print "nick: " + nick + " - " + str(len(nick))
        print "username: " + sys.modules["__main__"].settings.getSetting("username")
        print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth2_access_token: " + oauth2_access_token + " - " + str(len(oauth2_access_token))
        assert(len(nick.strip()) > 1 )
        assert(len(oauth2_access_token) > 40)

    def test_plugin_should_perform_googleplus_login_correctly(self):
        sys.modules["__main__"].settings.load_strings("./resources/basic-login-settings-plus.xml")

        assert(sys.modules["__main__"].settings.getSetting("nick") == "")
        assert(sys.modules["__main__"].settings.getSetting("auth") == "")
        assert(sys.modules["__main__"].settings.getSetting("oauth2_access_token") == "")

        print "nick: " + sys.modules["__main__"].settings.getSetting("nick")
        print "username: " + sys.modules["__main__"].settings.getSetting("username")
        print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth2_access_token: " + sys.modules["__main__"].settings.getSetting("oauth2_access_token")

        self.navigation.executeAction({"action": "settings"})

        nick = sys.modules["__main__"].settings.getSetting("nick")
        oauth2_access_token = sys.modules["__main__"].settings.getSetting("oauth2_access_token")
        print "nick: " + nick + " - " + str(len(nick))
        print "username: " + sys.modules["__main__"].settings.getSetting("username")
        print "pass: " + sys.modules["__main__"].settings.getSetting("user_password")
        print "oauth2_access_token: " + oauth2_access_token + " - " + str(len(oauth2_access_token))
        assert(len(nick.strip()) > 0 )
        assert(len(oauth2_access_token) > 40)

if __name__ == "__main__":
    nose.runmodule()
