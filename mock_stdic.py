
from expressionfolder import ExpressionFolder
from pairiterators.pairiterator import PairIteratorFactory
from imagefilters.imagefilter import ImageFilterFactory
from sequencefilters.sequencefilter import SequenceFilterFactory
from sequencefilters.imageorder import ImageOrderFactory
from imagelist import ImageList
from imageobject import ImageObject
from dic import Dic
from dffexporter2 import *
from generatedffname import GenerateDffName

class mock_stdic:
    
    def __init__(self, folder, dfffolder, configurationfile=None):
        
        """
        configuration = ParseConfig(configurationfile)
        
        filtconfig      = configuration.filter_configuration
        dicconfig       = configuration.dic_configuration
        
        ordername        = configuration.order_name        
        seqname          = configuration.sequence_name
        pairiteratorname = configuration.pairiterator_name
        
        regexp          = configuration.regular_expression
        """
        filtconfig      = dict()
        
        ordername           = 'Filename'
        seqname             = 'Linear'
        seqconf             = None
        pairiteratorname    = 'First'
        
        regexp          = '.*-(?P<picturenumber>\d+)\.tiff'
        
        folder_object   = ExpressionFolder(folder)
        folder_object.findWithExpression(regexp)
        
        if len(folder_object.filelist) < 2:
            raise Exception("Could not find two pictures from folder: %s" % folder)

        imagefilters    = ImageFilterFactory().getImageFilters(filtconfig)
        order           = ImageOrderFactory().getImageOrder(ordername)        
        sequencefilter  = SequenceFilterFactory(order).getSequenceFilter(seqname, seqconf)
        imageclass      = ImageObject
        
        imagelist = ImageList(folder_object, imageclass, sequencefilter, imagefilters, regexp)
        
        pairIterator = PairIteratorFactory(imagelist).getPairIterator(pairiteratorname)
        
        exportparameters    = DffExportParameters(overwrite=True)
        exporter            = DffExporter2
        namegenerator       = GenerateDffName(dfffolder)
        dic                 = Dic()
        
        for (image1, image2) in pairIterator:
            
            dic.analyze(image1.getImage(), image2.getImage())
            exporterinstance = exporter(image1, image2, dic, exportparameters, namegenerator.generatename(image1, image2))
            exporterinstance.export()
            
if __name__=="__main__":
    mock_stdic('testsuite/test1','testsuite/test1')