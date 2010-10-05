
from pairholder import PairHolderFactory
from pairholder import ToPreviousPairHolder
from pairholder import ToFirstPairHolder
from pairholder import SinglePairHolder
from unittest import TestCase

class test_pairholder(TestCase):
    
    def testPairHolderFactory(self):
        test_factory = PairHolderFactory()
        test_configuration = dict(Folder="dummy", Filters="dummy", First="dummy")
        self.assertTrue(isinstance(test_factory.getPairHolder(test_configuration), ToFirstPairHolder))
        test_configuration = dict(Previous="dummy", Folder="dummy", Filters="dummy")
        self.assertTrue(isinstance(test_factory.getPairHolder(test_configuration), ToPreviousPairHolder))
        test_configuration = dict(Picture2="dummy", Picture1="dummy")
        self.assertTrue(isinstance(test_factory.getPairHolder(test_configuration), SinglePairHolder))