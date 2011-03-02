
class ImageFilter:
    
    pass

class TrueFilter:
    
    def filter(self, image):
        return True

class ImageFilterFactory:
   
    def __init__(self):
    
        from picturenumberfilter import PictureNumberFilter
    
        self.imageFilterDictionary = dict({
                                           "True":TrueFilter,
                                           "PictureNumber":PictureNumberFilter
                                           })
        
    def getImageFilters(self, configurationdict):
        filters = []
        for key, value in configurationdict.items():
            filters.append(self.imageFilterDictionary[key](value))
        return filters