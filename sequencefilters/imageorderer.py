
class ImageOrdererFactory:
    
    def __init__(self):
        self.imageOrdererDictionary = dict({
                                            "PictureNumber":PictureNumberOrdering
                                            })
    
    def getImageOrderer(self, ordering, configuration=None):
        
        return self.imageOrdererDictionary[ordering](configuration)
    
class ImageOrderer:
    
    def __init__(self):
        pass
    
class PictureNumberOrdering(ImageOrderer):
    
    def __init__(self):
        pass
    
    def order(self, image1, image2):
        if image1.PictureNumber < image2.PictureNumber:
            return -1
        elif image1.PictureNumber > image2.PictureNumber:
            return 1
        
        return 0
        
    
    