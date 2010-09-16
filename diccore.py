#!/usr/bin/python
"""

	Erkka Valo, September 2005

	Rewrite Simo Tuomisto, 2010

"""

import bigtools
import bigfelreg
import bigoptimize

#------------------------------------------------------------------------------


def dic(firstImg, secondImg, parameters, crop=None):

	# Returns the deformation from the firsImg to secondImg.
	try:
		if crop == None:
			firstImg = bigtools.ImageToArray(firstImg)
			secondImg = bigtools.ImageToArray(secondImg)
		else:
			firstImg = bigtools.ImageToArrayWithCrop(firstImg, crop)
			secondImg = bigtools.ImageToArrayWithCrop(secondImg, crop)
	except:
		raise Exception("Could not read images.")

	par=bigtools.Parameters(parameters, override={'refimg':firstImg,
											'testimg':secondImg})

	warpingProblem = bigfelreg.MultigridableWarpingProblemBase(par=par)
	mrs = bigoptimize.MROptimizerState(warpingProblem, par=par)
	mrs.solveMR()
	defFunction = mrs.getProblem().datapart.testw

	return defFunction
