''' 
     XBMC dummy for testing.
     Version: 1.0
'''
abortRequested = False

def translatePath(*args, **kwargs):
    print "XBMC : translatePath : " + repr(args) + " - " + repr(kwargs)
    return True

def getSkinDir(*args, **kwargs):
    print "XBMC : getSkinDir : " + repr(args) + " - " + repr(kwargs)
    return True

def skinHasImage(*args, **kwargs):
    print "XBMC : skinHasImage : " + repr(args) + " - " + repr(kwargs)
    return True

def getInfoLabel(*args, **kwargs):
    print "XBMC : getInfoLabel : " + repr(args) + " - " + repr(kwargs)
    return True

def executebuiltin(*args, **kwargs):
    print "XBMC : executebuiltin : " + repr(args) + " - " + repr(kwargs)
    return True

def Player(*args, **kwargs): # Needs to return something that can do ().setSubtitles
    print "XBMC : Player : " + repr(args) + " - " + repr(kwargs)
    return True

def PlayList(*args, **kwargs):
    print "XBMC : PlayList : " + repr(args) + " - " + repr(kwargs)
    return True

def Keyboard(*args, **kwargs):
    print "XBMC : Keyboard : " + repr(args) + " - " + repr(kwargs)
    return "Dummy test string"

