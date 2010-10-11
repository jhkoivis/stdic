
class SequenceFilterFactory:
    
    def __init__(self):
        self.sequenceFilterDictionary = dict({
                                              "FirstPictureNumber":LinearSequence
                                              })

    def getSequenceFilter(self, sequence_configuration):
        name = sequence_configuration.name
        order = sequence_configuration.order
        parameter_value = getattr(sequence_configuration,'parameter',None)
        
        filter = self.sequenceFilterDictionary[name]
        return filter(order, parameter_value)

class SequenceFilter:
    
    def __init__(self, order):
        self.order = order
    
class LinearSequence:
    
    def __init__(self, order, skip=1):
        
        self.skip = 1
        SequenceFilter.__init__(order)