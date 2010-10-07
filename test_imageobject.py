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
        
        resultdictionary1 = dict({'Filename':imagefile})
        resultdictionary2 = dict({'Filename':imagefile, 'key1':'parameter1', 'key2':'parameter2', 'picturenumber':'0001'})
        
        self.assertTrue(isinstance(imageobject1.getImage(), TiffImageFile))
        
        self.assertEquals(imageobject1.getImageDataValue('Filename'), imagefile)
        
        self.assertEquals(imageobject1.getImageData(), resultdictionary1)
        self.assertEquals(imageobject2.getImageData(), resultdictionary2)