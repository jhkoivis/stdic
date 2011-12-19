from imageclick import ImageClick
from glob import glob

#fn = '/work/jko/DIC-predict/emma/09021604/09021604-0000000001-2673-0000-499718-8bit.tiff'

#fn = '/work/jko/DIC-predict/jvi/05061309/20050613-9-2-3098-8bit-0000-3124741.tiff'

#folderName = '/work/jko/DIC-predict/jvi/05072603'

folderName = '/work/jko/lyon/exp405_small'


fnList = glob(folderName + '/*')
fnList.sort()
fn = fnList[0]
for fn in fnList[::10]:
    ic = ImageClick(fn)
    ic.main()



