# -*- coding: utf-8 -*-
"""
SLMtools.slmplot.results

Created on Thu Jun  2 12:19:03 2016

@author: dhancock
"""
from itertools import cycle
markers = cycle(["x","o","^"])

class EnergyDensityPorosityGraph():
    """
    Plots a graph of part density against 
    volumetric energy density for a set of SLM builds
    Keyword arguments:
        - fitcurve: False, ('poly',[integer]),'tanh_linear'
    """
    def __init__(self,
                 buildset,
                 figuretitle = 'auto',
                 graphtitle = 'auto',
                 fitcurve = False,
                 label = 'auto',
                 showbest = True,
                 normalised = False,
                 errorbars = False,
                 **kwargs):
        
        from matplotlib import pyplot as plt
        from SLMtools.calculators.energydensity import energydensity
        from scipy.optimize import curve_fit
        import numpy as np
        
        self.buildset = buildset
        
        """ give figure sensible title  """
        if figuretitle == 'auto':
            try:
                figuretitle = "Energy vs. Density graph\n [{}]".format(buildset.name)
            except:
                figuretitle = 'Energy density vs. part density'
        if graphtitle == 'auto':
            try: 
                graphtitle = figuretitle
            except: 
                graphtitle = "Energy Density vs. Part Density"
        if label == 'auto':
            """
            materials = []
            allmaterials = [build.material.name for build in buildset.builds]
            [materials.append(material) \
                        for material in allmaterials \
                        if material not in materials]
            label = ', '.join(materials)
            """
            label = buildset.name

        """ import data """
        energies, densities = [], []
        for build in buildset.builds:
            try:
                density = float(build.results.relative_density)
                #if density < 0.5: density = "Fail"
                if normalised is True:
                    try:
                        #print("Normalising data")
                        build.normalise()
                    except:
                        print('Could not normalise')
                    energy = float(build.normalised.energy)
                else:
                    energy = float(energydensity(build)/(1e9))
                if density > 0.5: 
                    densities.append(density)
                    energies.append(energy)
            except:
                pass
        if len(densities) == 0:
            print("No densities in {:} available to plot".format(buildset.name))
            return
         

        
        """ plot data """
        self.fig = plt.figure(figuretitle,
                              figsize = (7,6),
                              dpi = 100) 
        ax = plt.gca()
        #ax = self.fig.add_subplot(111)
        if normalised is True:
            plt.xlabel('E*')
        else:
            plt.xlabel('Energy Density [J/mm^3]')
        plt.ylabel('Relative Part Density')
        plt.title(graphtitle)
        plt.grid('on',
                 linestyle=":")
        
        if errorbars is 'sd':
            es, meandensities, stds = self.find_std(energies, densities)
            plt.errorbar(es,meandensities,yerr=stds,
                         fmt='x',
                         ecolor=None,
                         label=label)
            self.errorbardata = [es,meandensities,stds]
        if errorbars is 'experimental error':
            print('experimental error bars not supported yet')
            pass
        else:
            #mkr = 'x'
            mkr = next(markers)
            if "marker" in kwargs: mkr = kwargs["marker"]
            ax.plot(energies, densities, marker = mkr,linestyle='',label=label)            
            pass
        ax.legend(ncol = 2,
                  loc="upper left",
                  bbox_to_anchor = (0,-0.03,1,-0.1),
                  mode = "expand",
                  borderaxespad=0,
                  #handlelength = 5,
                  )
        plt.tight_layout(pad=1.2)
        self.fig.subplots_adjust(bottom = 0.2)
        

        """add trendline"""
        if fitcurve is False:
            maxdensity = max(densities)
            bestenergy = energies[densities.index(maxdensity)]

        elif len(densities)>3:
            if fitcurve == 'lognormal':
                def lognormal(x,sigma,mu,height,l):
                    a = height*1/(x/l*sigma*np.sqrt(2*np.pi))
                    b = ((np.log(x/l)-mu)**2) / (2 * sigma**2)
                    return a*np.exp(-b)
                fitcurve = lognormal 
            
            if fitcurve == "tanh_linear":
                def tanh_linear(x,a,b,c,d,e):
                    from numpy import tanh
                    tanh_bit = a*tanh((x**b/(100*c)))
                    linear_decay_bit = (-d/1e5)*x+1+(e/1e3)
                    return tanh_bit*linear_decay_bit
                fitcurve = tanh_linear

            elif 'poly' in str(fitcurve):
                trendline = np.poly1d(np.polyfit(energies,densities,fitcurve[1]))

            if callable(fitcurve) is True:            
                try:
                    popt,pcov = curve_fit(fitcurve,energies,densities)
                    trendline = lambda x: fitcurve(x,*popt)
                except:
                    print('could not fit curve to function')
                    trendline = None
                
            try:
                xs = np.linspace(min(energies),max(energies),100)
                ax.plot(xs, trendline(xs),'--r')
    
                maxdensity = max(trendline(xs))
                bestenergy = xs[trendline(xs).argmax()]
            except:
                print("could not plot trend line using {}".format(fitcurve))
        else:
            print("not enough density points to plot trendline")
            
        """ Show maximum point"""
        if showbest is True:
            try:
                ax.annotate('Max ({1:5.3f},{0:0.2f})'.format(
                                                maxdensity,bestenergy), 
                                                xy = (bestenergy,maxdensity*1.001), 
                                                fontsize = "x-small")
            except:
                print('could not display best value')
        
        """ Set limits of graph """
        plt.ylim([min(densities),1])        
        plt.show()
                
        self.headers = ['Energy [W/mm^3]','relative density']
        self.data = sorted([x for x in zip(energies,densities)],key=lambda row: row[0])

        return
        
    def find_std(self,energies,densities):
        import numpy as np
        deduped = {}
        for i, e in enumerate(energies):
            if e not in deduped:
                deduped[e] = []
            deduped[e].append(densities[i])
        #print(deduped)
        print("De-duplicating points")
        energies = [energy for energy in deduped.keys()]
        meandensities = [np.sum(deduped[x])/len(deduped[x]) for x in deduped.keys()]
        uncertainties = [np.std(deduped[x]) for x in deduped.keys()]
        return energies,meandensities,uncertainties
        
    def tabulate_data(self):
        print('_'*40)
        print('\n'.join(self.buildset.sourcefile))
        print('_'*40)
        print('|'.join(['{:^20}'.format(x) for x in self.headers]))
        print('='*40)
        for row in self.data:
            print('|'.join(['{:^20g}'.format(x) for x in row]))
    
    def write_to_file(self,filename):
        try:
            with open(filename,'w') as f:
                f.write(', '.join(self.headers)+'\n')
                f.writelines([','.join([str(i) for i in row])+'\n' for row in self.data])
            print("Wrote data to {}".format(filename))    
        except:
            raise
            print("unable to write graph data to file")
        return

