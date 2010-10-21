
from unittest import TestCase
from imagefilters import *

class mock_imageobject:
    
    def __init__(self):
        self.picturenumber = 100
        
class mock_configsub:
    
    def __init__(self, name, configdict):
        self.configDict = dict({'name':name})
        self.configDict.update(configdict)
    
    def getValues(self):
        return self.configDict
        
class mock_configobject:
    
    def __init__(self):
        sub1 = mock_configsub('FirstPictureNumber', dict({'picturenumber':50}))
        self.subs = dict({'sub1':sub1})
    
    def getSubs(self):
        return self.subs
        
class test_imagefilters(TestCase):
    
    def _checkInstance(self, instance):
        filterclasses = [
                         firstpicturenumberfilter.FirstPictureNumberFilter,
                         imagefilter.TrueFilter
                         ]
        
        for filterclass in filterclasses:
            if isinstance(instance, filterclass):
                return True
        return False
    
    def testImageFilterFactory(self):
        testconfig = mock_configobject()
        
        test_factory = imagefilter.ImageFilterFactory()
        filters = test_factory.getImageFilters(testconfig)
        for filter in filters:
            self.assertTrue(self._checkInstance(filter))
        
    def test_FirstPictureNumberFilter(self):
        
        test_filter1 = firstpicturenumberfilter.FirstPictureNumberFilter(1)
        test_filter2 = firstpicturenumberfilter.FirstPictureNumberFilter(101)
        
        mock_image = mock_imageobject()
        
        self.assertTrue(test_filter1.filter(mock_image))
        self.assertFalse(test_filter2.filter(mock_image))