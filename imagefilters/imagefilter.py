
class ImageFilter:
    
    pass

class TrueFilter:
    
    def filter(self, image):
        return True

class ImageFilterFactory:
   
    def __init__(self):
    
        from firstpicturenumberfilter import FirstPictureNumberFilter
    
        self.imageFilterDictionary = dict({
                                           "True":TrueFilter,
                                           "FirstPictureNumber":FirstPictureNumberFilter
                                      
                                           })
        
    def getImageFilters(self, configuration_dict):
        keys = configuration_dict.keys()
        filters = []
        filters.append(self.imageFilterDictionary["True"]())
        for key in keys:
            filters.append(self.imageFilterDictionary[key](configuration_dict[key]))
        return filters