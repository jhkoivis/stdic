
class SequenceFilter:
    
    def __init__(self, orderer):
        self.orderer = orderer

class SequenceFilterFactory:
    
    def __init__(self, order):
        from linearsequence import LinearSequence
        
        self.order = order
        self.sequenceFilterDictionary = dict({
                                              "Linear":LinearSequence
                                              })

    def getSequenceFilter(self, name, configuration):
        
        return self.sequenceFilterDictionary[name](self.order, configuration)