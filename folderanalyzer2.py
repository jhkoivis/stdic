
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
        
        #--------------------------------------------------------
        # Configuration parsing
        #--------------------------------------------------------
        
        configurationparser     = ConfigObjectParser(configurationfile)
        configuration           = configurationparser.parse('configuration')
        
        regexp                  = configuration.regularexpression._value
        
        try:
            outputconfig        = configuration.output.getValues()
            outputformat        = outputconfig.pop('format')
        except:
            outputformat        = "dff-%s-%s.dff"
        
        try:
            filtconfig = dict()
            for sub in configuration.filters.getSubs():
                values = sub.getValues()
                name = values.pop('name')
                filtconfig[name] = values
        except AttributeError:
            filtconfig          = dict()
        
        orderconfig             = configuration.order.getValues()
        ordername               = orderconfig.pop('name')
        
        seqconfig               = configuration.sequence.getValues()
        seqname                 = seqconfig.pop('name')
        
        self.pairiteratorconfig = configuration.pairiterator.getValues()
        pairiteratorname        = self.pairiteratorconfig.pop('name')
            
        try:
            dicconfig           = configuration.dic.getValues()
        except AttributeError:
            dicconfig           = dict()
        
        try:
            exporterconfig      = configuration.dff.getValues()
        except AttributeError:
            exporterconfig      = dict({'name':'DffExporter'})
            
        exportername            = exporterconfig.pop('name')
        
        self.overwrite          = configuration.overwrite._value
        
        #--------------------------------------------------------
        # Creation of pairiterator
        #--------------------------------------------------------
                
        folder_object = ExpressionFolder(folder)
        folder_object.findWithExpression(regexp)
        
        if len(folder_object.filelist) < 2:
            raise Exception("Could not find two pictures from folder: %s" % folder)

        imagefilters            = ImageFilterFactory().getImageFilters(filtconfig)
        order                   = ImageOrderFactory().getImageOrder(ordername, orderconfig)
        sequencefilter          = SequenceFilterFactory().getSequenceFilter(seqname, order, seqconfig)
        imageclass              = ImageObject
        
        imagelist               = ImageList(folder_object, imageclass, sequencefilter, imagefilters, regexp)
                
        self.pairiterator       = PairIteratorFactory().getPairIterator(pairiteratorname, imagelist, self.pairiteratorconfig)
        
        #--------------------------------------------------------
        # Creation of other objects and classes
        #--------------------------------------------------------
        
        self.exportparameters   = DffExportParameters(dicconfig = dicconfig, **exporterconfig)
        
        self.exporter           = ExporterClassFactory().getExporterClass(exportername)
        
        self.namegenerator      = PictureNumberDffname(dfffolder, outputformat)
        self.dffchecker         = CheckDffExistence()
        self.dic                = Dic(**dicconfig)
        
    def analyze(self):
        
        for (image1, image2) in self.pairiterator:
            try:
                print "Analyzing pictures number %s and %s." % (image1.picturenumber, image2.picturenumber)
            except AttributeError:
                pass
            dffname = self.namegenerator.generatename(image1, image2)
            if not self.overwrite:
                if self.dffchecker.checkExistence(dffname):
                    continue
            self.dic.analyze(image1.getImage(), image2.getImage())
            exporterinstance = self.exporter(image1, image2, self.dic, self.exportparameters, dffname)
            exporterinstance.export()
            
if __name__=="__main__":
    
    analyzer = FolderAnalyzer(*argv[1:])
    analyzer.analyze()