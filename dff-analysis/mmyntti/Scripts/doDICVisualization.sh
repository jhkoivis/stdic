#!/bin/sh

# This script runs the followinf scripts for .dff files it finds.

for file in `find * | sed '/crop.*dff.*dff.*dff/!d'`; do
	python fitMeanStrain.py $file; 
	python display_dff_6.0.py $file; 
	python shearingMap_1.0.py $file; 
	python uyData.py $file;
done
