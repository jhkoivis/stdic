import numpy
import pylab
import os
from glob import glob
import matplotlib.pyplot as mpl

lag = 50
pps = 10 # Points per second for interpolation

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

if os.path.exists('yield.csv'):
	saveToFile = False
else:
	saveToFile = True
	file = open("yield.csv", 'w')
	

def monotonize(list):
	for i in range(0,len(list)-1):
		if list[i] > list[i+1]:
			list[i+1] = list[i]


fnList = glob("*.dat")
fnList.sort()

for fn in fnList:
	
	data = numpy.loadtxt(fn)

	# F -> stress
	data[:,1] = -data[:,1] * 200 / sampleArea
	
	# Drop off the points after Fmax
	sig_max_ind = numpy.argmax(data[:,1])
	data = data[:sig_max_ind,:]

	print "sig_max_ind = %g" % sig_max_ind

	# d -> epsilon
	data[:,2] = -data[:,2]*3.157
	data[:,2] = 100 * (data[:,2] - data[0,2]) / sampleZ

	# interpolate data
	t = numpy.arange(0,data.shape[0])
	tpps = numpy.arange(0,data.shape[0],pps)
	einterp = numpy.interp(tpps,t,data[:,2])
	sinterp = numpy.interp(tpps,t,data[:,1])
	
	# Find e_0
	msinterp = sinterp.copy()
	monotonize(msinterp)
	diff  = (  sinterp[lag:] -  sinterp[:-lag] ) / ( einterp[lag:] - einterp[:-lag] )
	mdiff = ( msinterp[lag:] - msinterp[:-lag] ) / ( einterp[lag:] - einterp[:-lag] )
	mdiff[0:50] = 0 # We don't want the first points in any case.
	der_max_ind = numpy.argmax(mdiff[:int(len(diff)/2)])
	der_max     = diff[der_max_ind]	
	eps_E       = einterp[der_max_ind]
	sig_E       = sinterp[der_max_ind]
	const       = sig_E - der_max*eps_E
	eps_0       = -const/der_max

	print "der_max_ind = %g" % der_max_ind
	print "der_max = %g" % der_max
	print "eps_E = %g" % eps_E
	print "sig_E = %g" % sig_E
        print "const = %g" % const
	print "eps_0 = %g" % eps_0

	# Find the yield point (eps_y, sig_y)
	linapp  = einterp*der_max + const
	yld_ind = (linapp > 1.1*sinterp)
	eps_y = numpy.extract(yld_ind,einterp)[0]
	sig_y = numpy.extract(yld_ind,sinterp)[0]

	print "eps_y = %g" % eps_y
	print "sig_y = %g" % sig_y

	if saveToFile==True:
		fat = int(fatigues[fn])
		print fat
		sf = "%d, %e, %e, %e, %e, %e, %e\n" % (fat, eps_0, eps_E, der_max, sig_E, eps_y, sig_y)
		sf = fn + ", " + sf
		file.write(sf)
		
	sf = fn.split('.dat')[0] + "-interp.csv"
	out = numpy.array(zip(einterp-eps_0, sinterp), dtype='float')
	numpy.savetxt(sf, out, fmt='%f, %f')
	
	# Plots
	mpl.figure(1)
	mpl.plot(einterp-eps_0,sinterp,label=fn)
	mpl.plot(eps_E-eps_0,sig_E,'ro')
	mpl.plot(eps_y-eps_0,sig_y,'go')
	mpl.plot(0,0,'ko')

	mpl.figure(2)
	mpl.plot(einterp-eps_0,sinterp,label=fn)
	mpl.plot(eps_E-eps_0,sig_E,'ro')
	mpl.plot(eps_y-eps_0,sig_y,'go')
	mpl.plot(0,0,'ko')

	#mpl.show()

if saveToFile==True:
	file.close()
else:
	print "'yield.csv' already exists! Data not saved!"

# Change the default legend font size
mpl.matplotlib.rcParams['legend.fontsize']=8
	
mpl.figure(1)
mpl.xlabel("Strain [%]")
mpl.ylabel("Stress [N/m^2]")
mpl.legend(loc="upper left")
mpl.ylim(0,8e+6)
mpl.xlim(-1,5)

mpl.figure(2)
mpl.xlabel("Strain [%]")
mpl.ylabel("Stress [N/m^2]")
mpl.legend(loc="upper left")
mpl.ylim(0,1000/sampleArea)
mpl.xlim(-1,20)
mpl.gca().set_color_cycle([mpl.cm.spectral(i) for i in numpy.linspace(0, 0.9, len(fnList))])


mpl.show()

