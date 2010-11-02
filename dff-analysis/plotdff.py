import sys
import numpy as np
import matplotlib.pyplot as mpl
from optparse import OptionParser
from dffreader import DffReader

class PlotDff:

	def __init__(self, filename, subPlots):
					
		reader = DffReader(filename)
		self.diffX = reader.defX - reader.origX
		self.diffY = reader.defY - reader.origY
		
		if subPlots%2 != 0:
			subPlots += 1
		
		self.columns = subPlots/2
		self.rows = subPlots/self.columns
			
		self.figure = mpl.figure()
		
		self.currentPlot = 0
		self.subPlots = subPlots
			
	def getNextPlot(self):
	
		self.currentPlot += 1
		
		if self.currentPlot > self.subPlots:
			self.currentPlot = 1
		
		return mpl.subplot(self.rows, self.columns, self.currentPlot)
		
	def plotDiffX(self):
		
		self.getNextPlot()
		
		diffX = self.diffX
		
		mpl.contourf(diffX,50)
		mpl.axis("tight")
		mpl.xlabel("X-displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
				
	def plotDiffY(self):
		
		self.getNextPlot()
			
		diffY = self.diffY
		
		mpl.contourf(diffY,50)
		mpl.axis("tight")
		mpl.xlabel("Y-displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
		
	def plotDiffXDer(self, axis):
		
		self.getNextPlot()

		derX = np.diff(self.diffX, 1, axis)
		
		mpl.contourf(derX,50)
		mpl.axis("tight")
		mpl.xlabel("Derivative of X-displacement towards %d axis" % axis)
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
		
	def plotDiffYDer(self, axis):
		
		self.getNextPlot()

		derY = np.diff(self.diffY, 1, axis)
		
		mpl.contourf(derY,50)
		mpl.axis("tight")
		mpl.xlabel("Der of Y-displacement: %d axis" % axis)
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
		
	def show(self):
		self.figure
		mpl.show()

if __name__ == "__main__":
	
	argparser = OptionParser()
	
	argparser.add_option("--xdiff", action="store_true", default=False, dest="xDiff")
	argparser.add_option("--ydiff", action="store_true", default=False, dest="yDiff")
	argparser.add_option("--xxdiff", action="store_true", default=False, dest="xx")
	argparser.add_option("--xydiff", action="store_true", default=False, dest="xy")
	argparser.add_option("--yxdiff", action="store_true", default=False, dest="yx")
	argparser.add_option("--yydiff", action="store_true", default=False, dest="yy")
	
	(options, positionalArgs) = argparser.parse_args()
	
	subPlots = 0
	
	if options.xDiff:
		subPlots += 1
	if options.yDiff:
		subPlots += 1
	if options.xx:
		subPlots += 1
	if options.xy:
		subPlots += 1
	if options.yx:
		subPlots += 1
	if options.yy:
		subPlots += 1
		
	filename = positionalArgs[0]
	
	if subPlots > 0:
		plot = PlotDff(filename, subPlots)
		if options.xDiff:
			plot.plotDiffX()
		if options.yDiff:
			plot.plotDiffY()
		if options.xx:
			plot.plotDiffXDer(1)
		if options.xy:
			plot.plotDiffXDer(0)
		if options.yx:
			plot.plotDiffYDer(1)
		if options.yy:
			plot.plotDiffYDer(0)
		plot.show()
	else:
		plot = PlotDff(filename, 4)
		plot.plotDiffX()
		plot.plotDiffY()
		plot.plotDiffXDer(1)
		plot.plotDiffYDer(0)
		plot.show()
		
#------------------------------------------------------------------------------

