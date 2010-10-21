
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
        
    def getImageFilters(self, configobject):
        filterconfigs = configobject.getSubs()
        filters = []
        filters.append(self.imageFilterDictionary["True"]())
        for filterconfig in filterconfigs.values():
            configdict = filterconfig.getValues()
            filtername = configdict.pop('name')
            filters.append(self.imageFilterDictionary[filtername](configdict))
        return filters