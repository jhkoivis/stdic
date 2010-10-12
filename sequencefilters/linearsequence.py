from sequencefilter import SequenceFilter
    
class LinearSequence(SequenceFilter):
    
    def __init__(self, orderer, skip=1):
        
        self.skip = skip
        SequenceFilter.__init__(self, orderer)
        
    def filter(self, objectlist):
        
        sortedlist = self._sort(objectlist)

        skippedlist = []
        index = 0
        while index < len(sortedlist):
            skippedlist.append(index)
            index += self.skip
        
        return skippedlist