from pairiterator import PairIterator

class ToFirstIterator(PairIterator):

    def __init__(self, imagelistobject):
        PairIterator.__init__(self, imagelistobject)
        
    def next(self):
        return (self.imagelist[0], self._listiterator.next())
        
    def __iter__(self):
        self._listiterator = iter(self.imagelist)
        return self