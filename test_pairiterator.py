
from pairholder import PairHolderFactory
from pairholder import ToPreviousPairHolder
from pairholder import ToFirstPairHolder
from unittest import TestCase

class test_pairholder(TestCase):
    
    def testPairHolderFactory(self):
        testconfig_first = [set(["First"]),"dummyfolder", "dummyfilters"]
        testconfig_previous = [set(["Previous"]),"dummyfolder", "dummyfilters"]
                
        test_factory = PairHolderFactory()
        self.assertTrue(isinstance(test_factory.getPairHolder(*testconfig_first), ToFirstPairHolder))
        self.assertTrue(isinstance(test_factory.getPairHolder(*testconfig_previous), ToPreviousPairHolder))