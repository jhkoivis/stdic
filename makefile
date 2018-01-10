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
ALTNUMPYINCLUDE=/usr/lib/pymodules/python2.7/numpy/core/include/numpy/
UBUNTUINCLUDE=/usr/lib/python2.7/dist-packages/numpy/core/include/numpy/

INCLUDES=-I$(PYTHONINCLUDE) -I$(NUMPYINCLUDE) -I$(ALTNUMPYINCLUDE) -I$(UBUNTUINCLUDE)
LDFLAGS=-lm -L/usr/lib/python2.7/config-x86_64-linux-gnu/ -lpython2.7
#LD=ld -G
LD=gcc -Wl,-undefined,dynamic_lookup -shared #ld -G
CFLAGS=-Wall -fPIC -O2 $(INCLUDES) -DBIGSPLINES
CC=gcc

vpath %.c src
vpath %.o src
vpath %.so lib/dic
SOURCES=BIGsplines.c fiir.c splninterp.c bsplneval.c ffir.c bigsdcgr.c
OBJECTS=$(addprefix src/,$(SOURCES:.c=.o))

#############################
# osx compilation
ISDARWIN=$(shell uname)
ifeq ($(ISDARWIN), Darwin)
OSXPREFIX=/Developer/SDKs/MacOSX10.6.sdk/System/Library/Frameworks/Python.framework/Versions/2.6/
INCLUDE1=$(OSXPREFIX)/Extras/lib/python/numpy/core/include/numpy/
INCLUDE2=$(OSXPREFIX)/include/python2.6/
INCLUDES=-I $(INCLUDE1) -I $(INCLUDE2)
CFLAGS=-Wall -fPIC -O2 $(INCLUDES) -DBIGSPLINES -DDARWIN
LD=gcc -Wl,-undefined,dynamic_lookup
endif
############################


# generic compile rule
.c.o:	$(HEADERS)	
	$(CC) -c $(CFLAGS) $^ -o $@

all: BIGsplines.so

BIGsplines.so: $(OBJECTS)
	$(LD) $^ $(LDFLAGS) -o lib/dic/BIGsplines.so

clean:
	rm $(OBJECTS) lib/dic/BIGsplines.so

info:
	echo $(ISDARWIN) 
