
from sys import argv
from expressionfolder import ExpressionFolder
from pairiterators.pairiterator import PairIteratorFactory
from imagefilters.imagefilter import ImageFilterFactory
from sequencefilters.sequencefilter import SequenceFilterFactory
from sequencefilters.imageorder import ImageOrderFactory
from configobject import *
from imagelist import ImageList
from imageobject import ImageObject
from dic import Dic
from exporters.exporter import ExporterClassFactory
from exporters.dffexporter import DffExportParameters
from dfftools import *

class FolderAnalyzer:
    
    def __init__(self, folder, dfffolder, configurationfile):
        
        self.initialize(configurationfile)
        
        folder_object = ExpressionFolder(folder)
        folder_object.findWithExpression(self.regexp)
        
        if len(folder_object.filelist) < 2:
            raise Exception("Could not find two pictures from folder: %s" % folder)

        imagefilters        = ImageFilterFactory().getImageFilters(self.filtconfig)
        order               = ImageOrderFactory().getImageOrder(self.ordername, self.orderconfig)
        sequencefilter      = SequenceFilterFactory().getSequenceFilter(self.seqname, order, self.seqconfig)
        imageclass          = ImageObject
        
        imagelist           = ImageList(folder_object, imageclass, sequencefilter, imagefilters, self.regexp)
        
        pairIterator        = PairIteratorFactory().getPairIterator(self.pairiteratorname, imagelist, self.pairiteratorconfig)
        
        exportparameters    = DffExportParameters(dicconfig = self.dicconfig, **self.dffconfig)
        exporterfactory     = ExporterClassFactory()
        exporter            = exporterfactory.getExporterClass(self.dffname)
        
        namegenerator       = PictureNumberDffname(dfffolder)
        dffchecker          = CheckDffExistence()
        dic                 = Dic(**self.dicconfig)
        
        for (image1, image2) in pairIterator:
            self.dffname = namegenerator.generatename(image1, image2)
            if not self.overwrite:
                if dffchecker.checkExistence(self.dffname):
                    continue
            dic.analyze(image1.getImage(), image2.getImage())
            exporterinstance = exporter(image1, image2, dic, exportparameters, self.dffname)
            exporterinstance.export()
            
    def initialize(self, configurationfile):
        
        configurationparser     = ConfigObjectParser(configurationfile)
        configuration           = configurationparser.parse('configuration')
        
        self.regexp             = configuration.regularexpression._value
        
        try:
            self.filtconfig     = configuration.filters.getValues()
        except AttributeError:
            self.filtconfig     = dict()
        
        self.orderconfig        = configuration.order.getValues()
        self.ordername          = self.orderconfig.pop('name')
        
        self.seqconfig          = configuration.sequence.getValues()
        self.seqname            = self.seqconfig.pop('name')
        
        self.pairiteratorconfig = configuration.pairiterator.getValues()
        self.pairiteratorname   = self.pairiteratorconfig.pop('name')
            
        try:
            self.dicconfig      = configuration.dic.getValues()
        except AttributeError:
            self.dicconfig      = dict()
        
        try:
            self.dffconfig      = configuration.dff.getValues()
        except AttributeError:
            self.dffconfig      = dict({'name':'DffExporter'})
            
        self.dffname            = self.dffconfig.pop('name')
        
        self.overwrite          = configuration.overwrite._value
            
if __name__=="__main__":
    
    FolderAnalyzer(*argv[1:])