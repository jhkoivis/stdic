
import unittest
import masterdata
from os import path

class test_masterdata(unittest.TestCase):

	folder	= path.join("testsuite","test_masterdata")
	testMD	= masterdata.MasterData(path.join(folder,"test_masterdata1.dicconf"))
	errorMD = path.join(folder,"test_masterdata2.dicconf")
	
	def testCaller(self):
		self.assertEquals(self.testMD.get("Caller"),"test_masterdata.py")

	def testIntegers(self):
		self.assertEquals(self.testMD.get("int"), 5)
		self.assertEquals(self.testMD.get("intWithWhitespace"), 32)
		self.assertEquals(self.testMD.get("intWithComment"), 7)

	def testFloats(self):
		self.assertEquals(self.testMD.get("float"), 3.14)
		self.assertEquals(self.testMD.get("floatWithWhitespace"), 42.11322)
		self.assertEquals(self.testMD.get("floatWithComment"), 11.27)

	def testTuples(self):
		self.assertEquals(self.testMD.get("tuple"), (3.14,1))
		self.assertEquals(self.testMD.get("tupleWithWhitespace"), (42.11322,32))
		self.assertEquals(self.testMD.get("tupleWithComment"), (11,27))

	def testStrings(self):
		self.assertEquals(self.testMD.get("string"), "3.14 = about pii")
		self.assertEquals(self.testMD.get("stringWithWhitespace"), "	whitespace   ")
		self.assertEquals(self.testMD.get("stringWithComment"), "stringtocomment")

	def testRegularExpressions(self):
		self.assertEquals(self.testMD.get("reg"), "(?P<3\.14>\w+)\.(?P<pii>\w+)\.txt")
		self.assertEquals(self.testMD.get("regWithWhitespace"),"(?P<		whitespace>\w+)")
		self.assertEquals(self.testMD.get("regWithComment"), "(?P<stringtocomment>\w+)")

	def testGetandSet(self):
		key = "number"
		value = 75.25
		self.testMD.set(key, value)
		self.assertEquals(self.testMD.get(key), 75.25)

	def testException_uncommentedline1(self):
		self.writeError(["[test_masterdata.py]","uncommented line"])
		self.failData()

	def testException_uncommentedline2(self):
		self.writeError(["[paragraph]","uncommented line"])
		self.failData()

	def testException_invalidfloat1(self):
		self.writeError(["[test_masterdata.py]","float = 3. 14"])
		self.failData()

	def testException_invalidfloat2(self):
		self.writeError(["[test_masterdata.py]","float = 3..14"])
		self.failData()

	def testException_invalidtuple(self):
		self.writeError(["[test_masterdata.py]","tuple = (1, 1. 1)"])
		self.failData()

	def writeError(self, strings):
		errorconfig = open(path.join(self.errorMD), 'w+')
		for string in strings:
			errorconfig.write(string + '\r\n')
		errorconfig.close

	def failData(self):
		try:
			faildata = masterdata.MasterData(self.errorMD)
			self.fail()
		except:
			pass
