''' 
     XBMC plugin dummy for testing.
     Version: 1.0
'''

def endOfDirectory(*args, **kwargs):
    print "XBMCPlugin : endOfDirectory : " + repr(args) + " - " + repr(kwargs)
    return True

def addDirectory(*args, **kwargs):
    print "XBMCPlugin : addDirectory : " + repr(args) + " - " + repr(kwargs)
    return True

def setContent(*args, **kwargs):
    print "XBMCPlugin : setContent : " + repr(args) + " - " + repr(kwargs)
    return True

def addSortMethod(*args, **kwargs):
    print "XBMCPlugin : addSortMethod : " + repr(args) + " - " + repr(kwargs)
    return True

def setResolvedUrl(*args, **kwargs):
    print "XBMCPlugin : setResolvedUrl : " + repr(args) + " - " + repr(kwargs)
    return True
