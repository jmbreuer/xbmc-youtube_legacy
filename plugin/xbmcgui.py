''' 
     XBMC Gui dummy for testing.
     Version: 1.0
'''

class Dialog():
    def create(*args, **kwargs):
        print "XBMCGui : Dialog->create : " + repr(args) + " - " + repr(kwargs)
        return True

    def close(*args, **kwargs):
        print "XBMCGui : Dialog->close : " + repr(args) + " - " + repr(kwargs)
        return True

    def update(*args, **kwargs):
        print "XBMCGui : Dialog->update : " + repr(args) + " - " + repr(kwargs)
        return True

    def select(*args, **kwargs):
        print "XBMCGui : Dialog->select : " + repr(args) + " - " + repr(kwargs)
        return True

def ControlImage(*args, **kwargs):
    print "XBMCGui : ControlImage : " + repr(args) + " - " + repr(kwargs)
    return True

def ControlLabel(*args, **kwargs):
    print "XBMCGui : ControlLabel : " + repr(args) + " - " + repr(kwargs)
    return True

def ControlProgress(*args, **kwargs):
    print "XBMCGui : ControlProgress : " + repr(args) + " - " + repr(kwargs)
    return True

def WindowXMLDialog(*args, **kwargs):
    print "XBMCGui : WindowXMLDialog : " + repr(args) + " - " + repr(kwargs)
    return True

def getCurrentWindowId(*args, **kwargs):
    print "XBMCGui : getCurrentWindowId : " + repr(args) + " - " + repr(kwargs)
    return True

def Window(*args, **kwargs):
    print "XBMCGui : Window : " + repr(args) + " - " + repr(kwargs)
    return True

def ListItem(*args, **kwargs):
    print "XBMCGui : ListItem : " + repr(args) + " - " + repr(kwargs)
    return True

