import numpy
import pylab
import os
from glob import glob
import matplotlib.pyplot as mpl
from scipy import stats as sp



def monotonize(list):
	for i in range(0,len(list)-1):
		if list[i] > list[i+1]:
			list[i+1] = list[i]

def polylin(data,N):
	coeff  = [numpy.array([])] * N
	bounds = [numpy.array([])] * N
	parts  = [numpy.array([])] * N
	blocklen = int( numpy.ceil( len(data) / N ) )

	for i in numpy.arange(0,N):
		f = i * blocklen             # from
		t = ( i + 1 ) * blocklen -1  # to
		if i < N-1:
			parts[i] = data[f:t, :]
		else:
			parts[i] = data[f:,:]

	for i in numpy.arange(0,N):
	        block = parts[i]
		x = block[:,0]
		y = block[:,1]
		#A = numpy.vstack([x, numpy.ones(len(x))]).T
		#h,w = A.shape
		#a,b = numpy.linalg.lstsq(A,y)[0]
		slope, intercept, r_value, p_value, std_err = sp.linregress(x,y)
		bounds[i] = [ x[1], x[-1] ]
		coeff[i] = [ slope, intercept ]

	return bounds, coeff



pps  = 10 # Points per second for interpolation
lag  = 5*pps # 5*pps is about 1.7% strain
lags = 80*pps # 30*pps is about 10% strain


# Pos. quadrant of (x,y,z)
sampleX = 6.0   # (mm)
sampleY = 12.0
sampleZ = 6.0
sampleArea = sampleX*sampleY/(10**6) # (m^2)

# Read fatigue times for the samples
lines = numpy.loadtxt("dict.csv",dtype="string")
fatigues = {}
for i in range(lines.shape[0]):
	fn=lines[i].split(',')[0]
	fatigue=lines[i].split(',')[1]
	fatigues[fn]=fatigue

# This is the list of files to process
fnList = fatigues.keys()
fnList.sort()

# We don't necessarily want overwrite old results
if os.path.exists('yield.csv'):
	saveToFile = False
else:
	saveToFile = True
	file = open("yield.csv", 'w')

# There was a bug in the labview program saving the TTM data. The data
# was saved partially in engineering units. For this script to work
# after the switch to correct units, we need to read the conversion
# factors necessary for this measurement's data in case the data is
# not in SI units. If conversion.csv exists, it will cotain the
# conversion factors; if not, the data is already in SI units. The
# format of the file is:
# 1st line:f1,f2,f3
# 2nd line:fs1,fs2,fs3
# where values on first line are the engineerin unit conversion
# factors and values on the second line are the full scale constants
if os.path.exists('conversion.csv'):
	lines=numpy.loadtxt('conversion.csv', dtype="string")
	forceFactor = float(lines[1].split(',')[1]) / float(lines[0].split(',')[1])
	dPosFactor  = float(lines[1].split(',')[2]) / float(lines[0].split(',')[2])
else:
	forceFactor = 1
	dPosFactor  = 1000

if not os.path.exists('plots'):
	os.mkdir('plots')


fnnum = 1

