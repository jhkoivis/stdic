
from sequencefilter import *

class SequenceFilterFactory:
    
    def __init__(self):
        self.sequenceFilterDictionary = dict({
                                              "Linear":LinearSequence
                                              })

    def getSequenceFilter(self, name, orderer, configuration=None):
        
        return self.sequenceFilterDictionary[name](orderer, configuration)

class SequenceFilter:
    
    def __init__(self, orderer = None):
        self.orderFunction = orderer.order
        
    def _sort(self, listing):
        return sorted(listing, cmp=self.orderFunction)