''' 
     StorageServer override.
     Version: 1.0
'''

class StorageServer():
    def cacheFunction(self, funct = False, *args):
        return funct(*args)
    
    def Set(self, name, data):
        return ""

    def Get(self, name):
        return ""

    def SetMulti(self, name, data):
        return ""

    def GetMulti(self, name, items):
        return ""

    def lock(self, name):
        return False

    def unlock(self, name):
        return False
