
from imagefilter import ImageFilter

class FirstPictureNumberFilter(ImageFilter):
    
    def __init__(self, pictureNumber):
        self.pictureNumber = pictureNumber
        
    def filter(self, image):
        if image.picturenumber >= self.pictureNumber:
            return True
        return False