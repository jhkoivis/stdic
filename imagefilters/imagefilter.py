
class ImageFilter:
    
    pass


class ImageFilterFactory:
   
    def __init__(self):
    
        from firstpicturenumberfilter import FirstPictureNumberFilter
    
        self.imageFilterDictionary = dict({
                                       "FirstPictureNumber":FirstPictureNumberFilter
                                      
                                      })
        
    def getImageFilters(self, configuration_dict):
        keys = configuration_dict.keys()
        filters = []
        for key in keys:
            filters.append(self.imageFilterDictionary[key](configuration_dict[key]))
        return filters