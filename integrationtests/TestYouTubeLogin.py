import BaseTestCase
import nose
import sys
import time
from mock import Mock


class TestYouTubeLogin(BaseTestCase.BaseTestCase):
    totp = ""
    
    def ttest_plugin_should_perform_basic_login_correctly(self):
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

    def ttest_plugin_should_perform_unlinked_login_correctly(self):
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
        import pyotp
        self.totp = pyotp.TOTP("fbfkkk27ffmaihzg")
        self.lastpin = False

        sys.modules["__main__"].settings.load_strings("./resources/2factor-login-settings.xml")
        tmp = sys.modules["__main__"].xbmcgui.Dialog()
        tmp.numeric.side_effect = self.generatePin
        #self.intializePlugin()
        #tmp = sys.modules["__main__"].common.getUserInputNumbers("testing")

        #print repr(tmp)
        #assert(False)
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

    def ttest_plugin_should_perform_googleplus_login_correctly(self):
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
    
    def generatePin(self, *args, **kwargs):
        userpin = self.totp.at(time.time())
        if userpin == self.lastpin or len(str(userpin)) < 6:
            time.sleep(15)
            return self.generatePin(args, kwargs)
        print "GENERATED PIN : " + str(userpin)
        return userpin
        
if __name__ == "__main__":
    nose.runmodule()
