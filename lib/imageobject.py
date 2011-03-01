from PIL import Image
import re
from os import path

class ImageObject:
    
    def __init__(self, filename, regexpression=None):
        
        self.filename = filename
        if regexpression != None:
            pattern = re.compile(regexpression)
            basename = path.basename(filename)
            matchdictionary = pattern.match(basename).groupdict()
            for key in matchdictionary:
                setattr(self,key, matchdictionary[key])
            
    def getImage(self):
        return Image.open(self.filename)