#!/usr/bin/python
"""
	See stdic.py for original file.
	Use method modifyMasterdata for programmable access to stdic. 
	
	The purpose of this is to show how to access the parameters via
	python.

	TODO: Make singleAnalyzer-class (c.f. folderAnalyzer)

	Juha Koivisto, 2010
	Simo Tuomisto, 2010

"""
from folderanalyzer import FolderAnalyzer
from configparser import ConfigParser
from masterdata import MasterData
from glob import glob
import sys
import os
import time


def modifyMasterdata(stdic):
	"""
	Override configuration parameters here.
	"""
	# set input and output -folders
	stdic.imagefolder = "test_transforms/test_at/"
	stdic.dfffolder = "test_transforms/test_at/dff"
	
	# initialize imagelist
	imageList = glob(stdic.imagefolder +'/*.tiff')
	imageList.sort()
	imageList = map(lambda x: x.split('/')[-1], imageList)

	for i in range(1,len(imageList)-1):

		firstImage = imageList[i]
		secondImage = imageList[i+1]
	
		confFn = '/tmp/' + '%lf' % time.time() + '.dicconf'
		confFile = open(confFn, 'w')
		confFile.write('[stdic.py]\n')
		confFile.write('Analyze = "%s"\n' % 		'True')
		confFile.write('AnalyzeTo = "%s"\n' % 		firstImage)
		confFile.write('FirstPicture = "%s"\n' % 	firstImage)
		confFile.write('LastPicture = "%s"\n' % 	secondImage)
		confFile.write('PictureSkip = %s\n' % 	'0')
		confFile.write('AnalyzesMax = %s\n' %     '100000')
		confFile.write('OverwriteDffs = "%s"\n' %   'False')
		confFile.write('WriteCoefs = "%s"\n' %		'False')
		confFile.write('Verbose = %s\n' %			'1')
		confFile.write('DffStep = %s\n' %			'10')
		confFile.write('[deformdata.py]\n')
		confFile.write('Crop = "%s"\n' %   			'False')
		confFile.write('CropXStart = %s\n' %      '300')
		confFile.write('CropXEnd = %s\n' %     	'600')
		confFile.write('CropYStart = %s\n' %      '50')
		confFile.write('CropYEnd = %s\n' %        '250')
		confFile.write('CrateTuple = %s\n' %      '(16,16)')
		confFile.write('Verbose = %s\n' %         '3')
		confFile.write('Xtol = %s\n' %         	'0.05')
		confFile.write('DegF = %s\n' %            '3')
		confFile.write('DegC = %s\n' %          	'3')
		confFile.write('[deformdata.py]\n')
		confFile.write('PictureForm = %s\n' %		'<<ignore>-<PictureNumber>.tiff>')
		
		confFile.close()

		ConfigParser(confFn, stdic.masterdata, 'stdic.py').parse()
		ConfigParser(confFn, stdic.masterdata, 'all').parse()
		ConfigParser(confFn, stdic.masterdata, 'deformdata.py').parse()
		
		stdic.run()









class Stdic:
	""" Analyzes series of images in a folder. The purpose of this class is to initialize 
		the objects and their dependices, and offer a method to run the analysis """
	# XXX: bit rigid, but on purpose
	def __init__(self):
		"""
			Reads default configuration file. These parameters 
			can be overridden in modifyMasterdata (see above)
		"""
		self.masterdata = MasterData()
		modifyMasterdata(self)
	
	def run(self):

		
		self.analyzer = FolderAnalyzer(self.imagefolder, 
										self.dfffolder, 
										self.masterdata, 
										self.masterdata)
		self.analyzer.analyze()

def usage():
	print ""
	print "Usage: python stdic_programming_interface.py"
	print ""
	print "all the parameters are defined in method modifyMasterdata"
	print "(first method in stdic_programming_interface.py)"
	sys.exit()
	
if __name__ == "__main__":
	arglist = sys.argv[1:]
	if len(arglist) != 0:
		usage()
	stdic = Stdic(*arglist)
	stdic.run()
