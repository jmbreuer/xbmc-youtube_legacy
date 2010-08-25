import sys, xbmc, xbmcaddon

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
__version__ = "0.9.6"
__plugin__ = "YouTube-" + __version__
__author__ = "TheCollective"
__url__ = "www.xbmc.com"
__svn_url__ = ""
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "32430"
__settings__ = xbmcaddon.Addon(id='plugin.video.youtube.beta')
__language__ = __settings__.getLocalizedString
__dbg__ = __settings__.getSetting( "debug" ) == "true"
__dbg__ = True

if (__name__ == "__main__" ):
    if __dbg__:
        print __plugin__ + " ARGV: " + repr(sys.argv)
    else:
        print __plugin__
    import YouTubeNavigation as navigation
    navigator = navigation.YouTubeNavigation()
    
    if ( not __settings__.getSetting( "firstrun" ) ):
        navigator.login()
        __settings__.setSetting( "firstrun", '1' )
        
    if (not sys.argv[2]):
        navigator.listMenu()
    else:
        params = navigator.getParameters(sys.argv[2])
        get = params.get
        if (get("action")):
            navigator.executeAction(params)
        elif (get("path")):
            navigator.listMenu(params)
