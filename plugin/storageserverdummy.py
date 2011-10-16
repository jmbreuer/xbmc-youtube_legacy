''' 
     StorageServer override.
     Version: 1.0
'''

class StorageServer():
    def cacheFunction(self, funct = False, *args):
        return funct(*args)
    
    def sqlSet(self, name, data):
        return ""

    def sqlGet(self, name):
        return ""

    def sqlSetMulti(self, name, data):
        return ""

    def sqlGetMulti(self, name, items):
        return ""

    def lock(self, name):
        return False

    def unlock(self, name):
        return False
