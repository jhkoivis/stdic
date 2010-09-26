
from configparser import ConfigParser
from masterdata import MasterData
from unittest import TestCase

import os
import inspect

class mock_MasterData(MasterData):

	def __init__(self):
		self.masterdata = dict()
		self.caller = "test_masterdata.py"

class test_configparser(TestCase):
	
	def setUp(self):
		folder	= os.path.join("testsuite","test_masterdata")
		self.mockmaster = mock_MasterData()
		self.configparser = ConfigParser(os.path.join(folder,"test_masterdata1.dicconf"))
		self.configparser.setMasterdata(self.mockmaster)
		self.configparser.parse()

	def testIntegers(self):
		self.assertEquals(self.mockmaster.get("int"), 5)
		self.assertEquals(self.mockmaster.get("intWithWhitespace"), 32)
		self.assertEquals(self.mockmaster.get("intWithComment"), 7)

	def testFloats(self):
		self.assertAlmostEqual(self.mockmaster.get("float"), 3.14)
		self.assertAlmostEqual(self.mockmaster.get("floatWithWhitespace"), 42.11322)
		self.assertAlmostEqual(self.mockmaster.get("floatWithComment"), 11.27)

	def testTuples(self):
		self.assertEquals(self.mockmaster.get("tuple"), (3.14,1))
		self.assertEquals(self.mockmaster.get("tupleWithWhitespace"), (42.11322,32))
		self.assertEquals(self.mockmaster.get("tupleWithComment"), (11
																    ,27))

	def testStrings(self):
		self.assertEquals(self.mockmaster.get("string"), "3.14 = about pii")
		self.assertEquals(self.mockmaster.get("stringWithWhitespace"), "	whitespace   ")
		self.assertEquals(self.mockmaster.get("stringWithComment"), "stringtocomment")

	def testRegularExpressions(self):
		self.assertEquals(self.mockmaster.get("reg"), "(?P<3\.14>\w+)\.(?P<pii>\w+)\.txt")
		self.assertEquals(self.mockmaster.get("regWithWhitespace"),"(?P<		whitespace>\w+)")
		self.assertEquals(self.mockmaster.get("regWithComment"), "(?P<stringtocomment>\w+)")

	def testGetandSet(self):
		key = "number"
		value = 75.25
		self.mockmaster.set(key, value)
		self.assertAlmostEqual(self.mockmaster.get(key), 75.25)

