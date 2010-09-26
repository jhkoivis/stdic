
import unittest
import masterdata

class mock_ConfigParser:
	
	def __init__(self):
		self.parseCalled = False
	
	def parse(self):
		self.parseCalled = True

	def setMasterdata(self, null):
		pass


class test_masterdata(unittest.TestCase):

	def testInitAndGetSet(self):
		configFn = "configFn"
		CALLER = "NAME"
		mockconfigparser = mock_ConfigParser()
		md = masterdata.MasterData(mockconfigparser)
		md.set("Caller", CALLER)
		self.assertEquals(md.get("Caller"), CALLER)
		self.assertTrue(md.check("Caller"))
		self.assertTrue(mockconfigparser.parseCalled)
