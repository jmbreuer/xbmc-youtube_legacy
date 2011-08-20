''' 
     XBMC Addon dummy for testing.
     Version: 1.0
'''

def Addon(*args, **kwargs):
    print "XBMCAddon : Addon " + repr(args) + " - " + repr(kwargs)
    return True
