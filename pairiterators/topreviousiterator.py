from pairiterator import PairIterator

class ToPreviousIterator(PairIterator):

    def __init__(self, imagelistobject):
        PairIterator.__init__(self, imagelistobject)
        
    def next(self):
        return (self._listiterator1.next(), self._listiterator2.next())
        
    def __iter__(self):
        self._listiterator1 = iter(self.imagelist)
        self._listiterator2 = iter(self.imagelist)
        self._listiterator2.next()
        return self