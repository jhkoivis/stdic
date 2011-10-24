

from glob import glob
import os

#dffFolder = '/work/jko/angleCompression/IB7-1-R41-201106071247/cropped/dff/'
dffFolder = '/work/jko/angleCompression/Matleenan_dfft/IB7-1-R41-201106071247_skip_9/crop_IB7-1-R41-201106071247_dff'

jpgFolder = dffFolder + '/../jpg' 

try:
    os.makedirs(jpgFolder)
except OSError:
    pass

for fn in glob(dffFolder + '/*.dff'):
    fn = os.path.basename(fn)
    print 'python plotdff.py %s/%s %s/%s.png %s/%s.dat' % (dffFolder, fn, jpgFolder,fn, jpgFolder, fn) 
