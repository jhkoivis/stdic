from unittest import TestCase
from imageobject import ImageObject
from PIL.TiffImagePlugin import TiffImageFile
from os import getcwd
from os import path

class test_ImageObject(TestCase):
    
    def test_ImageObject(self):
        
        folder = path.join(path.join(getcwd(), 'testsuite'), 'test_imageobject')
        
        imagefile = path.join(folder, 'test-parameter1-parameter2-0001.tiff')
        
        imageobject1 = ImageObject(imagefile)
        imageobject2 = ImageObject(imagefile, '^.*-(?P<key1>\w+)-(?P<key2>\w+)-(?P<picturenumber>\d+)\.tiff$')
        
        resultdictionary1 = dict({'filename':imagefile})
        resultdictionary2 = dict({'filename':imagefile, 'key1':'parameter1', 'key2':'parameter2', 'picturenumber':'0001'})
        
        self.assertTrue(isinstance(imageobject1.getImage(), TiffImageFile))
        
        for key in resultdictionary1:
            self.assertEquals(getattr(imageobject1,key), resultdictionary1[key])
            
        for key in resultdictionary2:
            self.assertEquals(getattr(imageobject2,key), resultdictionary2[key])