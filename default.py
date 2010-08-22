import sys, xbmc, xbmcaddon
#import YouTubeCore as core

REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger work for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")

# plugin constants
__plugin__ = "YouTube"
__author__ = "TheCombine"
__url__ = "www.xbmc.com"
__svn_url__ = ""
__version__ = "1.0.0"
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "32430"

__settings__ = xbmcaddon.Addon(id='plugin.video.youtube.beta')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting( "debug" ) == "True"

if (__name__ == "__main__" ):
    import YouTubeNavigation as navigation
    navigator = navigation.YouTubeNavigation()

    if ( not __settings__.getSetting( "firstrun" ) ):
         __settings__.openSettings()
         __settings__.setSetting( "firstrun", '1' )
    if (not sys.argv[2]):
        navigator.listMenu()
    else:
        if __dbg__:
            print __plugin__ + " ARGV: " + sys.argv[2]
        params = navigator.getParameters(sys.argv[2])
        get = params.get
        if (get("action")):
            navigator.executeAction(params)
        elif (get("path")):
            navigator.listMenu(params)
