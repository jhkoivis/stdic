#!/usr/bin/python
import glob, trace, unittest, sys

modules = map(trace.fullmodname, glob.glob(sys.argv[1]))
suite = unittest.TestLoader().loadTestsFromNames(modules)

unittest.TextTestRunner().run(suite)
