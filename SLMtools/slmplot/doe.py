# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import SLMtools

def doeplot(buildset,parameters=('power','scanspeed')):
    
    from matplotlib import pyplot as plt
    xs = []
    ys = []
    for build in buildset.builds:
        x, y =(build.beam.__dict__[item] for item in parameters)
        xs.append(x)
        ys.append(y)

    fig = plt.figure(buildset.name)
    ax = fig.add_subplot(111)
    ax.plot(xs,ys,'*r')
    plt.xlabel(parameters[0])
    plt.ylabel(parameters[1])
    plt.xlim(0.9*min(xs),1.1*max(xs))
    plt.ylim(0.9*min(ys),1.1*max(ys))
    plottitle = '{:}'.format(buildset.name)
    plt.title(plottitle)
    fig.show()
    
    return fig
    
        
def doetable(buildset, 
             parameters=['power', 
                         'scanspeed',
                         'layerthickness',
                         'hatchspacing'], 
             display=False):
    
        results = [parameters]

        for build in buildset.builds:
            row = []
            for item in parameters:
                try:
                    row.append(build.__dict__[item])
                except:
                    pass
                try:
                    row.append(build.beam.__dict__[item])
                except:
                    pass
            results.append(row)
        if display == True:
            for row in results:
                print(row)
        return results
            
            
if __name__ == '__main__':
    filename = 'F:/Python/Scripts/data/SLMtools/Ta_Birmingham_20161003.xlsx'
    buildset = SLMtools.BuildSet()
    buildset.import_excel(filename)
    """    
    buildset = SLMtools.BuildSet(testing=True)
    powers = [200,200,200,400,400,300]
    scanspeeds = [50,100,250,100,150,250]

    for i in range(len(powers)-1):
        buildset.builds.append(SLMtools.BuildParameters(testing=True))
    for build in buildset.builds:
        build.beam.power = powers.pop(0)
        build.beam.scanspeed = scanspeeds.pop(0)
    buildset.name = "Testing DOE plot tools"
    """
    table = doetable(buildset,display=True)
    doeplot(buildset) 
