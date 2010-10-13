


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
