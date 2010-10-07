from glob import glob
from os import path
import re

class ExpressionFolder:
    
    def __init__(self, folder):
        self.folder = folder
        self.fileNameList = []
        self.fileList = []
        
    def findWithExpression(self, regexpression):
        
        filelist = glob(path.join(self.folder, '*'))
        
        filenamelist = map(path.basename, filelist)
        
        pattern = re.compile(regexpression)
        
        for item in filenamelist:
            if pattern.match(item) != None:
                self.fileNameList.append(item)
                self.fileList.append(path.join(self.folder,item))

    def getFileNames(self):
        
        return self.fileNameList
    
    def getFiles(self):
        
        return self.fileList