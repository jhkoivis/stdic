
class ImageOrdererFactory:
    
    def __init__(self):
        self.imageOrdererCollection = dict({
                                            "ordering":"class"
                                            })
    
    def getImageOrderer(self, ordering, configuration=None):
        
        return self.imageOrdererCollection[ordering](configuration)
    
class ImageOrderer:
    
    def __init__(self):
        pass
    
class PictureNumberOrdering(ImageOrderer):
    
    def __init__(self):
        pass
    
    