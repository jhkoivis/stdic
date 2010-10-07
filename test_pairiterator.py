
from pairiterator import PairIteratorFactory
from pairiterator import ToPreviousPairIterator
from pairiterator import ToFirstPairIterator
from unittest import TestCase

class test_pairiterator(TestCase):
    
    def testPairHolderFactory(self):
        testconfig_first = [set(["First"]), dict(Folder="dummyfolder"), "dummyfilters"]
        testconfig_previous = [set(["Previous"]), dict(Folder="dummyfolder"), "dummyfilters"]
                
        test_factory = PairIteratorFactory()
        self.assertTrue(isinstance(test_factory.getPairIterator(*testconfig_first), ToFirstPairIterator))
        self.assertTrue(isinstance(test_factory.getPairIterator(*testconfig_previous), ToPreviousPairIterator))