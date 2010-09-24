#!/usr/bin/python
import glob, trace, unittest, sys

# find all of the planet test modules
modules = map(trace.fullmodname, glob.glob(sys.argv[1]))

# load all of the tests into a suite
suite = unittest.TestLoader().loadTestsFromNames(modules)

# run test suite
unittest.TextTestRunner().run(suite)
