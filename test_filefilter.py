
from unittest import TestCase
from filefilter import FileFilterFactory
from filefilter import FirstPictureNumberFilter
from filefilter import LastPictureNumberFilter
from filefilter import FirstPictureOrdinalFilter
from filefilter import LastPictureOrdinalFilter

class test_filefilter(TestCase):
    
    def testPairHolderFactory(self):
        testconfig_firstpicturenumber = dict({"FirstPictureNumber":1})
        
        test_factory = FileFilterFactory()
        self.assertTrue(isinstance(test_factory.getFileFilters(testconfig_firstpicturenumber)[0], FirstPictureNumberFilter))