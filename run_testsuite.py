import sys
from os import path
import unittest
sys.path.append(path.join(path.dirname(sys.argv[0]), "testsuite"))
import test_masterdata
import test_deformdata
import test_stdic
		
if __name__=="__main__":
	masterdata_suite	= unittest.defaultTestLoader.loadTestsFromModule(test_masterdata)
	unittest.TextTestRunner().run(masterdata_suite)
	
	deformdata_suite	= unittest.defaultTestLoader.loadTestsFromModule(test_deformdata)
	unittest.TextTestRunner().run(deformdata_suite)

	stdic_suite			= unittest.defaultTestLoader.loadTestsFromModule(test_stdic)
	unittest.TextTestRunner().run(stdic_suite)
