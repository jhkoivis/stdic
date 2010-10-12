
class ImageFilter:
    
    def __init__(self):
        pass

from firstpicturenumberfilter import *

class ImageFilterFactory:
    
    def __init__(self):
        self.imageFilterDictionary = ["FirstPictureNumber",FirstPictureNumberFilter]
        
    def getImageFilters(self, configuration_dict):
        keys = configuration_dict.keys()
        filters = []
        for imageFilter in imageFilterClasses:
            if imageFilter.parameterKey in configuration_dict:
                filters.append(imageFilter(imageFilter.parameterKey))
        return filters