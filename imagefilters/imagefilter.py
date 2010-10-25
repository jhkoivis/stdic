
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
        
    def getImageFilters(self, configobject):
        filterconfigs = configobject.getSubs()
        filters = []
        filters.append(self.imageFilterDictionary["True"]())
        for filterconfig in filterconfigs.values():
            configdict = filterconfig.getValues()
            filtername = configdict.pop('name')
            filters.append(self.imageFilterDictionary[filtername](configdict))
        return filters