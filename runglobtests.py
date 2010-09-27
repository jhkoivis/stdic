import glob, trace, unittest, sys

""" argv[1] is globbing. runs tests matching to the glob (aka sh wildcards) """

if __name__=="__main__":
	modules = map(trace.fullmodname, glob.glob(sys.argv[1]))
	suite = unittest.TestLoader().loadTestsFromNames(modules)
	unittest.TextTestRunner().run(suite)
