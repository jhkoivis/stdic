
class ImageFilterFactory:
    
    def __init__(self):
        self.imageFilterDictionary = dict({
                                     "FirstPictureNumber":FirstPictureNumberFilter,
                                     "LastPictureNumber":LastPictureNumberFilter,
                                     "FirstPictureOrdinal":FirstPictureOrdinalFilter,
                                     "LastPictureOrdinal":LastPictureOrdinalFilter
                                     })

    def getImageFilters(self, configuration):
        keys = set(configuration.keys())
        filters = []
        for key in keys:
            filters.append(self.imageFilterDictionary[key](configuration[key]))
        return filters

class ImageFilter:
    
    def __init__(self):
        pass
    
class FirstPictureNumberFilter(ImageFilter):
    
    def __init__(self, configuration):
        pass
    
class LastPictureNumberFilter(ImageFilter):
    
    def __init__(self, configuration):
        pass
    
class FirstPictureOrdinalFilter(ImageFilter):
    
    def __init__(self, configuration):
        pass
    
class LastPictureOrdinalFilter(ImageFilter):
    
    def __init__(self, configuration):
        pass