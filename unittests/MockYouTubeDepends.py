import sys
from mock import Mock, patch

sys.path.append('../plugin/')

sys.modules["xbmc"] = __import__("mock")
sys.modules["xbmcgui"] = __import__("mock")
sys.modules["xbmcvfs"] = __import__("mock")
sys.modules["xbmcplugin"] = __import__("mock")

sys.modules[ "__main__" ].__settings__ = Mock()
sys.modules[ "__main__" ].__language__ = Mock()
sys.modules[ "__main__" ].__login__ = Mock()
sys.modules[ "__main__" ].__plugin__ = "unittest"
sys.modules[ "__main__" ].__dbg__ = False
sys.modules[ "__main__" ].__storage__ = Mock()

sys.modules[ "__main__" ].__settings__.getAddonInfo = Mock()
sys.modules[ "__main__" ].__settings__.getAddonInfo.return_value = "somepath"
sys.modules["xbmc"].translatePath = Mock()
sys.modules["xbmc"].translatePath.return_value = "testing"