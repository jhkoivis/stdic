
from pairiterators import *
from unittest import TestCase

class test_pairiterators(TestCase):
    
    def test_PairIteratorFactory(self):
        config1 = 'First'
        config2 = 'Previous'

        factory = pairiterator.PairIteratorFactory()
        
        iterator1 = factory.getPairIterator(config1, [])
        iterator2 = factory.getPairIterator(config2, [])
        
        self.assertTrue(isinstance(iterator1, tofirstiterator.ToFirstIterator))
        self.assertTrue(isinstance(iterator2, topreviousiterator.ToPreviousIterator))
        
    def test_ToFirstIterator(self):
        
        imagelist = range(5)
        iterator = iter(tofirstiterator.ToFirstIterator(imagelist))
        
        results = []
        for number in imagelist:
            results.append((0,number))

        for tuple1, tuple2 in zip(results, iterator):
            self.assertEquals(tuple1, tuple2)
            
    def test_ToPreviousIterator(self):
        
        imagelist = range(5)
        iterator = iter(topreviousiterator.ToPreviousIterator(imagelist))
        
        results = []
        for number in imagelist:
            results.append((number,number + 1))
        results.pop(-1)

        for tuple1, tuple2 in zip(results, iterator):
            self.assertEquals(tuple1, tuple2)
        