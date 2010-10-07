from PIL import Image
import re
from os import path

class ImageObject:
    
    def __init__(self, filename, regexpression=None):
        
        self.filename = filename
        self.imagedata = dict({"Filename":filename})
        if regexpression != None:
            pattern = re.compile(regexpression)
            basename = path.basename(filename)
            matchdictionary = pattern.match(basename).groupdict()
            self.imagedata.update(matchdictionary)
            
    def getImage(self):
        return Image.open(self.filename)
    
    def getImageData(self):
        return self.imagedata
    
    def getImageDataValue(self, key):
        return self.imagedata.get(key, None)