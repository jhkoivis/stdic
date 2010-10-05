from unittest import TestCase
from imagefolder import ImageFolder
from os import path
from os import getcwd

class test_imagefolder(TestCase):
    
    def test_imagefolder(self):
        
        pathname = getcwd()
        
        test_imagefolder1 = ImageFolder(pathname)
        test_imagefolder2 = ImageFolder(pathname)
        test_imagefolder3 = ImageFolder(pathname)
        
        test_expression1 = '^imagefolder\.py$'
        test_expression2 = '^test_imagefolder\.py$'
        test_expression3 = '^.*imagefolder\.py$'
        
        test_imagefolder1.findImagesExpression(test_expression1)
        test_imagefolder2.findImagesExpression(test_expression2)
        test_imagefolder3.findImagesExpression(test_expression3)
        
        result1 = 'imagefolder.py'
        result2 = 'test_imagefolder.py'
        result3 = [result1, result2]
        
        self.assertEquals(test_imagefolder1.getImageNames()[0], result1)
        self.assertEquals(test_imagefolder2.getImageNames()[0], result2)
        self.assertTrue(set(test_imagefolder3.getImageNames()) == set(result3))
        
        result1 = path.join(pathname, 'imagefolder.py')
        result2 = path.join(pathname, 'test_imagefolder.py')
        result3 = [result1, result2]
        
        self.assertEquals(test_imagefolder1.getImageFiles()[0], result1)
        self.assertEquals(test_imagefolder2.getImageFiles()[0], result2)
        self.assertTrue(set(test_imagefolder3.getImageFiles()) == set(result3))