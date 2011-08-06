''' 
     XBMCVFS override for Dharma.
'''

import os, sys, time, errno

def exists(target):
    return os.path.exists(target) 

def rename(origin, target):
    return os.rename(origin, target)

def delete(target):
    if os.path.isfile(target):
        return os.unlink(target)
    return False
        
