
from sys import argv
from expressionfolder import ExpressionFolder
from pairiterators.pairiterator import PairIteratorFactory
from imagefilters.imagefilter import ImageFilterFactory
from sequencefilters.sequencefilter import SequenceFilterFactory
from sequencefilters.imageorder import ImageOrderFactory
from configparser import ConfigParser
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
        
        configurationparser     = ConfigParser()
        config                  = configurationparser.parseFile(configurationfile)
        
        regexp                  = config['imageformat']
        
        try:
            outputconfig        = config['output']
            outputformat        = outputconfig['format']
        except:
            outputformat        = "dff-%s-%s.dff"
        
        try:
            filtconfig          = config["imagefilters"]
        except AttributeError:
            filtconfig          = dict()
        
        orderconfig             = config["order"]
        ordername               = orderconfig.pop('name')
        
        seqconfig               = config["sequence"]
        seqname                 = seqconfig.pop('name')
        
        pairiteratorconfig      = config["pairiterator"]
        pairiteratorname        = pairiteratorconfig.pop('name')
            
        try:
            dicconfig           = config["dic"]
        except AttributeError:
            dicconfig           = dict()
        
        try:
            exporterconfig      = config["dff"]
        except AttributeError:
            exporterconfig      = dict({'name':'DffExporter'})
            
        exportername            = exporterconfig.pop('name')
        
        self.overwrite          = config["overwrite"]
        
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
                
        self.pairiterator       = PairIteratorFactory().getPairIterator(pairiteratorname, imagelist, pairiteratorconfig)
        
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
