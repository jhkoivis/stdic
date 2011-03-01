
from sys import argv
from pairiterators.pairiterator import PairIteratorFactory
from imagefilters.imagefilter import ImageFilterFactory
from sequencefilters.sequencefilter import SequenceFilterFactory
from sequencefilters.imageorder import ImageOrderFactory
from configparser import ConfigParser
from imagelist import ImageList
from diccontroller import DICController
from exporters.exporter import ExporterClassFactory
from exporters.dffexporter import DffExportParameters
from dfftools import *

class Analyzer:
    
    def __init__(self, filelist, dfffolder, config):
        
        #--------------------------------------------------------
        # Generate image filters
        #--------------------------------------------------------
        
        try:
            filtconfig          = config["imagefilters"]
        except KeyError:
            filtconfig          = dict()
        
        imagefilters            = ImageFilterFactory().getImageFilters(filtconfig)
        
        #--------------------------------------------------------
        # Generate ordering
        #--------------------------------------------------------
        
        orderconfig             = config["order"]
        ordername               = orderconfig.pop('name')
        
        order                   = ImageOrderFactory().getImageOrder(ordername, orderconfig)

        #--------------------------------------------------------
        # Generate sequence with ordering
        #--------------------------------------------------------
        
        seqconfig               = config["sequence"]
        seqname                 = seqconfig.pop('name')
        
        sequencefilter          = SequenceFilterFactory().getSequenceFilter(seqname, order, seqconfig)
        
        #--------------------------------------------------------
        # Generate imagelist from filelist, imagefilters and sequence
        #--------------------------------------------------------
        
        if len(filelist) < 2:
            raise Exception("Filelist too short.")
        
        try:
            regexp              = config['imageformat']
        except KeyError:
            regexp              = None
        
        imagelist               = ImageList(filelist, sequencefilter, imagefilters, regexp)
         
        #--------------------------------------------------------
        # Generate pairiterator from imagelist
        #--------------------------------------------------------
        
        pairiteratorconfig      = config["pairiterator"]
        pairiteratorname        = pairiteratorconfig.pop('name')  
        
        self.pairiterator       = PairIteratorFactory().getPairIterator(pairiteratorname, imagelist, pairiteratorconfig)
        
        #--------------------------------------------------------
        # Generate DIC
        #--------------------------------------------------------
            
        try:
            dicconfig           = config["dic"]
        except KeyError:
            dicconfig           = dict()
            
        self.dic                = DICController(**dicconfig)
        
        #--------------------------------------------------------
        # Generate Exporter and analysis parameters
        #--------------------------------------------------------
        
        try:
            exporterconfig      = config["dff"]
        except KeyError:
            exporterconfig      = dict({'name':'DffExporter'})
            
        exportername            = exporterconfig.pop('name')
            
        self.exporter           = ExporterClassFactory().getExporterClass(exportername)
        
        self.overwrite          = config["overwrite"]
        
        try:
            outputconfig        = config['output']
            outputformat        = outputconfig['format']
        except KeyError:
            outputformat        = "dff-%s-%s.dff" 
        
        self.namegenerator      = PictureNumberDffname(dfffolder, outputformat)
        
        self.exportparameters   = DffExportParameters(dicconfig = dicconfig, **exporterconfig)
        
        self.dffchecker         = CheckDffExistence()
        
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
