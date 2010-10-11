
    
class LinearSequence:
    
    def __init__(self, orderer, skip=1):
        
        self.skip = 1
        SequenceFilter.__init__(orderer)
        
    def filter(self, imagelist):
        
        sortedlist = self._sort(imagelist)

        skippedlist = []
        index = 0
        while index < xrange(len(sortedlist)):
            skippedlist.append(self.skip*index)
            index += 1