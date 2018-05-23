# -*- coding: utf-8 -*-
"""
calculates 1D and 2D energy densities from build parameter file
for renishaw (i.e. pulsed laser)

Created on Thu Jan 14 14:48:50 2016

@author: dhancock
"""

def getenergydensities(bp = None,linelength = 1,dimension = "all", testing = False):
    
    if testing is True:
        #default values to compare to Jon's calcs    
        print('running energydensitycalculator using test values')
        bp = SLMtools.classes.BuildParameters()        
        bp.beam.power = 180
        bp.beam.hatchspacing = 0.09e-3
        bp.beam.radius = 25e-6
        bp.beam.exposuretime = 200e-6
        bp.beam.pointdistance = 50e-6
        
    if bp is None:
        print('build parameters not supplied')
        return
        
    exposuretime = bp.beam.exposuretime
    pointdistance = bp.beam.pointdistance
    power = bp.beam.power    
    spotsize = bp.beam.radius * 2
    hatchspacing = bp.beam.hatchspacing
    pointsperm = linelength / pointdistance
    #print(pointsperm)
    energyperpoint = power * exposuretime
    lineareaperm = linelength * spotsize
    areaenergydensityscale = spotsize / hatchspacing
    
    line1Denergydensity = pointsperm * energyperpoint
    line2Denergydensity = line1Denergydensity / lineareaperm
    area2Denergydensity = line2Denergydensity * areaenergydensityscale    
    
    if dimension == 'all':
        energydensity = {'1D line':line1Denergydensity,
                         '2D line':line2Denergydensity,
                         '2D area':area2Denergydensity}
    elif dimension == '1D line':
        energydensity = {'1D line':line1Denergydensity}
    elif dimension == '2D line':
        energydensity = {'2D line':line2Denergydensity}
    elif dimension == '2D area':
        energydensity = {'2D area':area2Denergydensity}
    else: 
        print(
        'dimension must be \'1D line\', \'2D line\', \'2D area\', or \'all\'')
        energydensity = None
    
    return energydensity
    
def printenergydensities(energydensity = None, testing = False):
    if testing is True:
        energydensity = getenergydensities(testing = True)
        
    if energydensity is None:
        print('energy density not supplied')
        return
        
    names = ['1D line','2D line','2D area']
    units = ['J/m','J/mm^2','J/mm^2']
    multipliers = [1,1e-6,1e-6]
    
    print('Energy densities:')
    for number, name in enumerate(names):
        if name in energydensity.keys():
            print(name,
                  '= {0:8.4}'.format(
                        float(energydensity[name])*multipliers[number]),
                  units[number])
                  
    return energydensity


if __name__ == '__main__':
    import SLMtools
    energydensity = printenergydensities(testing=True)
    print()    
    energydensity = getenergydensities(testing = True, dimension='2D area')
    printenergydensities(energydensity)
    print()
    energydensity = getenergydensities()