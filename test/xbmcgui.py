''' 
     XBMC Gui dummy for testing.
     Version: 1.0
'''

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

def Dialog(*args, **kwargs):
    print "XBMCGui : Dialog : " + repr(args) + " - " + repr(kwargs)
    return True
