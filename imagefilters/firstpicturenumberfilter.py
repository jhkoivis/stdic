
from imagefilter import ImageFilter

class FirstPictureNumberFilter(ImageFilter):
    
    def __init__(self, picturenumber = 0):
        self.picturenumber = picturenumber
        
    def filter(self, image):
        if image.picturenumber >= self.picturenumber:
            return True
        return False