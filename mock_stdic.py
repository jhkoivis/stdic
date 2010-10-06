
from expressionfolder import ExpressionFolder
from imageorderer import *
from filefilter import *

class mock_stdic:
    
    def __init__(self, folder, regexp, filter_properties):
        
        folder_object = ExpressionFolder(folder)
        folder_object.findWithExpression(regexp)
        
        orderfactory = ImageOrdererFactory()
        order = ImageOrdererFactory().getImageOrderer(parameter)
        
        filterfactory = FileFilterFactory()
        filters = FileFilterFactory().getFileFilters(parameter)

        imageList = ImageList(folder_object, order, filters)
        
        pairIterator = PairIterator(ImageList)
        
        exporter = DffExporter()
        
        for pair in pairIterator:
            
            deformation = dic.analyze(pair)
            exporter(pair.getData(), deformation)