from glob import glob
from os import path
import re
from itertools import izip

class ExpressionFolder:
    
    def __init__(self, folder):
        self.folder = folder
        self.filelist = []
        
    def findWithExpression(self, regexpression):
        
        filelist = glob(path.join(self.folder, '*'))
        
        filenamelist = map(path.basename, filelist)
        
        pattern = re.compile(regexpression)
        
        for itemname, item in izip(filenamelist,filelist):
            if pattern.match(itemname) != None:
                self.filelist.append(item)
                
    def __iter__(self):
        self._filelistIterator = iter(self.filelist)
        return self
    
    def next(self):
        return self._filelistIterator.next()