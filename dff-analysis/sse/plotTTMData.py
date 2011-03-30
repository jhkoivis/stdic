import numpy
import pylab
from glob import glob
import matplotlib.pyplot as mpl

lag = 2000

# Pos. quadrant of (x,y,z)
sampleX = 6.0   # (mm)
sampleY = 12.0
sampleZ = 6.0
sampleArea = sampleX*sampleY/(10**6) # (m^2)


lines = numpy.loadtxt("dict.csv",dtype="string")
fatigues = {}
for i in range(lines.shape[0]):
	fn=lines[i].split(',')[0]
	fatigue=lines[i].split(',')[1]
	fatigues[fn]=fatigue

file = open("yield.csv", 'w')

for fn in glob("*.dat"):
	
	data = numpy.loadtxt(fn)

	# F -> stress
	data[:,1] = -data[:,1] * 200 / sampleArea
	
	# Drop off the points after Fmax
	sig_max_ind = numpy.argmax(data[:,1])
	data = data[:sig_max_ind,:]

	print "sig_max_ind = %g" % sig_max_ind

	# d -> epsilon
	data[:,2] = -data[:,2]
	data[:,2] = 100 * (data[:,2] - min(data[:,2])) / sampleZ	

	# Find e0
	diff = ( data[lag:,1] - data[:-lag,1] ) / (data[lag:,2] - data[:-lag,2])
	der_max_ind = numpy.argmax(diff[:diff.shape[0]/4])
	der_max     = diff[der_max_ind]	
	eps_E       = data[der_max_ind,2]
	sig_E       = data[der_max_ind,1]
	const       = sig_E - der_max*eps_E
	eps_0       = -const/der_max

	print "der_max_ind = %g" % der_max_ind
	print "der_max = %g" % der_max
	print "eps_E = %g" % eps_E
	print "sig_E = %g" % sig_E
        print "const = %g" % const
	print "eps_0 = %g" % eps_0

	# Find eps_y, sig_y
	linapp  = data[:,2]*der_max + const
	yld_ind = (linapp > 1.1*data[:,1])
	eps_y = numpy.extract(yld_ind,data[:,2])[0]
	sig_y = numpy.extract(yld_ind,data[:,1])[0]

	print "eps_y = %g" % eps_y
	print "sig_y = %g" % sig_y

	fat = int(fatigues[fn])
	print fat
	sf = "%d, %e, %e, %e, %e, %e\n" % (fat, eps_0, eps_E, sig_E, eps_y, sig_y)
	sf = fn + ", " + sf
	file.write(sf)
	
	# Plots

	mpl.figure(1)
	mpl.plot(data[:,2]-eps_0,data[:,1],label=fn)
#	mpl.plot(data[der_max_ind,2]-eps_0,data[der_max_ind,1],'ro',markersize=5)
#	mpl.plot(0,0,'go',markersize=5)
#	mpl.plot(data[:,2]-eps_0, data[:,2]*der_max+const,'g-')
#	mpl.plot(eps_y-eps_0,sig_y,'bo',markersize=5)
	#mpl.figure(2)
	#mpl.plot(data[:,2]-eps_0,data[:,1])
	#mpl.plot(data[:-lag,2],diff)
	#mpl.plot(data[der_max_ind,2],der_max,'ro',markersize=5)


file.close()
	
mpl.figure(1)
mpl.xlabel("Strain [%]")
mpl.ylabel("Stress [N/m^2]")
mpl.legend(loc="upper left")

#xmin, xmax = pylab.xlim()
#pylab.xlim(xmax, xmin)



mpl.show()
