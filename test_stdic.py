
import unittest
import stdic
import glob
from os import path
import time

class CreepExperimentTest(unittest.TestCase):

	showtimes		= False

	folder			= path.join("testsuite","test2")
	config			= path.join(folder,"test2.dicconf")

	def testCreepExperiment(self):
		
		deformation = self.getDffDeformation(self.folder, self.config)
		self.assertAlmostEqual(deformation, 180.944640, 4)
		
	def getDffDeformation(self, folder, config):
		time1 = time.clock()
		experiment = stdic.CreepExperiment(folder,folder, config)
		time2 = time.clock()
		timetaken = time2 - time1
		if self.showtimes:
			print "Time taken: %s seconds." % timetaken
		dffFilename	= glob.glob(path.join(folder,"*.dff"))[0]
		dffFile 	= open(dffFilename,'r')
		for line in dffFile:
			linesplit = line.split()
			if len(linesplit) == 0:
				continue
			if linesplit[0] != '%':
				if int(linesplit[0]) == 10 and int(linesplit[1]) == 180:
					return float(linesplit[3])
