
from imageobject import ImageObject
import copy

class ImageList:
    
    def __init__(self, folderobject, seqFilter,  imgFilters, regExpression=None):
        # unordered list is static containing all images! do not modify!
        self.unorderedList = self._getFilteredFolder(folderobject, 
                                                     imgFilters, 
                                                     regExpression)
        
        self.imagelist = seqFilter.filter(copy.copy(self.unorderedList))
        
    def _getFilteredFolder(self, folderobject, imgFilters, regExpression=None):
                
        imagelist = []
        for filename in folderobject:
            imageObject = ImageObject(filename, regExpression)
            appendBoolean = True
            for imageFilter in imgFilters:
                if not imageFilter.filter(imageObject):
                    appendBoolean = False
                    break
            if appendBoolean:
                imagelist.append(imageObject)
        return imagelist
    
    def get_list_of_all_images_in_folder(self):
        return self.unorderedList
            
    def next(self):
        return self.imageiterator.next()
    
    def __iter__(self):
        return iter(self.imagelist)
