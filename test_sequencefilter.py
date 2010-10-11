
from unittest import TestCase
from sequencefilter import SequenceFilterFactory

class test_filefilter(TestCase):
    
    def testPairHolderFactory(self):
        test_factory = SequenceFilterFactory()
        self.assertTrue(isinstance(test_factory.getSequenceFilters())