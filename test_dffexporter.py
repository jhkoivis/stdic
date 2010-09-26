
import unittest.TestCase
import dffexporter

class test_DffExporter(unittest.TestCase):
	
	def setUp(self):
		mockdeformation = MockDeformationData()
		mockconfiguration = MockConfigurationData()
		exportparameters = ExportParameters()
		
		self.exporter = DffExporter(mockdeformation, exportparameters, outputfile)