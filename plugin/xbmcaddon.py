''' 
     XBMC Addon dummy for testing.
     Version: 1.0
'''

class Addon():
    def getSetting(*args, **kwargs):
        print "XBMCAddon : getSetting " + repr(args) + " - " + repr(kwargs)
        return "getSetting test return"

    def setSetting(*args, **kwargs):
        print "XBMCAddon : setSetting " + repr(args) + " - " + repr(kwargs)
        return True

    def openSetting(*args, **kwargs):
        print "XBMCAddon : openSetting " + repr(args) + " - " + repr(kwargs)
        return True

    def getAddonInfo(*args, **kwargs):
        print "XBMCAddon : getSetting " + repr(args) + " - " + repr(kwargs)

        if kwargs.has_key("path"):
            return "/tmp"
        else:
            return "getAddonInfo test return"