for fn in fnList:

	print fn
	
	data = numpy.loadtxt(fn)

	# F -> stress
	data[:,1] = -data[:,1] * forceFactor / sampleArea
	
	# Drop off the points after Fmax
	sig_max_ind = numpy.argmax(data[:,1])
	data = data[:sig_max_ind,:]

	#print "sig_max_ind = %g" % sig_max_ind

	# d -> epsilon
	data[:,2] = -data[:,2]*dPosFactor
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
	der_max_ind = numpy.argmax(mdiff[:int(len(diff)/4)])
	der_max     = diff[der_max_ind]	
	eps_E       = einterp[der_max_ind]
	sig_E       = sinterp[der_max_ind]
	const       = sig_E - der_max*eps_E
	eps_0       = -const/der_max

	#print "der_max_ind = %g" % der_max_ind
	#print "der_max = %g" % der_max
	#print "eps_E = %g" % eps_E
	#print "sig_E = %g" % sig_E
        #print "const = %g" % const
	#print "eps_0 = %g" % eps_0

	# Find the yield point (eps_y, sig_y)
	linapp  = einterp*der_max + const
	yld_ind = (linapp > 1.1*sinterp)
	eps_y = numpy.extract(yld_ind,einterp)[0]
	sig_y = numpy.extract(yld_ind,sinterp)[0]

	#print "eps_y = %g" % eps_y
	#print "sig_y = %g" % sig_y

	# Find slope of the "plateu" part of the curves
	bounds, coeff = polylin( numpy.concatenate( ( numpy.row_stack(einterp-eps_0), numpy.row_stack(sinterp) ), 1), 4)

	#mdiff = ( msinterp[lags:] - msinterp[:-lags] ) / ( einterp[lags:] - einterp[:-lags] )
	#mdiff[1:int( len( mdiff ) / 10 )] = mdiff[numpy.argmax(mdiff)]
	#mdiff[0:lags+1] = der_max # Guaranteed to be larger than the "plateu slope" :)
	#der_min_ind = numpy.argmin(mdiff)
	#der_min     = mdiff[der_min_ind]
	#der_min_eps = einterp[der_min_ind]
	#der_min_sig = sinterp[der_min_ind]

	#print "lags = %d"        % lags
	#print "der_min_ind = %d" % der_min_ind
	#print "der_min = %g"     % der_min
	#print "der_min_eps = %g" % der_min_eps
	#print "der_min_sig = %g" % der_min_sig
				 
	if saveToFile==True:
		# First save "fatigue vs" data
		fat = int(fatigues[fn])
		sf = "%d, %e, %e, %e, %e, %e, %e, %e, %e\n" % (fat, eps_0, eps_E, sig_E, der_max, eps_y, sig_y, coeff[1][0], coeff[2][0])
		sf = fn + ", " + sf
		file.write(sf)
		# Then the interpolated & eps_0 translated data 
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


	# Single curve plots with linear fit overlays
	fig = mpl.figure(fnnum+2)
	fig.clf()
	ax = fig.add_subplot(111)
	
	mpl.plot(einterp-eps_0,sinterp,label=fn)
	fnnum = fnnum + 1
	for i in numpy.arange( 0, len(coeff) ):
		x = numpy.array(bounds[i])
		y = x.copy() * coeff[i][0] + coeff[i][1]
		print "x0 = %g, x1 = %g" % (x[0],x[1])
		print "y0 = %g, y1 = %g" % (y[0],y[1])
		mpl.plot( x, y, 'k-', linewidth=2)
	for i in numpy.arange( 0, len(coeff) ):
		x = numpy.array(bounds[i])
		mpl.plot([x[0],x[0]],[0,1.4*1e7], 'k:')
	mpl.plot([x[1],x[1]],[0,1.4*1e7], 'k:')
	
	# Labels for the plots..
	bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="white", ec="b", lw=2)
	
	textX = ( bounds[1][0] + bounds[1][1] ) / 2
	textY = (textX * coeff[1][0] + coeff[1][1]) + 2.5e6
	t = ax.text(textX, textY, "1", ha="center", va="center", rotation=-90,
            size=15,
            bbox=bbox_props)

	textX = ( bounds[2][0] + bounds[2][1] ) / 2
	textY = (textX * coeff[2][0] + coeff[2][1]) + 2.5e6
	t = ax.text(textX, textY, "2", ha="center", va="center", rotation=-90,
            size=15,
            bbox=bbox_props)

	titlestr = fn.split('-')[1] + " " + fn.split('-')[2].split('.dat')[0] + " fatigue time: " + fatigues[fn] + " s"
	ax.annotate(titlestr, xy=(.5, .975),
		    xycoords='figure fraction',
		    horizontalalignment='center', verticalalignment='top',
		    fontsize=20)

	locs, labels = mpl.yticks([0, 2e+6, 4e+6, 6e+6, 8e+6, 1e+7, 1.2e+7, 1.4e+7],
				  ['0', '2', '4', '6', '8', '10', '12', '14'],
				  fontsize=15)
	locs, labels = mpl.xticks(fontsize=15)

	mpl.xlabel(r'Strain $\epsilon$ [%]', {'color'    : 'k',
					      'fontsize'   : 25 })
	mpl.ylabel(r'Stress $\sigma$ [MPa]', {'color'    : 'k',
						'fontsize'   : 25 })


	# And axis limits
	#ax.set_xlim( -1, einterp[-1] )
	#ax.set_ylim(  0, ( 1000 / sampleArea ) )
	mpl.ylim(0,1.4e7)
	mpl.xlim(numpy.min(einterp-eps_0),numpy.max(einterp-eps_0))
	
	# Save the single-plots
	fname = "plots/%s_stess-strain_with_fits.pdf" % fn.split('.dat')[0]
	mpl.savefig(fname, dpi=300, facecolor='w', edgecolor='w',
		    orientation='portrait', format='pdf',
		    transparent=False, bbox_inches=None, pad_inches=0.1)
	fname = "plots/%s_stess-strain_with_fits.eps" % fn.split('.dat')[0]
	mpl.savefig(fname, dpi=300, facecolor='w', edgecolor='w',
		    orientation='portrait', format='eps',
		    transparent=False, bbox_inches=None, pad_inches=0.1)
	
	#slope_eps = [ einterp[(der_min_ind-2*lags)], einterp[(der_min_ind+2*lags)] ]
	#slope_sig = (slope_eps - der_min_eps)*der_min + der_min_sig
	#mpl.plot( slope_eps-eps_0, slope_sig,'k--',)
	#mpl.plot( der_min_eps-eps_0, der_min_sig, 'ko')
	#mpl.plot(0,0,'k+')

	#mpl.figure(3)
	#mpl.plot(einterp,msinterp)

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
mpl.xlim(-1,15)

mpl.figure(2)
mpl.xlabel("Strain [%]")
mpl.ylabel("Stress [N/m^2]")
mpl.legend(loc="upper left")
mpl.ylim(0,1000/sampleArea)
mpl.xlim(-1,60)
mpl.gca().set_color_cycle([mpl.cm.spectral(i) for i in numpy.linspace(0, 0.9, len(fnList))])


mpl.show()

