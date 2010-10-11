
from unittest import TestCase
from imagefilter import ImageFilterFactory
from imagefilter import FirstPictureNumberFilter
from imagefilter import LastPictureNumberFilter
from imagefilter import FirstPictureOrdinalFilter
from imagefilter import LastPictureOrdinalFilter

class test_filefilter(TestCase):
    
    def testPairHolderFactory(self):
        testconfig_firstpicturenumber = dict({"FirstPictureNumber":1})
        
        test_factory = ImageFilterFactory()
        self.assertTrue(isinstance(test_factory.getImageFilters(testconfig_firstpicturenumber)[0], FirstPictureNumberFilter))