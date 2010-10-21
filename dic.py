import bigtools
import bigoptimize
import bigfelreg
import numpy as np

class Dic:

    def __init__(self, verbose=0, xtol=0.05, degf=3, degc=3, crate=(16,16)):
        self.parameters = {"verbose": verbose, "xtol":xtol, 
                           "degf":degf, "degc":degc, 
                           "crate":crate}
        
    def analyze(self, image1, image2):
        
        imagearray1 = bigtools.OpenedImageToArray(image1)
        imagearray2 = bigtools.OpenedImageToArray(image2)
        
        par = bigtools.Parameters(self.parameters, override={'refimg':imagearray1,
                                                'testimg':imagearray2})
        warpingProblem = bigfelreg.MultigridableWarpingProblemBase(par=par)
        mrs = bigoptimize.MROptimizerState(warpingProblem, par=par)
        mrs.solveMR()
        self.deformationFunction = mrs.getProblem().datapart.testw
        self.shape = imagearray1.shape
        
    def getDeformationAtPoints(self, pointcollection):
        return self.deformationFunction.getDeformationAtPoints(np.array(pointcollection,float))
        