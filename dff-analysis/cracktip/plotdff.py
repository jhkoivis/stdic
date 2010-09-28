import sys
import numpy as np
import matplotlib.pyplot as mpl
from optparse import OptionParser

class PlotDff:

	def __init__(self, filename, subPlots):
			
		(self.diffX, self.diffY) = self.readDiffFromDff(filename)
		
		if subPlots%2 != 0:
			subPlots += 1
		
		self.columns = subPlots/2
		self.rows = subPlots/self.columns
			
		self.subPlots = subPlots
			
		self.figure = mpl.figure()
			
	def getNextPlot(self):
	
		self.figure
	
		try:
			self.currentPlot += 1
		except AttributeError:
			self.currentPlot = 0
			self.currentPlot += 1
		
		if self.currentPlot > self.subPlots:
			self.currentPlot = 1
		
		return mpl.subplot(self.rows, self.columns, self.currentPlot)
		
	def plotDiffX(self):
		
		if self.subPlots > 1:
			self.getNextPlot()
		
		diffX = self.diffX	
		
		mpl.contourf(diffX,50)
		mpl.axis("image")
		mpl.xlabel("X-displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
		
	def plotDerDiffX(self, axis):

		derXX = np.diff(self.diffX, 1, axis)
		
		mpl.contourf(derX,50)
		mpl.axis("image")
		mpl.xlabel("X-displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
		
	def plotDerDiffY(self, axis):

		derY = np.diff(self.diffY, 1, axis)
		
		mpl.contourf(derY,50)
		#mpl.contourf(derY,np.arange(-0.07,0.1,0.005))
		mpl.axis("image")
		mpl.xlabel("Y-strain")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
				
	def plotDiffY(self):
	
		self.figure
		
		if self.subPlots > 1:
			self.getNextPlot()
			
		diffY = self.diffY
		
		mpl.contourf(diffY[20:-20,20:-20],50)
		mpl.axis("image")
		mpl.xlabel("Y-displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		mpl.draw()
				
	def plotStrain(self):

		#mpl.subplot(2,2,4)
		mpl.figure(3)
		#print diffY.T.shape
		strainY = diffY.T[1:77,:] - diffY.T[0:76,:]
		#strainY[:,0:20] =np.mean(strainY)
		#strainY[:,-10:10] = np.mean(strainY)
		limMin = np.mean(strainY) - 3* np.std(strainY)
                limMax = np.mean(strainY) + 3* np.std(strainY)
                strainY[ strainY > limMax] = limMax
                strainY[ strainY < limMin] = limMin
		mpl.contourf(strainY,np.arange(-0.02,0.02,0.001))
		#mpl.contourf(strainY,50)
		mpl.axis("image")
		mpl.xlabel("Y-strain")
		mpl.colorbar()
		mpl.gca().invert_yaxis()

		if not grayScalePic == None:
			#mpl.subplot(2,2,3)
			mpl.figure(4)
			grayIm = mpl.imread(grayScalePic)
			# remove outlayers
			#limMin = np.mean(grayIm) - 3* np.std(grayIm)
			#limMax = np.mean(grayIm) + 3* np.std(grayIm)
			#grayIm[grayIm > limMax] = limMax
			#grayIm[grayIm < limMin] = limMin

			mpl.imshow(grayIm)
			mpl.xlabel('grayscale')
			mpl.gca().invert_yaxis()

		if saveString == None:
			mpl.show()
		else:
			mpl.figure(1)
			mpl.savefig(saveString + "-diffs.png")

	def readDiffFromDff(self, filename):
			
		dff = open(filename,'r')
		
		dfflines = dff.readlines()
		
		dff.close()
		
		lastline = dfflines[len(dfflines)-1]
		lastlinesplit = lastline.split()
		
		last_x	= int(lastlinesplit[0])
		last_y	= int(lastlinesplit[1])
		
		lastline2 = dfflines[len(dfflines)-2]
		lastlinesplit2 = lastline2.split()
		
		last2_y	= int(lastlinesplit2[1])
		
		step = last_y - last2_y
		
		dffpointsx	= (last_x + step)/step
		dffpointsy	= (last_y + step)/step
				
		diffX		= np.zeros((dffpointsy, dffpointsx),float)
		diffY		= np.zeros((dffpointsy, dffpointsx),float)
		
		for line in dfflines:
			linesplit = line.split()
			try:
				x	= int(linesplit[0])
				y	= int(linesplit[1])
				dx	= float(linesplit[2])
				dy	= float(linesplit[3])
			except (ValueError, IndexError):
				continue
				
			xcoord = x/step
			ycoord = y/step
			diffX[ycoord,xcoord]	= dx - x
			diffY[ycoord,xcoord]	= dy - y
			
		return (diffX, diffY)
						
	def show(self):
	
		self.figure
		mpl.axis("image")
		mpl.show()

if __name__ == "__main__":

	from threading import Thread
	
	argparser = OptionParser()
	
	argparser.add_option("-g", "--grayscale", dest="grayScalePic")
	argparser.add_option("-s", "--strain", action="store_true", default=False, dest="strainFigure")
	argparser.add_option("-x", "--xdiff", action="store_true", default=False, dest="xDiff")
	argparser.add_option("-y", "--ydiff", action="store_true", default=False, dest="yDiff")
	argparser.add_option("--xx", "--xxdiff", action="store_true", default=False, dest="xx")
	argparser.add_option("--xy", "--xydiff", action="store_true", default=False, dest="xy")
	argparser.add_option("--yx", "--yxdiff", action="store_true", default=False, dest="yx")
	argparser.add_option("--yy", "--yydiff", action="store_true", default=False, dest="yy")
	
	(options, positionalArgs) = argparser.parse_args()
	
	subPlots = 0
				
	if options.grayScalePic != None:
		parameterArgs['grayScalePic'] = options.grayScalePic
	if options.strainFigure:
		subPlots += 1
		subPlots += 1
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
		plot = PlotDff(filename, 4)
		if options.strainFigure:
			plot.plotStrain()
		if options.xDiff:
			plot.plotDiffX()
		if options.yDiff:
			plot.plotDiffY()
		if options.xx:
			plot.plotDerDiffX(1)
		if options.xy:
			plot.plotDerDiffX(0)
		if options.yx:
			plot.plotDerDiffY(1)
		if options.yy:
			plot.plotDerDiffY(0)
		plot.show()
		
#------------------------------------------------------------------------------

