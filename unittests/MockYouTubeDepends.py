import os, sys, string, inspect
from mock import Mock, patch

# Shield us from XBMC
sys.modules["xbmc"] = __import__("mock")
sys.modules["xbmcgui"] = __import__("mock")
sys.modules["xbmcvfs"] = __import__("mock")
sys.modules["xbmcvfs"].rename = Mock()
sys.modules["xbmcplugin"] = __import__("mock")

# Shield us from the file system
sys.modules["__builtin__"].open = Mock() 

#Emulate more of XBMC
sys.modules[ "__main__" ].settings = Mock()
sys.modules[ "__main__" ].settings.getAddonInfo = Mock()
sys.modules[ "__main__" ].settings.getAddonInfo.return_value = "somepath"

sys.modules[ "__main__" ].language = Mock()
sys.modules[ "__main__" ].common = Mock()
import YouTubeUtils
sys.modules[ "__main__" ].utils = Mock(YouTubeUtils.YouTubeUtils)
sys.modules[ "__main__" ].utils.VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
sys.modules[ "__main__" ].cache = Mock()
sys.modules[ "__main__" ].core = Mock()
sys.modules[ "__main__" ].feeds = Mock()
sys.modules[ "__main__" ].scraper = Mock()
sys.modules[ "__main__" ].login = Mock()
sys.modules[ "__main__" ].plugin = "unittest"
sys.modules[ "__main__" ].dbg = True
sys.modules[ "__main__" ].dbglevel = 10
sys.modules[ "__main__" ].storage = Mock()

sys.modules["xbmc"].translatePath = Mock()
sys.modules["xbmc"].translatePath.return_value = "testing"

class temp():
    def log(self, description, level = 0):
        print "[%s] %s : '%s'" % ("YouTube", inspect.stack()[2][3], description) # inspect.stack() is dependent on testcommonfunctions.py
        #print "[%s] %s : '%s'" % ("YouTube", "No inspect", description)

sys.modules[ "__main__" ].log_override = temp()
sys.modules[ "__main__" ].common.log.side_effect = sys.modules[ "__main__" ].log_override.log
