from glob import glob
from os import path
import re

class ImageFolder:
    
    def __init__(self, folder):
        self.folder = folder
        self.imageNameList = []
        self.imageFileList = []
        
    def findImagesExpression(self, regexpression):
        
        filelist = glob(path.join(self.folder, '*'))
        
        filenamelist = map(path.basename, filelist)
        
        pattern = re.compile(regexpression)
        
        for item in filenamelist:
            if pattern.match(item) != None:
                self.imageNameList.append(item)
                self.imageFileList.append(path.join(self.folder,item))

    def getImageNames(self):
        
        return self.imageNameList
    
    def getImageFiles(self):
        
        return self.imageFileList