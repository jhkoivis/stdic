from os import path

class PictureNumberDffname:

	def __init__(self, folder):
		self.string = path.join(folder,"dff-%s-%s.dff")
	
	def generatename(self, image1, image2):
		return self.string % (image1.picturenumber, image2.picturenumber)
	
class CheckDffExistence:
		
	def checkExistence(self, dffname):
		if os.exists(name):
			return True
		return False