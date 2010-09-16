#!/usr/bin/python
"""

	Simo Tuomisto, 2010

"""

import sys
import os
import re
import deformdata
import masterdata
import time
from numpy import save as npsave

#------------------------------------------------------------------------------

class CreepExperiment:

	def __init__(self, pathname, dffpath, configfile):

		if not os.path.exists(pathname):
			raise Exception("Invalid path: " + pathname)
		if not os.path.exists(dffpath):
			os.mkdir(dffpath)
		self.masterdata = masterdata.MasterData(configfile)
		self.set('Pathname', pathname)
		self.set('DffPathname', dffpath)
		if self.check('Verbose'):
			self.verbose = self.get('Verbose')
		else:
			self.verbose = 3
		self.analyzePictures()

	def analyzePictures(self):
		
		pathname = self.get('Pathname')
		
		if self.verbose > 2:
			print "Searching path: " + pathname
			
		pathsplit = os.path.split(pathname)
		
		if len(pathsplit[1]) == 0:
			pathsplit = os.path.split(pathsplit[0])
		
		self.set('Name', pathsplit[1])
		
		self.set('Pictures', self.sortPictures(pathname))

		if self.verbose > 0:
			print "Starting registeration..."

		analyzesDone	= 0
		analyzesSkipped	= 0
		analyzesLeft	= len(self.get('Pictures'))-1
		
		analyzesMaxExists = self.check('AnalyzesMax')
		
		if analyzesMaxExists:
			analyzesMax = self.get('AnalyzesMax')
			if analyzesMax < analyzesLeft:
				analyzesLeft = analyzesMax
		
		writeCoefs = False
		
		if self.check('WriteCoefs'):
			if self.get('WriteCoefs') == 'True':
				writeCoefs = True
		
		timetaken		= 0
		totaltimetaken	= 0

		pictures	= self.get('Pictures')
		
		try:
			analyzeTo = self.get('AnalyzeTo')
		except KeyError:
			raise KeyError("[stdic.py]:AnalyzeTo must be defined.")

		try:
			overwrite = self.get('OverwriteDffs')
		except KeyError:
			raise KeyError("[stdic.py]:OverwriteDffs must be defined.")

		analysispicture = pictures[0]
		
		if self.get("Analyze") == 'True':
			for picture in pictures:
				if picture != analysispicture:
					filename = os.path.join(self.get('DffPathname'),"%s-%s-%s" % (self.get('Name'), analysispicture[0], picture[0]))
					dffname = filename + ".dff"
					if not os.path.exists(dffname) or overwrite == "True":
				
						if self.verbose > 1:
							print "Registrations left: " + str(analyzesLeft)
							if self.verbose > 3:
								print "Registering deformation from picture " + str(analysispicture[0]) + " to picture " + str(picture[0])

						time1 = time.clock()
						deformation = deformdata.DeformationData(analysispicture[1], picture[1], self.get('ConfigFile'))
						time2 = time.clock()
						timetaken = time2 - time1
						totaltimetaken += timetaken
						if self.verbose > 1:
							print "Registration took: " + str(timetaken) + " seconds."

						deformation.set('PictureData1', analysispicture[2])
						deformation.set('PictureData2', picture[2])
						self.writeDff(deformation, dffname)
						if writeCoefs:
							self.writeCoefs(deformation, filename)

					elif self.verbose > 1:
						print "Dff %s exists. Will not overwrite." % dffname
						analyzesSkipped += 1
					
					analyzesDone += 1
					analyzesLeft -= 1

					if analyzesMaxExists:
						if analyzesDone == analyzesMax:
							if self.verbose > 1:
								print "Maximum number of analyzes done."
							break

					try:
						if self.verbose > 1:
							print "Time left: " + str("%d" % (analyzesLeft * totaltimetaken/(analyzesDone-analyzesSkipped))) + " seconds."
					except ZeroDivisionError:
						pass
				
					if analyzeTo == "Previous":
						analysispicture = picture
						
		elif self.verbose > 0:
			print "Analysis skipped."
				
		if self.verbose > 0:	
			print "Registration done."
			
	def get(self, key):

		# Get's data from masterdata dictionary.

		return self.masterdata.get(key)

	def set(self, key, value):

		# Put's data to masterdata dictionary.

		self.masterdata.set(key, value)

	def check(self, key):

		return self.masterdata.check(key)

	def sortPictures(self, pathname):

		"""
		Seeks for pictures that match the format and arranges them.
		Returns an array that has a three-cell array in every cell.
		The first cell has the picture's number, the second has it's
		name with path included and the third has a dictionary formed 
		from the regular expression keywords that user supplies
		with PictureForm.
		
		Configuration flags:
		
		PictureForm regular expression is required so that the program
		can find the pictures. All other data can be <ignore>'d but
		PictureNumber is essential and must be present. Rest of the
		keywords (<key>) are user definable and show up only at the
		dff-file.
		
		If AnalyzeTo-flag is a picture's name the program takes
		only the pictures following that picture.
		
		Same if FirstPicture is defined. If FirstPicture is a picture
		taken before analysispicture, no pictures are found.
		
		If LastPicture is defined the program will ignore pictures
		taken after that.
		
		If PictureSkip's name is self-explanatory. LastPicture will
		always be the last picture, even if it isn't a skip:th
		picture.
		"""
		
		files = os.listdir(pathname)
		files.sort()

		pictures = []

		try:
			analyzeTo = self.get('AnalyzeTo')
		except KeyError:
			raise KeyError("[stdic.py]:AnalyzeTo must be defined.")
		
		findanalysispicture = (analyzeTo != "First" and analyzeTo != "Previous")
		if findanalysispicture:
			analysispicture = analyzeTo
		else:
			analysispicture = None

		findfirstpicture = self.check('FirstPicture')
		if findfirstpicture:
			firstpicture = self.get('FirstPicture')

		findlastpicture	= self.check('LastPicture')
		if findlastpicture:
			lastpicture = self.get('LastPicture')
			
		try:
			testExpression = re.compile(self.get('PictureForm'))
		except KeyError:
			raise KeyError("[stdic.py]:PictureForm must be defined.")
			
		if 'PictureNumber' not in testExpression.groupindex:
			raise Exception("No PictureNumber key in the picture name expression.")
		for possiblePicture in files:
			if possiblePicture == analysispicture:
				findanalysispicture = False
				pictureMatch = testExpression.match(possiblePicture, 0, len(possiblePicture))
				if pictureMatch != None:
					analysispicture = [int(pictureMatch.group('PictureNumber')), os.path.join(pathname,possiblePicture), pictureMatch.groupdict()]
			if not findanalysispicture:
				if (not findfirstpicture) or possiblePicture == firstpicture:
					findfirstpicture = False
					pictureMatch = testExpression.match(possiblePicture, 0, len(possiblePicture))
					if pictureMatch != None:
						pictures.append([int(pictureMatch.group('PictureNumber')), os.path.join(pathname,possiblePicture), pictureMatch.groupdict()])
					elif self.verbose > 4:
						print "Picture filename '" + possiblePicture + "' is in wrong format."
					if findlastpicture:
						if possiblePicture == lastpicture:
							break

		pictures.sort()
		if self.verbose > 2:
			print "Found " + str(len(pictures)) + " pictures."
		chosenPictures = []

		if analysispicture != None:
			chosenPictures.append(analysispicture)

		if self.check('PictureSkip') == 'True':
			skip = self.get('PictureSkip')
		else:
			skip = 0
		multiplier = 0
		index = 0

		if skip == 0 or skip == 1:
			if self.verbose > 2:
				print "Taking every picture."
			chosenPictures.extend(pictures)
		else:
			if self.verbose > 2:
				print "Taking every " + str(skip) + ":th picture."
			while index < len(pictures):
				chosenPictures.append(pictures[index])
				multiplier += 1
				index = multiplier * skip

		if findlastpicture:
			if chosenPictures[len(chosenPictures) -1][0] != pictures[len(pictures) - 1][0]:
				chosenPictures.append(pictures[len(pictures) - 1])
	
		if len(chosenPictures) < 2:
			raise Exception("Could not get two images from directory %s." % pathname)

		if self.verbose > 2:
			print str(len(chosenPictures)) + " pictures to be analyzed."

		return chosenPictures

	def writeDff(self, deformation, filename):
		
		# Writes .dff-files for every deformation analysis.

		outputfile		= open(filename, 'w')
		picturedata1	= deformation.get("PictureData1")
		picturedata2	= deformation.get("PictureData2")
		parameters		= deformation.get("Parameters")

		outputfile.write("%% picture1 filename: %s\n" % deformation.get("FirstPictureName"))
		for key in picturedata1:
			outputfile.write("%% picture2 %s: %s\n" % (key, picturedata1[key]))
		outputfile.write("\n")

		outputfile.write("%% picture2 filename: %s\n" % deformation.get("SecondPictureName"))
		for key in picturedata2:
			outputfile.write("%% picture2 %s: %s\n" % (key, picturedata2[key]))
		outputfile.write("\n")
		
		outputfile.write("% analysis parameters:\n")
		for key in parameters:
			outputfile.write("%% %s: %s\n" % (key, str(parameters[key])))
		outputfile.write("\n")
	
		crop = deformation.get("Crop")
		size = deformation.get("PictureSize")

		outputfile.write("%% picture size x: %d\n" % size[0])
		outputfile.write("%% picture size y: %d\n" % size[1])
		outputfile.write("%% crop start   x: %d\n" % crop[0])
		outputfile.write("%% crop end     x: %d\n" % crop[1])
		outputfile.write("%% crop start   y: %d\n" % crop[2])
		outputfile.write("%% crop end     y: %d\n" % crop[3])
		outputfile.write("\n")

		try:
			step = self.get("DffStep")
		except KeyError:
			raise KeyError("[stdic.py]:DffStep must be defined.")
		pointarray = []
		rangex = xrange(0, crop[1] - crop[0], step)
		rangey = xrange(0, crop[3] - crop[2], step)
		for x in rangex:
			for y in rangey:
				pointarray.append([x,y])
		deformedpointarray = deformation.getDeformationAtPoints(pointarray)
		for index in xrange(0, len(pointarray)):
			x = pointarray[index][0]
			y = pointarray[index][1]
			xd = deformedpointarray[index][0]
			yd = deformedpointarray[index][1]
			outputfile.write("%d %d %lf %lf \n" % (x, y, xd, yd))
		outputfile.close()

	def writeCoefs(self, deformation, filename):
		
		coefsArray = deformation.getCoefs()
		npsave(filename,coefsArray)
		
#------------------------------------------------------------------------------

if __name__ == "__main__":

	register(CreepExperiment(*sys.argv[1:]))
	
#------------------------------------------------------------------------------
