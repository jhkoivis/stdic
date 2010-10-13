
from expressionfolder import ExpressionFolder
from pairiterator import *
from imageorderer import *
from imagefilter import *
from sequencefilter import *

class mock_stdic:
    
    def __init__(self, folder, configurationfile):
        
        configuration = ParseConfig(configurationfile)
        
        filtconfig  = configuration.filter_configuration
        orderconfig = configuration.order_configuration
        seqconfig   = configuration.sequence_configuration
        regexp      = configuration.regular_expression
        
        folder_object = ExpressionFolder(folder)
        folder_object.findWithExpression(regexp)

        imagefilters = ImageFilterFactory().getImageFilters(filtconfig)
        
        orderer = ImageOrdererFactory().getImageOrderer(orderconfig)
        
        sequencefilter = SequenceFilterFactory().getSequenceFilter(seqconfig)
        
        imagelist = ImageList(folder_object, sequencefilter, imagefilters)
        
        pairIterator = PairIterator(imagelist)
        
        exporter = DffExporter()
        
        for pair in pairIterator:
            
            deformation = dic.analyze(pair)
            exporter(pair.getData(), deformation)