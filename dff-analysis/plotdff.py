import sys
import numpy as np
#import matplotlib
#matplotlib.use('MacOSX')
import matplotlib.pyplot as mpl

class PlotDff:

	def __init__(	self, 
					filename, 
					imageName 	= None, 
					savestring	= None):
		
		self.filename 	= filename
		self.imageName 	= imageName
		self.savestring = savestring
		
		print "edit __init__ to use this"
		
		########################################	
		#diffX, diffY = self.readData(filename)
		#self.plotDisplacement(	diffX, 
		#						diffY, 
		#						filename, 
		#						imageName, 
		#						savestring)
		########################################
		#lag = 10
		#print diffY.shape
		#strainYY = diffY[lag:,:] - diffY[:-lag,:]
		#strainXY = diffY[lag:,X] - diffY[:,:-lag]
		#for i in range(1,93,10):
		#	print strainYY[i,38], " ",
		#print ""
		###########################################
		
	def plotDisplacement(self, diffX, diffY, filename, imageName, savestring):
		"""
			plots u and v (diffX and diffY retruned by readData) as contourplots.
		"""
		
		mpl.figure(1)
		
		mpl.subplot(2,1,1)
		mpl.contourf(diffX.T,50)
		mpl.axis("image")
		mpl.xlabel("X-directional displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
	
		mpl.title(filename.split('/')[-1])
	
		mpl.subplot(2,1,2)
		mpl.contourf(diffY.T,50)
		mpl.axis("image")
		mpl.xlabel("Y-directional displacement")
		mpl.colorbar()
		mpl.gca().invert_yaxis()
		
		#if not imageName == None:
			#mpl.subplot(4,2,1)
			#mpl.figure(2)
			#mpl.axis("image")
			#a = mpl.imread(imageName)
			#mpl.imshow(a)
			#mpl.show()
		
		if savestring == None:
			mpl.show()
		else:
			mpl.figure(1)
			mpl.savefig(savestring + "-XYdiff.png")
	

	
	def readData(self, filename):
		"""
			Reads dff to matrices: u,v (x-disp and y-disp)
		"""
		# read raw data
		dff = open(filename,'r')
		dfflines = dff.readlines()
		dff.close()
		
		# find spatial coordinates
		lastline = dfflines[len(dfflines)-1]
		lastlinesplit = lastline.split()
		
		last_x	= int(lastlinesplit[0])
		last_y	= int(lastlinesplit[1])
		
		# find step size
		# assume same step size
		# use last two lines
		lastline2 = dfflines[len(dfflines)-2]
		lastlinesplit2 = lastline2.split()
		last2_y	= int(lastlinesplit2[1])
		step = last_y - last2_y
		
		# get number of points using stepsize
		dffpointsx	= (last_x + step)/step
		dffpointsy	= (last_y + step)/step
				
		testX		= np.zeros((dffpointsx, dffpointsy),float)
		testY		= np.zeros((dffpointsx, dffpointsy),float)
		
		# parse the data
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
			testX[xcoord,ycoord]	= dx - x
			testY[xcoord,ycoord]	= dy - y
			
		xgrid		= np.arange(0,dffpointsx)
		ygrid		= np.arange(0,dffpointsy)
		refX, refY	= np.meshgrid(ygrid, xgrid)
			
		diffX		= testX
		diffY		= testY
		
		return (diffX, diffY)
		
		
			

if __name__=="__main__":
	
	if len(sys.argv) < 2:
		print "usage: dff-plotter, see __init__ for details"
		print "       python plotdff.py file.dff"
		sys.exit()
	
	plot = PlotDff(*sys.argv[1:])
