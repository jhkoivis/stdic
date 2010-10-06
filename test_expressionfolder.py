from unittest import TestCase
from expressionfolder import ExpressionFolder
from os import path
from os import getcwd

class test_ExpressionFolder(TestCase):
    
    def test_ExpressionFolder(self):
        
        pathname = getcwd()
        
        test_ExpressionFolder1 = ExpressionFolder(pathname)
        test_ExpressionFolder2 = ExpressionFolder(pathname)
        test_ExpressionFolder3 = ExpressionFolder(pathname)
        
        test_expression1 = '^expressionfolder\.py$'
        test_expression2 = '^test_expressionfolder\.py$'
        test_expression3 = '^.*expressionfolder\.py$'
        
        test_ExpressionFolder1.findWithExpression(test_expression1)
        test_ExpressionFolder2.findWithExpression(test_expression2)
        test_ExpressionFolder3.findWithExpression(test_expression3)
        
        result1 = 'expressionfolder.py'
        result2 = 'test_expressionfolder.py'
        result3 = [result1, result2]
        
        self.assertEquals(test_ExpressionFolder1.getFileNames()[0], result1)
        self.assertEquals(test_ExpressionFolder2.getFileNames()[0], result2)
        self.assertTrue(set(test_ExpressionFolder3.getFileNames()) == set(result3))
        
        result1 = path.join(pathname, 'expressionfolder.py')
        result2 = path.join(pathname, 'test_expressionfolder.py')
        result3 = [result1, result2]
        
        self.assertEquals(test_ExpressionFolder1.getFiles()[0], result1)
        self.assertEquals(test_ExpressionFolder2.getFiles()[0], result2)
        self.assertTrue(set(test_ExpressionFolder3.getFiles()) == set(result3))