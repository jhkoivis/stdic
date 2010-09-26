#!/usr/bin/python
""" 

	Simo Tuomisto, 2010

"""

from diccore import Dic
import os
from masterdata import MasterData
from configparser import ConfigParser

from PIL import Image
from numpy import array


#------------------------------------------------------------------------------

class DeformationData:
	
	def __init__(self, firstPictureName, secondPictureName, configfile):
		parser = ConfigParser(configfile)
		self.masterdata = MasterData(parser)
		# XXX: this execution and initialization logic DOES NOT belong here
		self.dic = Dic(verbose = self.get('Verbose'), xtol = self.get('Xtol'), degf = self.get('DegF'), degc = self.get('DegC'), crate = self.get('CrateTuple'))
		self.set('FirstPictureName', firstPictureName)
		self.set('SecondPictureName', secondPictureName)
		imsize = Image.open(firstPictureName).size
		self.set('PictureSize', [imsize[0],imsize[1]])		
		try:
			if self.get('Crop') == 'True':
				crop = [self.get('CropXStart'), self.get('CropXEnd'), self.get('CropYStart'), self.get('CropYEnd')]
				self.deformationCtx =  self.dic.register(firstPictureName, secondPictureName,crop)
				self.set('Crop', crop)
			else:
				# XXX: when you refactor this, please remember to remove copy-paste below
				self.deformationCtx = self.dic.register(firstPictureName, secondPictureName)
				self.set('Crop', [0,imsize[0],0,imsize[1]])
		except KeyError:
			raise KeyError("[deformdata.py]:Crop must be defined.")

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
		reversedendpoints = self.deformationCtx.getDeformationAtPoints(array(reversedpoints, float))
		endpoints = []
		for a in reversedendpoints:
			endpoints.append((a[1], a[0]))

		return endpoints
		
	def getCoefs(self):		
		return self.deformationCtx.getCAsArray()
