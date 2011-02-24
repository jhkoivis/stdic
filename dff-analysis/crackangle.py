import numpy as np
import sys
from math import *
from dffreader import DffReader
from scipy.ndimage.interpolation import map_coordinates

class CrackAngle:

	def __init__(self, dffFilename):
	
		dff = DffReader(dffFilename)
			
		diffY = dff.defY - dff.origY
		self.derY = np.diff(diffY, 1, 0)
		self.step = dff.step
		
	def setCoords(self,xcoord,ycoord,angle):
		
		xcoord = float(xcoord)/self.step
		ycoord = float(ycoord)/self.step
	
		angle = radians(angle)
	
		self.xcoords = np.array([], dtype=float)
		self.ycoords = np.array([], dtype=float)
		
		xcoordplus	= cos(angle)/self.step
		ycoordplus	= - sin(angle)/self.step
		maxX		= self.derY.shape[1] - 1
		maxY		= self.derY.shape[0] - 1
		
		while True:
			if xcoord < 0 or xcoord >= maxX or ycoord <= 0 or ycoord >= maxY:
				break
			self.xcoords = np.append(self.xcoords, xcoord)
			self.ycoords = np.append(self.ycoords, ycoord)
			
			xcoord += xcoordplus
			ycoord += ycoordplus
		
	def getE(self, xcoord, ycoord, angle):
		
		self.setCoords(xcoord, ycoord, angle)
		
		return map_coordinates(self.derY, [self.ycoords, self.xcoords], order=3)
	
	def getEs(self, xcoord, ycoord):
		
		self.setCoords(xcoord, ycoord, 45)
		e1 = map_coordinates(self.derY, [self.ycoords, self.xcoords], order=3)
		self.setCoords(xcoord, ycoord, -45)
		e2 = map_coordinates(self.derY, [self.ycoords, self.xcoords], order=3)
	
		return [e1,e2]