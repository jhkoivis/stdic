
from unittest import TestCase
from dffexporter import DffExportParameters, DffExporter

import os

class MockDeformationData:
	# XXX: mock tells us that we are VERY coupled to the deformationdata
	def __init__(self):
		self.data = {"Crop" : (100,100,120,120), 
					 "PictureSize" : (100,100), 
					 "PictureData1":{"key":"in","key":"is"}, 
					 "PictureData2":{"complicated":"stuff"}, 
					 "Parameters":{"complicated":"stuff"}, 
					 "FirstPictureName":"name1",
					 "SecondPictureName":"name2"}
	def get(self, key):
		return self.data[key]

	def getDeformationAtPoints(self, pointarray):
		self.getDeformationAtPointsCalled = True
		return (3.4, 4.5)

class test_DffExporter(TestCase):
	
	def setUp(self):
		self.mockdeformation = MockDeformationData()
		self.exportparameters = DffExportParameters(overwrite=True)
		# XXX: dependency from fs resource
		self.testfilename = 'test.dff'


	def testInit(self):
		exporter = DffExporter(self.mockdeformation, 
									self.exportparameters, 
									self.testfilename)
		self.assertTrue(exporter.deformation)
		self.assertTrue(exporter.exportparameters)
		self.assertTrue(exporter.outputfilename)
		
		
	def testExportData(self):
		exporter = DffExporter(self.mockdeformation, 
							   self.exportparameters, 
							   self.testfilename)
		self.assertTrue(exporter.export())
		self.assertTrue(self.mockdeformation.getDeformationAtPointsCalled)
		self.assertTrue(os.path.exists(self.testfilename))
		# XXX: should assert data

	def tearDown(self):
		if os.path.exists(self.testfilename):
			os.remove(self.testfilename)
	