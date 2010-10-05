from filefilter import *
from glob import glob
from os import path

class PairHolderFactory:
    
    def __init__(self):
        self.pairHolderPropertyList = [
                                     (set(["First"]), ToFirstPairHolder),
                                     (set(["Previous"]), ToPreviousPairHolder),
                                     ]

    def getPairHolder(self, properties=None, folder=None, filters=None):
        for pairHolderProperty in self.pairHolderPropertyList:
            if (pairHolderProperty[0] & properties) == pairHolderProperty[0]:
                return pairHolderProperty[1](folder, filters)
            
class PairHolder:
    
    def __init__(self, folder):
        self.folder = folder
    
    def next(self):
        pass
    
    def __iter__(self):
        return self
    
    def __getFilteredFilelist(self):
        filelist = glob(path.join(self.folder, '*'))
        for filter in self.filters:
            filelist = filter.filter(filelist)
        return filelist
    
class ToFirstPairHolder(PairHolder):

    def __init__(self, folder, filters):
        self.filters = filters
        PairHolder.__init__(self, folder)
        
class ToPreviousPairHolder(PairHolder):

    def __init__(self, folder, filters):
        self.filters = filters
        PairHolder.__init__(self, folder)
        