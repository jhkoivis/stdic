from filefilter import *
from glob import glob
from os import path

class PairIteratorFactory:
    
    def __init__(self):
        self.PairIteratorPropertyList = [
                                     (set(["First"]), ToFirstPairIterator),
                                     (set(["Previous"]), ToPreviousPairIterator),
                                     ]

    def getPairIterator(self, properties, configuration, filters=None):
        for PairIteratorProperty in self.PairIteratorPropertyList:
            if (PairIteratorProperty[0] & properties) == PairIteratorProperty[0]:
                return PairIteratorProperty[1](configuration, filters)
            
class PairIterator:
    
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
    
class ToFirstPairIterator(PairIterator):

    def __init__(self, configuration, filters):
        self.filters = filters
        PairIterator.__init__(self, configuration.pop("Folder"))
        
class ToPreviousPairIterator(PairIterator):

    def __init__(self, configuration, filters):
        self.filters = filters
        PairIterator.__init__(self, configuration.pop("Folder"))
        