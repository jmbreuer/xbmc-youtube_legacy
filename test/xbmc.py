''' 
     XBMC dummy for testing.
     Version: 1.0
'''
abortRequested = False

class Player():
    def isPlaying(*args, **kwargs):
        print "XBMC : Player->isPlaying : " + repr(args) + " - " + repr(kwargs)
        return True


    def setSubtitles(*args, **kwargs):
        print "XBMC : Player->setSubtitles : " + repr(args) + " - " + repr(kwargs)
        return True


    def stop(*args, **kwargs):
        print "XBMC : Player->Stop : " + repr(args) + " - " + repr(kwargs)
        return True


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

def PlayList(*args, **kwargs):
    print "XBMC : PlayList : " + repr(args) + " - " + repr(kwargs)
    return True

def Keyboard(*args, **kwargs):
    print "XBMC : Keyboard : " + repr(args) + " - " + repr(kwargs)
    return "Dummy test string"

