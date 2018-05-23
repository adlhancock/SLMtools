# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:34:55 2016

@author: dhancock
"""

class NormalisedBuildParameters:
    '''
    normalised build parameters object
    using [REF]_.
    
    '''
    contents = {'beampower':'normalised beam power',
            'beamvelocity':'normalised beam velocity',
            'layerthickness':'normalised layer thickness',
            'hatchspacing':'normalised hatch spacing',
            'qvl':'',
            'invhatchspacing':'inverse normalised hatch spacing',
            'energy':'normalised energy density'}


    def __init__(self):
        for item in self.contents:
            self.__dict__[item] = '{:} not calculated'.format(self.contents[item])



if __name__ == '__main__':
    from buildparameters import BuildParameters
    #buildparameters = BuildParameters(testing = True)
    buildparameters = BuildParameters()
    buildparameters.normalise()
    buildparameters.list_contents()
