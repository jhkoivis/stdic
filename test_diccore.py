
from unittest import TestCase
from diccore import Dic

class test_diccore(TestCase):
	
	def testInit(self):
		""" default constructor should initialize at least these values """
		dic = Dic()
		self.assertTrue(dic.parameters)
		self.assertTrue(dic.parameters['verbose'])
		self.assertTrue(dic.parameters['xtol'] > 0)
		self.assertTrue(dic.parameters['degf'] > 1)
		self.assertTrue(dic.parameters['degc'] > 1)
		self.assertTrue(dic.parameters['crate'])
		
		