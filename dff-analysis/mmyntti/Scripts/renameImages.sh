#!/bin/sh

# This script transforms the commas in the picture file names into dots.
# The camera computer may use commas instead of dots as decimal separators 
# when saving pictures, and it may confuse later the other programs. This
# script assumes that the picture files are in .tiff format.
#
# Before using, run this program like this! If the output looks right,
# remove first "echo" words from lines 16 and 17. After this, the
# script actually works.

for file in `find * | grep tiff`; do
# Gathers the pictures, they are in .tiff format.

	newFile=`echo $file | sed -e 's/,/./g'`
	# Creating the new file name

	echo mv $file $newFile 
	echo echo mv $file $newFile 
	# Actual replacing. 
done
