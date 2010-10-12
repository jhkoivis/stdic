
from unittest import TestCase
from imagefilters import *

class test_filefilter(TestCase):
    
    def testImageFilterFactory(self):
        testconfig_firstpicturenumber = dict({"FirstPictureNumber":1})
        
        test_factory = imagefilter.ImageFilterFactory()
        self.assertTrue(isinstance(test_factory.getImageFilters(testconfig_firstpicturenumber)[0], firstpicturenumberfilter.FirstPictureNumberFilter))