# -*- coding: utf-8 -*-
""" normalise.py

Created on Mon Mar 20 09:37:33 2017

@author: dhancock
"""

def normalise(self,verbose = False):
    '''generates normalised build parameters
    
    Note:
        imported into class buildparameters - not standalone.
    '''
    from SLMtools.classes import NormalisedBuildParameters
    requiredvalues = {'layer thickness':self.layerthickness,
                      'bed temperature':self.bedtemperature,
                      'beam coupling':self.beam.coupling,
                      'beam power':self.beam.power,
                      'beam radius':self.beam.radius,
                      'hatch spacing':self.beam.hatchspacing,
                      'scan speed':self.beam.scanspeed,
                      'material liquidus':self.material.liquidus,
                      'material conductivity':self.material.conductivity
                      }

    if type(self.beam.coupling) is not float:
        if verbose is True:
            print(type(self.beam.coupling))
            print("assuming 100% beam coupling for normalisation "+
                "rather than {}".format(self.beam.coupling))
        self.beam.coupling = 1
    try:
        # initialise Normalised object
        normalised = NormalisedBuildParameters()

        # calculate separate variables
        normalised.beampower = (
            (self.beam.coupling*self.beam.power) / (
                    (self.beam.radius * self.material.conductivity) *
                    (self.material.liquidus - self.bedtemperature)
            )
        )

        normalised.beamvelocity = (
            self.beam.scanspeed *
            self.beam.radius / self.material.diffusivity
        )

        normalised.layerthickness = (
            self.layerthickness / self.beam.radius
        )
        normalised.hatchspacing = (
            self.beam.hatchspacing / self.beam.radius
        )

        # calculate combined variables
        normalised.qvl = (
            normalised.beampower / (
            normalised.beamvelocity * normalised.layerthickness)
        )
        normalised.invhatchspacing = 1 / normalised.hatchspacing
        normalised.energy = (
            normalised.beampower / (
                normalised.beamvelocity
                * normalised.layerthickness
                * normalised.hatchspacing
            )
        )
        self.normalised = normalised
    except:
        print('#'*60)
        print('cannot calculate normalised values for',
              '{:}:{:}:{:};'.format(self.date,self.number,self.part.number))
        for value in requiredvalues:
            print('\t {:}: {:}'.format(value,requiredvalues[value]))
        raise

    try:
        from SLMtools.calculators.energydensity import energydensity
        self.energydensity = energydensity(self)
    except:
        print("could not get energy density")
    return
