#!/usr/bin/python
""" 

	Simo Tuomisto, 2010

"""

import diccore
import os
import masterdata
import configparser

from PIL import Image
from numpy import array


#------------------------------------------------------------------------------

class DeformationData:
	
	def __init__(self, firstPictureName, secondPictureName, configfile):
		parser = configparser.ConfigParser(configfile)
		self.masterdata = masterdata.MasterData(parser)
		self.set('FirstPictureName', firstPictureName)
		self.set('SecondPictureName', secondPictureName)
		imsize = Image.open(firstPictureName).size
		self.set('PictureSize', [imsize[0],imsize[1]])		
		try:
			parameters = dict(verbose = self.get('Verbose'), xtol = self.get('Xtol'), degf = self.get('DegF'), degc = self.get('DegC'), crate = self.get('CrateTuple'))
		except KeyError:
			raise KeyError("[deformdata.py]:{Verbose, Xtol, DegF, DegC, CrateTuple} must be defined.")		
		try:
			if self.get('Crop') == 'True':
				crop = [self.get('CropXStart'), self.get('CropXEnd'), self.get('CropYStart'), self.get('CropYEnd')]
				self.set('DefFunction', diccore.dic(firstPictureName, secondPictureName, parameters,crop))
				self.set('Crop', crop)
			else:
				self.set('DefFunction', diccore.dic(firstPictureName, secondPictureName, parameters))
				self.set('Crop', [0,imsize[0],0,imsize[1]])
		except KeyError:
			raise KeyError("[deformdata.py]:Crop must be defined.")
		self.set('Parameters',parameters) 

	def get(self, key):

		return self.masterdata.get(key)

	def set(self, key, value):

		self.masterdata.set(key, value)

	def check(self, key):

		return self.masterdata.check(key)


	def getDeformationAtPoints(self, points):
		"""
			Returns the endpoints of the given points
			in this deformation in a list.
			
			getDeformationAtPoints seems to use Matlab-convention of axes.
		"""
		reversedpoints = []
		for a in points:
			reversedpoints.append((a[1],a[0]))
		
		reversedendpoints = self.get('DefFunction').getDeformationAtPoints(array(reversedpoints, float))

		endpoints = []
		for a in reversedendpoints:
			endpoints.append((a[1], a[0]))

		return endpoints
		
	def getCoefs(self):
		
		return self.get('DefFunction').getCAsArray()
