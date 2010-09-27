import glob, trace, unittest, sys

""" argv[1:] is globbing. runs tests matching to the glob (aka sh wildcards) """

if __name__=="__main__":
	for g in sys.argv[1:]:
		modules = map(trace.fullmodname, glob.glob(g))
		suite = unittest.TestLoader().loadTestsFromNames(modules)
		unittest.TextTestRunner().run(suite)
