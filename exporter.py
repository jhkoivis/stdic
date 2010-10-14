

class Exporter:
	""" abstract base class for deformation data exporters """
	
	def export(self):
		if not self.initialize():
			return False
		self.writeVersion()
		self.writeMetadata()
		self.writeDeformationData()
		return self.finalize()
		