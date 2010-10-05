from filefilter import *
from glob import glob

class PairHolderFactory:
    
    def __init__(self):
        self.pairHolderPropertyList = [
                                     (set(["Folder", "First"]), ToFirstPairHolder),
                                     (set(["Folder", "Previous"]), ToPreviousPairHolder),
                                     (set(["Picture1", "Picture2"]), SinglePairHolder)
                                    ]

    def getPairHolder(self, configuration):
        print configuration
        properties = set(configuration.keys())
        for pairHolderProperty in self.pairHolderPropertyList:
            if (pairHolderProperty[0] & properties) == pairHolderProperty[0]:
                return pairHolderProperty[1](configuration)
            
class PairHolder:
    
    def __init__(self, folder):
        self.folder = folder
        
    def getPairs(self):
        return self.pairs
    
    def next(self):
        return self.pairs.next()
    
    def __iter__(self):
        pass
    
    def __getFilelist(self, filter_configuration):
        filters = FileFilterFactory.getFileFilters(filter_configuration)
        for filter in filters:
            pass 
    
class ToFirstPairHolder(PairHolder):

    def __init__(self, configuration):
        self.filters = configuration.pop("Filters", dict())
        PairHolder.__init__(self, configuration.pop("Folder"))
        
class ToPreviousPairHolder(PairHolder):

    def __init__(self, configuration):
        self.filters = configuration.pop("Filters", dict())
        PairHolder.__init__(self, configuration.pop("Folder"))
    
class SinglePairHolder(PairHolder):
    
    def __init__(self, configuration):
        self.filters = configuration.pop("Filters", dict())
        PairHolder.__init__(self, None)
        