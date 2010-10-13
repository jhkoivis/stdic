
from unittest import TestCase
from sequencefilters import *

class mock_orderer:

    def order(self, imagelist):
        return imagelist

class test_sequencefilters(TestCase):
    
    def testSequenceFilterFactory(self):
        test_factory = sequencefilter.SequenceFilterFactory()
        orderer = mock_orderer()
        
        config1 = ["Linear", orderer]
        
        filter1 = test_factory.getSequenceFilter(*config1)
        
        self.assertTrue(isinstance(filter1, linearsequence.LinearSequence))
        
    def test_LinearSequence(self):
        orderer = mock_orderer()
        config1 = [orderer, 1]
        config2 = [orderer, 2]
        test_sequence1 = linearsequence.LinearSequence(*config1)
        test_sequence2 = linearsequence.LinearSequence(*config2)
        
        numberlist = range(10)
        result1 = numberlist
        result2 = range(0,10,2)
        
        self.assertEquals(test_sequence1.filter(numberlist), result1)
        self.assertEquals(test_sequence2.filter(numberlist), result2)