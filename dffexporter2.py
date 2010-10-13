from exporter import Exporter
from numpy import save as npsave

import os

class DffExportParameters:

	def __init__(self, overwrite=False, dffstep=10, writeCoefs=False, diccoreParameters=dict()):
		self.overwrite = overwrite
		self.dffstep = dffstep
		self.writeCoefs = writeCoefs
		self.diccoreParameters = diccoreParameters

class DffExporter2(Exporter):
	""" 
		Exports a deformation using single ASCII format as an output. 
	
		XXX: Describe format here.
	"""
	def __init__(self, image1, image2, deformation, exportparameters, outputfilename):
		self.image1	= image1
		self.image2 = image2
		self.deformation = deformation
		self.exportparameters = exportparameters
		self.outputfilename = outputfilename

	def initialize(self):
		if not os.path.exists(self.outputfilename) or self.exportparameters.overwrite:
			self.outputfile = open(self.outputfilename, 'w')
			return True
		return False

	def writeVersion(self):
		""" Deformation file version identification """
		self.outputfile.write('% version: 2.0')
	
	def writeMetadata(self):
		""" Deformation metadata """
		imagedata1 = self.image1.__dict__
		imagedata2 = self.image2.__dict__
		for key in imagedata1.keys():
			self.outputfile.write("%% image1 %s : %s\n" % (key, imagedata1[key]))
			self.outputfile.write("%% image2 %s : %s\n" % (key, imagedata2[key]))
		self.outputfile.write("\n")
	
	def writeDeformationData(self):
		""" deformation data """
		step = self.exportparameters.dffstep
		deformationarray = self.deformation.getDeformation(step)
		arrayshape = deformationarray.shape
		for xindex in xrange(0, arrayshape[1]):
			for yindex in xrange(0, deformationarray.shape[0]):
				x  = xindex*step
				y  = yindex*step
				xd = deformationarray[yindex,xindex]
				yd = deformationarray[yindex,xindex]
				self.outputfile.write("%d %d %lf %lf \n" % (x,y,xd,yd))
		
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
	