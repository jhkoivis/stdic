# Makefile to create BIGsplines extension module for NumericPython
#
# Jan Kybic, August 2000
# $Id: Makefile,v 1.1 2004/06/11 14:28:25 jko Exp $
#
# Edited by Simo Tuomisto, 2010

PREFIX=/usr
LBITS=$(shell getconf LONG_BIT)

ifeq ($(LBITS),32)
LIBDIR=$(PREFIX)/lib
else
LIBDIR=$(PREFIX)/lib64
endif

INCLUDEDIR=$(PREFIX)/include

PYTHONVERSION=$(shell python -c "import sys; print sys.version[0:3]")

PYTHONINCLUDE=$(INCLUDEDIR)/python$(PYTHONVERSION)
PYTHONLIBRARY=$(LIBDIR)/python$(PYTHONVERSION)
ifeq ($(PYTHONVERSION), 2.4)
NUMPYINCLUDE=$(PYTHONLIBRARY)/site-packages/numpy/core/include/numpy
else
NUMPYINCLUDE=$(PYTHONLIBRARY)/dist-packages/numpy/core/include/numpy
endif
INCLUDES=-I$(PYTHONINCLUDE) -I$(NUMPYINCLUDE)
LDFLAGS=-lm
LD=ld -G
CFLAGS=-Wall -fPIC -O2 $(INCLUDES) -DBIGSPLINES
CC=gcc

VPATH=lib/src
OBJECTS=BIGsplines.o fiir.o splninterp.o bsplneval.o ffir.o bigsdcgr.o

# generic compile rule
.c.o:	$(HEADERS)	
	$(CC) -c $(CFLAGS) $^ -o $(VPATH)/$@

all: BIGsplines.so

BIGsplines.so: $(OBJECTS)
	$(LD) $^ $(LDFLAGS) -o lib/dic/BIGsplines.so

clean:
	rm $(VPATH)/*.o lib/dic/BIGsplines.so
