
class FileFilterFactory:
    
    def __init__(self):
        self.fileFilterCollection = [
                                     (set(["FirstPictureNumber"]), FirstPictureNumberFilter),
                                     (set(["LastPictureNumber"]), LastPictureNumberFilter),
                                     (set(["FirstPictureOrdinal"]), FirstPictureOrdinalFilter),
                                     (set(["LastPictureOrdinal"]), LastPictureOrdinalFilter)
                                     ]

    def getFileFilters(self, properties):
        filters = []
        for fileFilter in self.fileFilterCollection:
            if (fileFilter[0] & properties) == fileFilter[0]:
                filters.append(fileFilter[1])
        return filters
        

class FileFilter:
    
    def __init__(self):
        pass
    
class FirstPictureFilter(FileFilter):
    
    def __init__(self, filenumber):
        pass
    
    def filterFiles(self, filelist):
        pass