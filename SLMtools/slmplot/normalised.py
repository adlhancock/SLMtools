# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:59:27 2016

@author: David
"""


#plt.rc('text', usetex=True)

class NormalisedEnergyGraph():
    '''
    Plots normalised energy values and associated isopleths
    '''

    def __init__(self,
                 buildset = 'None',
                 figuretitle = 'filename',
                 energylines = 'auto',
                 pointlabels = True,
                 dedupe = True,
                 tabulate = True):

        from matplotlib import pyplot as plt
        import numpy as np
        
        try:
            if 'normalised' not in buildset.__dict__:
                [build.normalise() for build in buildset.builds]
        except:
            raise
        
        # set up graph axes
        self.dedupe = dedupe
        self.tabulate = tabulate
        self.pointlabels = pointlabels
        self.buildset = buildset
        self.get_envelope(buildset)
        
        if figuretitle == 'filename':
            try:
                fig = plt.figure(
                "Normalised Energy Graph [{}]".format(buildset.sourcefile))
            except:
                fig = plt.figure('Energy Graph')
        else:
            fig = plt.figure(figuretitle)
        #self.axes = fig.add_subplot(121)
        #self.axes = plt.subplot2grid((1,4),(0,0),colspan=3)
        self.axes = fig.add_subplot(111)
        self.axes.set_yscale('log')
        self.axes.set_xscale('log')
        self.axes.set_ylabel('1/h*')
        self.axes.set_xlabel('q*/(v*l*)')
        plt.title('Normalised Energy Density')
        plt.grid(which = 'both')

        #set limits
        xlim, ylim = [0.8*min(self.qvl_values),1.2*max(self.qvl_values)],\
                     [0.8*min(self.invh_values),1.2*max(self.invh_values)]

        for lim in xlim,ylim:
            if lim[0] < 0.1:
                lim[0] = 0.1
        

        # set ticks

        ax = plt.gca()

        magnitude = lambda x: np.floor(np.log10(x))
        lower = lambda y : (np.floor(y / 10**magnitude(y))-1)*10**magnitude(y)
        upper = lambda y : (np.floor(y / 10**magnitude(y))+1)*10**magnitude(y)
        step = lambda y: 10**magnitude(y)*2
        ticks = lambda z: np.arange(lower(z[0]),upper(z[1]),step(z[0]))
        
        xticks,yticks = ticks(xlim),ticks(ylim)
        
        ax.set_xticks(xticks)
        ax.set_xticklabels(['{:g}'.format(x) for x in xticks])
        ax.set_yticks(yticks)
        ax.set_yticklabels(['{:g}'.format(y) for y in yticks])
       
        plt.xlim(xlim)
        plt.ylim(ylim)

        self.plot_isopleths(energylines)

        self.plot_builds(buildset)

        """
        ax = plt.gca()
        ax.legend(bbox_to_anchor = (1,0),
                  loc = 3,
                  borderaxespad = 0,
                  ncol=1,
                  fontsize = 'small',
                  markerscale = 0.75)
        """

        plt.show()

    def get_envelope(self,buildset):
        self.energy_values = [self.buildset.builds[number].normalised.energy \
                        for number, build in enumerate(self.buildset.builds)]
        self.invh_values = [
                self.buildset.builds[number].normalised.invhatchspacing \
                        for number, build in enumerate(self.buildset.builds)]
        self.qvl_values = [self.buildset.builds[number].normalised.qvl \
                        for number, build in enumerate(self.buildset.builds)]
        self.e_max = max([build.beam.power for build in self.buildset.builds])
        return

    def plot_isopleths(self,energylines):
        from matplotlib import pyplot as plt
        import numpy as np
        from itertools import cycle
        lines = ["-","--","-.",":"]
        linecycler = cycle(lines)

        if energylines == 'auto':
          try:
              energylines = np.logspace(np.log10(0.9*min(self.energy_values)),
                                        np.log10(1.1*max(self.energy_values)),
                                        5)
              """
               energylines = np.linspace(0.9*min(self.energy_values),
                                        1.1*max(self.energy_values),
                                        5)
               """
          except:
              print('could not automatically set range')
        # set up isopleth values
        isopleths = {}
        isopleths['energies'] = energylines
        isopleths['qvl_min'] = 0.1
        isopleths['invh_min'] = 0.1

        isopleths['qvl_vals'], isopleths['invh_vals'] = [],[]
        for energy in isopleths['energies']:
            isopleths['qvl_vals'].append(
                [isopleths['qvl_min'],energy/isopleths['qvl_min']])
            isopleths['invh_vals'].append(
                [energy/isopleths['invh_min'],isopleths['invh_min']])

        # plot isopleths
        isopleths['lines'] = []
        for x in range(len(isopleths['energies'])):
            isopleths['lines'].append(
                self.axes.plot(isopleths['qvl_vals'][x],
                               isopleths['invh_vals'][x],
                               linestyle = next(linecycler),
                               marker = '.',
                   label = 'E* = {:0.1f}'.format(isopleths['energies'][x])))
        self.isopleths = isopleths
        ax = plt.gca()
        ax.legend(fontsize="small")
        plt.show()
        return

    def plot_builds(self, buildset):

        from matplotlib import pyplot as plt
        # plot build points
        if self.dedupe is True:
            allbuilds = buildset.builds
            energies = []
            dedupedbuilds = []
            for build in allbuilds:
                if build.normalised.energy not in energies:
                    energies.append(build.normalised.energy)
                    dedupedbuilds.append(build)
            builds = dedupedbuilds
        else:
            builds = buildset.builds
        buildpoints = []
        self.plotdetails = []
        
        self.headers = ['{:^5}'.format('point'),
                    '{:^5}'.format("mat."),
                    '{:^10}'.format("power [W]"),
                    '{:^10}'.format("s.speed [mm/s]"),
                    '{:^10}'.format("h.spacing [um]"),
                    '{:^14}'.format("Energy [W/mm^3]"),
                    '{:^10}'.format("E*")]        

        for i, build in enumerate(builds):
            x = build.normalised.qvl
            y = build.normalised.invhatchspacing

            self.plotdetails.append(['{:^5}'.format(i),
                                '{:^5}'.format(build.material.shortname),
                                '{:^10.0f}'.format(build.beam.power),
                                '{:^14.0f}'.format(build.beam.scanspeed*1000),
                                '{:^14.0f}'.format(build.beam.hatchspacing*1e6),
                                '{:^15.1f}'.format(build.energydensity*1e-9),
                                '{:^10.1f}'.format(build.normalised.energy)])

            plotlabel = i
            buildpoints.append(
                self.axes.plot(
                    x,
                    y,
                    'o',
                    markersize = build.beam.power/self.e_max*10,
                    label = plotlabel))
                    
            if self.pointlabels is True:

                self.axes.annotate(i,
                                   xy=(1.02*x,1.02*y),
                                   fontsize = "x-small")

        self.buildpoints = buildpoints
        
        if self.tabulate is True:
            print('_'*80)
            print('|'.join(self.headers))
            print('='*80)
            for row in self.plotdetails:
                print('|'.join(row))
        plt.show()
        return

    def export_plotdetails(self,filename):
        with open(filename,'w') as f:
            f.write(', '.join([header.strip() for header in self.headers])+'\n')
            for row in self.plotdetails:
                f.write(', '.join([point.strip() for point in row])+'\n')
        print('wrote plot details to {}'.format(filename))
            

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    plt.clf()
    # make sure we've got the buildparameters class
    from SLMtools.classes import BuildSet, BuildParameters

    # generate list of default buildparameters
    buildset = BuildSet()
    buildset.builds = [BuildParameters(testing=True),
                       BuildParameters(testing=True)]

    # change some of the values to make it interesting
    buildset.builds[1].beam.hatchspacing = (
        10e-6+(buildset.builds[0].beam.hatchspacing))
    buildset.builds[1].beam.scanspeed = (
        2*(buildset.builds[0].beam.scanspeed))

    # generate normalised values
    buildset.builds[0].normalise()
    buildset.builds[1].normalise()

    # give the builds different labels
    buildset.builds[0].number = 1
    buildset.builds[1].number = 2

    # tabulate points in console
    print('_'*40)
    print(
        '{0:^15}{1:^15}'
        .format('1/h*','q*/(v*l*)')
    )
    print('='*40)
    for build in buildset.builds:
        print(
            '{0:^15.2f}{1:^15.2f}'
            .format(build.normalised.invhatchspacing,
                    build.normalised.qvl))
    print('_'*40)
    # clear previous plots
    plt.close('all')

    # draw energy graph with range of isopleths
    #energygraph = EnergyGraph(buildset,energylines=[10,20,30,40])
    energygraph = NormalisedEnergyGraph(buildset,energylines='auto')

    #plt.show()

