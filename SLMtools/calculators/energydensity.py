# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 15:28:38 2016

@author: David
"""

""" TEMPORARILY REMOVED - amanda's new method below
def energydensity(build):
    energydensity = build.beam.power / (
        build.beam.scanspeed * build.layerthickness * build.beam.hatchspacing)
    
    return energydensity
"""
    
def energydensity(build):
    energydensity = build.beam.power/(
                        build.beam.scanspeed * 3.1415 * build.beam.radius**2)
    return energydensity

def find_missing(energy,
                 power=None,
                 scanspeed=None,
                 layerthickness=None,
                 hatchspacing=None,
                 verbose = False):
    if verbose is True:
        print('_'*30)
        for i in ['energy', 
                  'power', 
                  'scanspeed', 
                  'layerthickness', 
                  'hatchspacing']:
            if i in locals() and locals()[i] is not None:
                print('{:15} = {:10g}'.format(str(i),locals()[i]))
        print('='*30)

    if power is None:
        power = energy*scanspeed*layerthickness*hatchspacing
        if verbose is True:
            print("{:15} = {:10.1f} W".format('POWER',power))
        return 'beam power', power
    elif scanspeed is None:

        scanspeed = power/(energy*layerthickness*hatchspacing)
        if verbose is True:
            print("{:15} = {:10.1f} mm/s".format('SCAN SPEED',scanspeed*1e3))
        return 'scan speed', scanspeed
    elif layerthickness is None:

        layerthickness = power/(energy*hatchspacing*scanspeed)
        if verbose is True:        
            print("{:15} = {:10.1f} um".format("LAYER THICKNESS",layerthickness*1e6))
        return 'layer thickness', layerthickness
    elif hatchspacing is None:

        hatchspacing = power/(energy*scanspeed*layerthickness)
        if verbose is True:
            print("{:15} = {:10.1f} um".format('HATCH SPACING',hatchspacing*1e6))
        return 'hatch spacing', hatchspacing
    elif energy is None:
        energy = power / (scanspeed*layerthickness*hatchspacing)
        return 'energy density', energy
    else:
        print("no values found")
        return
    
    
if __name__ == '__main__':
    from SLMtools import BuildParameters

    build = BuildParameters(testing=True)
    #build.list_contents()
    ed = energydensity(build)
    print('build energy density = {:3.3e}'.format(ed))
    
    val = find_missing(energy=550e9,
                       power=400,
                       #scanspeed=250e-3,
                       layerthickness=30e-6,
                       hatchspacing=112e-6,
                       verbose=True)
