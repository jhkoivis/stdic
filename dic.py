
from lib.analyzer import Analyzer
from lib.configparser import ConfigParser
from lib.folderscan import FolderScan
import sys

if __name__=="__main__":
    
        folder = sys.argv[1]
        dfffolder = sys.argv[2]
        configuration = sys.argv[3]
        
        #--------------------------------------------------------
        # Configuration parsing
        #--------------------------------------------------------
        
        configurationparser     = ConfigParser()
        config                  = configurationparser.parseFile(configurationfile)
        
        imageformat = config['imageformat']

        folder = FolderScan(folder)
        filelist = folder.findWithExpression(imageformat)
        
        analyzer = Analyzer(filelist, dfffolder, configuration)
        analyzer.analyze()