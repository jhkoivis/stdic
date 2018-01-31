      
class PairIterator:
    
    def __init__(self, imagelistobject):
        self.imagelist = imagelistobject
        

class PairIteratorFactory:
    
    def __init__(self):
    
        from tofirstiterator    import ToFirstIterator
        from topreviousiterator import ToPreviousIterator
        from tolagiterator      import ToLagIterator 
        
        self.PairIteratorDictionary = dict({
                                            "First"     :   ToFirstIterator,
                                            "Previous"  :   ToPreviousIterator,
                                            "Lag"       :   ToLagIterator,
                                            })

    def getPairIterator(self, name, imagelistobject, configdict=dict()):
        return self.PairIteratorDictionary[name](imagelistobject, **configdict)