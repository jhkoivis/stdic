from sequencefilter import SequenceFilter
    
class LinearSequence(SequenceFilter):
    
    def __init__(self, orderer, skip=1):
                
        self.skip = skip
        SequenceFilter.__init__(self, orderer)
        
    def filter(self, objectlist):
        
        sortedlist = self.orderer.order(objectlist)

        skippedlist = []
        index = 0
        while index < len(sortedlist):
            skippedlist.append(sortedlist[index])
            index += self.skip
        
        return skippedlist