from imageorder import ImageOrder
    
class PictureNumberOrder(ImageOrder):
    
    def __init__(self):
        ImageOrder.__init__(self)
        
    def _compare(self, image1, image2):
        
        if image1.picturenumber < image2.picturenumber:
            return -1
        elif image1.picturenumber > image2.picturenumber:
            return 1
        
        return 0
    
    def order(self, imagelist):
        return ImageOrder._order(self, imagelist, self._compare)
        