def tabulatedensity(buildset,
                    sortedby='Relative Density'):
    
    """
    Plots a table of build parameters with density results:
        sortedby values:
            'Power',
            'Scan Speed',
            'Hatch',
            'Beam D',
            'E Density',
            'Relative Density'
    """    
    
    headings = ['Material',
                'Power',
                'Scan Speed',
                'Hatch',
                'Beam D',
                'E Density',
                'Relative Density']
                
    if sortedby not in headings:
        print('unable to sort data by {}\n'.format(sortedby))
        sortedby='Relative Density'
        
    from SLMtools import energydensity
    print('{:12} | '.format(headings[0])+
          '{:7} | '.format(headings[1])+
          '{:8} | '.format(headings[2])+
          '{:8} | '.format(headings[3])+
          '{:9} | '.format(headings[4])+
          '{:13} | '.format(headings[5])+
          '{:11} | '.format(headings[6]))
    print('='*95)
    rawdata = []
    for build in buildset.builds:
        try: 
            density = '{:8.2f}'.format(build.results.relative_density*100)
        except:
            density = '  {}  '.format('-')
        rawdatarow = [build.material.shortname,
                      build.material.supplier,
                      build.beam.power, 
                      build.beam.scanspeed*1000, 
                      build.beam.hatchspacing*1e6, 
                      build.beam.radius*2e6, 
                      energydensity(build)/(1e3)**3, 
                      density]

        rawdata.append(rawdatarow)


    try:    
        rawdata.sort(key = lambda row: row[headings.index(sortedby)+1])
    except:
        raise
        
    for row in rawdata:
        formattedrow = ('{:2s}:{:9s} | '.format(row[0],row[1])+
                        '{:3.0f} {:3s} | '.format(row[2],'W')+
                        '{:5.0f} {:4s} | '.format(row[3],'mm/s')+
                        '{:4.0f} {:3s} | '.format(row[4],'um')+
                        '{:4.0f} {:4s} | '.format(row[5],'um')+
                        '{:6.1f} {:6s} | '.format(row[6],'W/mm^3')+
                        '{:16s} |'.format(row[7]))
        print(formattedrow)
    print('sorted by {:}({:})\n'.format(sortedby,headings.index(sortedby)+1))
if __name__ == '__main__':
    testfile = '../../data/SLMtools/Ta_Birmingham_20161003.xlsx'
    import SLMtools
    buildset = SLMtools.BuildSet()
    buildset.import_excel(testfile)
    graph = EnergyDensityPorosityGraph(buildset)