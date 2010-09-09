import numpy
import sys
import math

class dff:
	
	def __init__(self, filename):
		self.filename = filename
		self.computed = False
	
	def __compute__(self):
		if not self.computed:
			(self.time, self.ydata) = self.__readydata__(self.filename)
			self.relativestrain =  self.__relativestrain__(self.ydata)
			self.__moments__()
			self.computed = True

	def __readydata__(self, filename):
		file = open(filename, 'r')
		ydata=[]
		xcoord = 0
		prevxcoord = 0
		cols = 1
		TIME = -1.0
		while 1:
			line = file.readline()
			if not line:
				break
			data = line.split()
			if line[0] == '%':
				if data[1] == 'time:':
					TIME = float(data[2])
				continue
			xcoord = int(data[0])
			if xcoord > prevxcoord:
				cols = cols + 1
			ycoord = int(data[1])
			ydata.append(float(data[3])-float(data[1]))
			prevxcoord = xcoord
		
		Z = numpy.array(ydata)
		rows = Z.shape[0]/cols
		Z = numpy.reshape(Z,(cols,rows))
		return (TIME, numpy.transpose(Z))
	
	def __relativestrain__(self, Zh):
		b=0.0
		k=0.0
		clamp = []
		for j in range (0, Zh.shape[1]):
			mid = Zh[:,j]
			xx = range(0, (len(mid))*10, 10)
			fit = numpy.polyfit(xx, mid, 1)
			k = fit[0]
			b = fit[1]
		clamp.append(b/k)
		zero = numpy.average(clamp)
		for j in range (0, Zh.shape[0]):
			for i in range (0, Zh.shape[1]):
				Zh[j,i] = Zh[j,i]/ (zero+j*10)
		center = Zh.shape[0]/2
		return Zh[(center):(Zh.shape[0]-5), 5:(Zh.shape[1]-5)]
	
	def __moments__(self):
		A = self.relativestrain
		N = numpy.product(numpy.shape(A))
		m1 = numpy.sum(A)/N
		m2 = numpy.sum(A*A)/N
		m3 = sum(A*A*A)/N
		m4 = sum(A*A*A*A)/N
		self.m1 = float(m1)
		self.variance = m2 - m1*m1
		self.stddev =  numpy.sqrt(self.variance)
		self.thirdcentralmoment = (m3 - 3 * m1* m2 + 2*m1**3)
		self.skewness = self.thirdcentralmoment/self.stddev**3
	
	def get_relativestrain(self):
		self.__compute__()
		return self.relativestrain
	
	def get_time(self):
		self.__compute__()
		return self.time
	
	def get_averagestrain(self):
		self.__compute__()
		return self.m1
	
	def get_cumulants(self):
		self.__compute__()
		return (self.m1, self.variance, self.thirdcentralmoment)
	
	def get_skewness(self):
		self.__compute__()
		return self.skewness
