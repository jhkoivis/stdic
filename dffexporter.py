from exporter import Exporter
from numpy import save as npsave

import os

class DffExportParameters:

	def __init__(self, overwrite=False, dffstep=10, writeCoefs=False, diccoreParameters=dict()):
		self.overwrite = overwrite
		self.dffstep = dffstep
		self.writeCoefs = writeCoefs
		self.diccoreParameters = diccoreParameters

class DffExporter(Exporter):
	""" 
		Exports a deformation using single ASCII format as an output. 
	
		XXX: Describe format here.
	"""
	def __init__(self, deformation, exportparameters, outputfilename):
		self.deformation = deformation
		self.exportparameters = exportparameters
		self.outputfilename = outputfilename

	def initialize(self):
		if not os.path.exists(self.outputfilename) or self.exportparameters.overwrite:
			self.outputfile = open(self.outputfilename, 'w')
			self.crop = self.deformation.get("Crop")
			self.size = self.deformation.get("PictureSize")
			self.picturedata1	= self.deformation.get("PictureData1")
			self.picturedata2	= self.deformation.get("PictureData2")
			self.firstpicturename = self.deformation.get("FirstPictureName")
			self.secondpicturename = self.deformation.get("SecondPictureName")
			return True
		return False

	def writeVersion(self):
		""" Deformation file version identification """
		self.outputfile.write('% version: 1.0')
	
	def writeMetadata(self):
		""" Deformation metadata """
		self.outputfile.write("%% picture1 filename: %s\n" % self.firstpicturename)
		for key in self.picturedata1:
			self.outputfile.write("%% picture2 %s: %s\n" % (key, self.picturedata1[key]))
		self.outputfile.write("\n")
		self.outputfile.write("%% picture2 filename: %s\n" % self.secondpicturename)
		for key in self.picturedata2:
			self.outputfile.write("%% picture2 %s: %s\n" % (key, self.picturedata2[key]))
		self.outputfile.write("\n")
		for key in self.exportparameters.diccoreParameters:
			self.outputfile.write("%% %s: %s\n" % (key, self.exportparameters.diccoreParameters[key]))
		self.outputfile.write("\n")
		self.outputfile.write("%% picture size x: %d\n" % self.size[0])
		self.outputfile.write("%% picture size y: %d\n" % self.size[1])
		self.outputfile.write("%% crop start   x: %d\n" % self.crop[0])
		self.outputfile.write("%% crop end     x: %d\n" % self.crop[1])
		self.outputfile.write("%% crop start   y: %d\n" % self.crop[2])
		self.outputfile.write("%% crop end     y: %d\n" % self.crop[3])
		self.outputfile.write("\n")
	
	def writeDeformationData(self):
		""" deformation data """
		step = self.exportparameters.dffstep
		pointarray = []
		rangex = xrange(0, self.crop[1] - self.crop[0], step)
		rangey = xrange(0, self.crop[3] - self.crop[2], step)
		for x in rangex:
			for y in rangey:
				pointarray.append([x,y])
		deformedpointarray = self.deformation.getDeformationAtPoints(pointarray)
		for index in xrange(0, len(pointarray)):
			x = pointarray[index][0]
			y = pointarray[index][1]
			xd = deformedpointarray[index][0]
			yd = deformedpointarray[index][1]
			self.outputfile.write("%d %d %lf %lf \n" % (x, y, xd, yd))
		
	def finalize(self):
		self.outputfile.close()
		if self.exportparameters.writeCoefs:
			self.__writeCoefs__()
		return True

	def __writeCoefs__(self):
		""" what is the point of this??? """
		# XXX: NOT TESTED. WRITE
		coefsArray = self.deformation.getCoefs()
		npsave(self.outputfilename + ".coefs", coefsArray)
	