import sys
import time
import inspect


class MockYouTubeDepends:
    common = ""

    def mock(self):
        from mock import Mock
        sys.path.append("../plugin/")

        #Setup default test various values
        sys.modules["__main__"].plugin = "YouTube - Unittest"
        sys.modules["__main__"].dbg = True
        try:
            plat = platform.uname()
        except:
            plat = ('', '', '', '', '', '')

        if plat[0] == "FreeBSD":
            sys.modules["__main__"].dbglevel = 5
        else:
            sys.modules["__main__"].dbglevel = 3
        sys.modules["__main__"].login = ""
        sys.modules["__main__"].language = Mock()
        sys.modules["__main__"].opener = Mock()
        sys.modules["__main__"].cookiejar = Mock()

        import YouTubeUtils
        sys.modules["__main__"].utils = Mock(spec=YouTubeUtils.YouTubeUtils)
        sys.modules["__main__"].utils.INVALID_CHARS = "\\/:*?\"<>|"

        sys.modules["__main__"].common = Mock()
        sys.modules["__main__"].common.log.side_effect = self.log
        sys.modules["__main__"].common.USERAGENT = "Mozilla/5.0 (MOCK)"

        sys.modules["__main__"].cache = Mock()

        import YouTubeStorage
        sys.modules["__main__"].storage = Mock(spec=YouTubeStorage.YouTubeStorage)
        import YouTubeCore
        sys.modules["__main__"].core = Mock(spec=YouTubeCore.YouTubeCore)
        import YouTubeLogin
        sys.modules["__main__"].login = Mock(spec=YouTubeLogin.YouTubeLogin)
        import YouTubeFeeds
        sys.modules["__main__"].feeds = Mock(spec=YouTubeFeeds.YouTubeFeeds)
        import YouTubeScraper
        sys.modules["__main__"].scraper = Mock(spec=YouTubeScraper.YouTubeScraper)
        import YouTubePlayer
        sys.modules["__main__"].player = Mock(spec=YouTubePlayer.YouTubePlayer)
        sys.modules["__main__"].downloader = Mock()
        import YouTubeScraper
        sys.modules["__main__"].scraper = Mock(spec=YouTubeScraper.YouTubeScraper)
        import YouTubePlaylistControl
        sys.modules["__main__"].playlist = Mock(spec=YouTubePlaylistControl.YouTubePlaylistControl)
        import YouTubeNavigation
        sys.modules["__main__"].navigation = Mock(spec=YouTubeNavigation.YouTubeNavigation)

    def mockXBMC(self):
        from mock import Mock
        sys.path.append("../xbmc-mocks/")
        import xbmc
        import xbmcaddon
        import xbmcgui
        import xbmcplugin
        import xbmcvfs

        #Setup basic xbmc dependencies
        sys.modules["__main__"].xbmc = Mock(spec=xbmc)
        sys.modules["__main__"].xbmc.translatePath = Mock()
        sys.modules["__main__"].xbmc.translatePath.return_value = "testing"
        sys.modules["__main__"].xbmc.getSkinDir = Mock()
        sys.modules["__main__"].xbmc.getSkinDir.return_value = "testSkinPath"
        sys.modules["__main__"].xbmc.getInfoLabel.return_value = "some_info_label"
        sys.modules["__main__"].xbmcaddon = Mock(spec=xbmcaddon)
        sys.modules["__main__"].xbmcgui = Mock(spec=xbmcgui)
        sys.modules["__main__"].xbmcgui.WindowXMLDialog.return_value = "testWindowXML"

        sys.modules["__main__"].xbmcplugin = Mock(spec=xbmcplugin)
        sys.modules["__main__"].xbmcvfs = Mock(spec=xbmcvfs)
        sys.modules["__main__"].settings = Mock(spec=xbmcaddon.Addon())
        sys.modules["__main__"].settings.getAddonInfo.return_value = "somepath"

        sys.modules["DialogDownloadProgress"] = __import__("mock")
        sys.modules["DialogDownloadProgress"].DownloadProgress = Mock()

    def log(self, description, level=0):
        if sys.modules["__main__"].dbg and sys.modules["__main__"].dbglevel > level:
            try:
                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), "YouTube IntegrationTest", inspect.stack()[3][3], description.decode("utf-8", "ignore"))
            except:
                print "%s [%s] %s : '%s'" % (time.strftime("%H:%M:%S"), "YouTube IntegrationTest", inspect.stack()[3][3], description)
