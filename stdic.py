#!/usr/bin/python
"""

	Simo Tuomisto, 2010

"""

from folderanalyzer import FolderAnalyzer
from configparser import ConfigParser
from masterdata import MasterData

import sys

class Stdic:
	""" Analyzes series of images in a folder. The purpose of this class is to initialize 
	the objects and their dependices, and offer a method to run the analysis """
	# XXX: bit rigid, but on purpose
	def __init__(self, imagefolder,dfffolder, configfile):
		masterdata = MasterData()
		ConfigParser(configfile, masterdata, 'stdic.py').parse()
		ConfigParser(configfile, masterdata, 'deformdata.py').parse()
		ConfigParser(configfile, masterdata, 'all').parse()
		self.analyzer = FolderAnalyzer(imagefolder, dfffolder, masterdata, masterdata)

	def run(self):
		self.analyzer.analyze()

if __name__ == "__main__":
	stdic = Stdic(*sys.argv[1:])
	stdic.run()
