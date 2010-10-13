from sequencefilters.sequencefilter import *
from imagefilters.imagefilter import *
from imageobject import *
from expressionfolder import ExpressionFolder

class ImageList:
    
    def __init__(self, folderobject, seqFilter,  imgFilters, imageClass, regExpression=None):
        unorderedList = self._getFilteredFolder(folderobject, imgFilters, imageClass, regExpression)
        self.imagelist = seqFilter.filter(unorderedList)
        
    def _getFilteredFolder(self, folderobject, imgFilters, imageClass, regExpression=None):
                
        imagelist = []
        for filename in folderobject:
            imageObject = imageClass(filename, regExpression)
            for imageFilter in imgFilters:
                if not imageFilter.filter(imageObject):
                    break
                    continue
            imagelist.append(imageObject)
        return imagelist
            
    def next(self):
        return self.imageiterator.next()
    
    def __iter__(self):
        self.imageiterator = iter(self.imagelist)
        return self
