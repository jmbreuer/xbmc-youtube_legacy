import BeautifulSoup
import sys
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import urllib
import YouTubeCore

class YouTubeScraperCore:     
    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__"].__plugin__    
    __dbg__ = sys.modules[ "__main__" ].__dbg__

    core = YouTubeCore.YouTubeCore()