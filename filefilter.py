
class FileFilterFactory:
    
    def __init__(self):
        self.fileFilterDictionary = dict({
                                     "FirstPictureNumber":FirstPictureNumberFilter,
                                     "LastPictureNumber":LastPictureNumberFilter,
                                     "FirstPictureOrdinal":FirstPictureOrdinalFilter,
                                     "LastPictureOrdinal":LastPictureOrdinalFilter
                                     })

    def getFileFilters(self, configuration):
        keys = set(configuration.keys())
        filters = []
        for key in keys:
            filters.append(self.fileFilterDictionary[key](configuration[key]))
        return filters

class FileFilter:
    
    def __init__(self):
        pass
    
class FirstPictureNumberFilter(FileFilter):
    
    def __init__(self, configuration):
        pass
    
class LastPictureNumberFilter(FileFilter):
    
    def __init__(self, configuration):
        pass
    
class FirstPictureOrdinalFilter(FileFilter):
    
    def __init__(self, configuration):
        pass
    
class LastPictureOrdinalFilter(FileFilter):
    
    def __init__(self, configuration):
        pass