# -*- coding: utf-8 -*-
"""
SLMtools DOE tools
Created on Mon Oct 24 14:26:28 2016

@author: dhancock
"""

def generate_DOE(startbuild,
                 power_range,
                 scanspeed_range,
                 layerthickness_range,
                 hatchspacing_range,
                 energy_range,
                 verbose = False):
    from copy import deepcopy
    parameters = ('beam power',
                  'scan speed',
                  'layer thickness',
                  'hatch spacing')
    builds = []
    
    logrange = lambda x: enumerate(np.logspace(np.log10(x[0]),
                                               np.log10(x[1]),
                                               x[2]))
    
    
    for i, p in logrange(power_range):
        for j, ss in logrange(scanspeed_range):
            for k, lt in logrange(layerthickness_range):
                for l, h in logrange(hatchspacing_range):
                    build = deepcopy(startbuild)
                    #print(i,j,k,l)                    
                    build.part.number = (1+i)*(1+j)*(1+k)*(1+l)
                    vs = [p,ss,lt,h]
                    for x in zip(parameters,vs):
                        build.set_parameter(*x,verbose=False)
                    build.normalise()
                    if min(energy_range) <= build.energydensity <= max(energy_range):
                        builds.append(build)
    
    return builds

if __name__ == '__main__':
    import numpy as np
    import SLMtools
    

    pr = (300,      400,    3)
    sr = (50e-3,   1500e-3, 5)
    lr = (20e-6,    40e-6,  3)
    hr = (50e-6,    100e-6, 5)
    er = (400e9,    1000e9)


    #pr = 30
    
    startbuild = SLMtools.BuildParameters(testing=True)
    
    doebuilds = generate_DOE(startbuild,
                             power_range = pr,
                             scanspeed_range = sr,
                             layerthickness_range = lr,
                             hatchspacing_range = hr,
                             energy_range=er)
    
    buildset = SLMtools.BuildSet()
    buildset.builds = doebuilds
    
    [build.normalise() for build in buildset.builds]
    SLMtools.NormalisedEnergyGraph(buildset,dedupe=True)
    

