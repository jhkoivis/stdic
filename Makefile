


all:
	@echo "Usage (choose your system):"
	@echo "      32-bit, python 2.4:      make -f Makefile32"
	@echo "      64-bit, python 2.4:      make -f Makefile64"
	@echo "      32-bit, python 2.6:      make -f Makefile32-python26"
	@echo "      64-bit, python 2.6:      make -f Makefile64-python26"                   
 
clean:
	rm -f *.pyc
	rm -f */*.pyc
	rm -f *.o
	rm -f *.so


tests:: shortTests longTests

shortTests:
	python run_globtests.py test_configparser.py
	python run_globtests.py test_dffexporter.py
	python run_globtests.py test_diccore.py
	python run_globtests.py test_expressionfolder.py
	python run_globtests.py test_folderanalyzer.py
	python run_globtests.py test_imagefilters.py
	python run_globtests.py test_imagelist.py
	python run_globtests.py test_imageobject.py
	python run_globtests.py test_imageorderers.py
	python run_globtests.py test_masterdata.py
	python run_globtests.py test_pairiterator.py
	python run_globtests.py test_sequencefilters.py
	python run_globtests.py test_stdic.py

longTests:
	python run_globtests.py test_deformdata.py
	python run_globtests.py test_transforms/test*








	
