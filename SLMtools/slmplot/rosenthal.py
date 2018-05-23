# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:17:42 2016

@author: dhancock

rosenthal modeller
"""


from matplotlib import pyplot as plt
from matplotlib import ticker
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class RosenthalPlot:
    def __init__(self,
                 build = None,
                 padding = (2,2),
                 figuretitle = "auto",
                 subplot=False):
        '''
        Takes a BuildParameters object (from SLMtools.classes)
        and plots the rosenthal surface

        padding = (xypadding, zpadding)
        '''
        if build is None:
            return
        self.build = build
        self.padding = padding
        self.figuretitle = figuretitle
        self.subplot = subplot
        self.setup_plot()
        self.setup_parameters()
        self.plot_rosenthal()


    def setup_plot(self):
        #from matplotlib import rc
        #rc('text',usetex=False)
        ## set plot envelope
        xypadding, zpadding = self.padding

        xyspan = xypadding*self.build.beam.hatchspacing
        xmin, xmax, ymin, ymax  = 2*(-xyspan,xyspan)
        zmin, zmax = -zpadding*self.build.layerthickness*1.5, 0
        self.bbox = xmin, xmax, ymin, ymax, zmin, zmax

        ## initialise plot
        if self.figuretitle == "auto":        
            try:
                self.figuretitle = str(build.date)+':'+str(build.part.number)
            except:
                print('unable to automatically label plot')
                self.figuretitle = "Rosenthal melt pool plot"
        
        self.fig = plt.figure(self.figuretitle,
                              plt.figaspect(1))

        ## place plot in figure
        if self.subplot is False:
            x,y,n = 1,1,1
        else:
            x,y,n = self.subplot
        self.ax = self.fig.add_subplot(x,y,n, 
                                       projection = '3d')

        """        
        ## Ensure equal aspect ratio by plotting "invisible" bounding box
        boxpoints = [[xmin,xmin,xmin,xmin,xmax,xmax,xmax,xmax],
                     [xmin,xmin,xmax,xmax,xmin,xmin,xmax,xmax],
                     [xmin,xmax,xmin,xmax,xmin,xmax,xmin,xmax]]
        self.ax.plot(boxpoints[0],boxpoints[1],boxpoints[2],'.w')
        """
        ## give the graph a pretty title
        axtitle = r'{:} :{:0.0f} W:{:0.0f} mm/s: {:0.0f} $\mu$m'.format(
                            self.build.material.shortname,
                            self.build.beam.power,
                            self.build.beam.scanspeed*1e3,
                            self.build.beam.hatchspacing*1e6)
        self.ax.set_title(axtitle)

        ## label axes
        self.ax.set_xlabel(r'x [$\mu$m]',fontsize = 9)
        self.ax.set_ylabel(r'y [$\mu$m]',fontsize = 9)
        self.ax.set_zlabel(r'z [$\mu$m]',fontsize = 9)

        ## set axis ticker format
        #fmt = ticker.FormatStrFormatter('%.1E')
        fmt = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*1e6))
        self.ax.xaxis.set_major_formatter(fmt)
        self.ax.yaxis.set_major_formatter(fmt)
        self.ax.zaxis.set_major_formatter(fmt)

        plt.setp(self.ax.get_xticklabels(),fontsize=9)
        plt.setp(self.ax.get_yticklabels(),fontsize=9)
        plt.setp(self.ax.get_zticklabels(),fontsize=9)
        


        return


    def setup_parameters(self):

        ## import build parameters
        T_m = self.build.material.liquidus
        T_atm = self.build.bedtemperature

        n = self.build.beam.coupling # need to check this is correct!
        Q = self.build.beam.power
        k = self.build.material.conductivity
        v = self.build.beam.scanspeed
        a = self.build.material.diffusivity

        ## combine
        self.build_parms = T_m, T_atm, n, Q, k, v, a


    def plot_rosenthal(self,hatchspacing=True):
        ## need to do this so that input of plot_implicit3d only takes x,y,z
        rosenthal_at_build = lambda x,y,z: self.rosenthal(x,y,z,self.build_parms)

        # plot rosenthal surface
        self.plot = self.plot_implicit3d(rosenthal_at_build,self.bbox)
        if hatchspacing is True:
            xmin = self.bbox[0]
            xmax = self.bbox[1]
            plt.gca().plot(
                [xmin,xmax],[self.build.beam.hatchspacing, 
                             self.build.beam.hatchspacing],'-r')
            plt.gca().plot(
                [xmin,xmax],[-self.build.beam.hatchspacing, 
                             -self.build.beam.hatchspacing],'-r')

        self.ax.set_xlim3d(xmin,xmax)
        self.ax.set_ylim3d(xmin,xmax)
        self.ax.set_zlim3d(xmin,0)
        plt.show()

        return

    def rosenthal(self,x,y,z,
              build_parms):
        '''
        calculates a rosenthal weld model function
        x,y,z   = location from centre of weld
        build_parms = build parameters (material and power input)
            build_parms = (T_m, T_atm, n, Q, k, v, a)
            T_m = melting temperature
            T_atm = ambient temperature
            n = power fraction delivered # needs checking
            Q = power
            k = material conductivity
            v = beam velocity
            a = material diffusivity
        '''
        # combine build parameters to object
        T_m, T_atm, n, Q, k, v, a = build_parms

        # do bits of calculation separately for tidiness
        DT  = T_m - T_atm
        R = (x**2 + y**2 + z**2)**0.5
        A = n*Q / (2*np.pi*k*R)
        B = -v/(2*a) * (x + R)

        # return function
        return A * np.exp(B) - DT


    def plot_implicit3d(self,fn, bbox, nslices = 30, ngrid = 100):
        '''
        Create a plot of an implicit function
        fn      = implicit function (plot where fn==0)
        bbox    = the x,y,and z limits of plotted interval
        nslices = number of slices across plotted area
        ngrid   = grid resolulution for plotted points
        '''

        # set bounding box limits
        xmin, xmax, ymin, ymax, zmin, zmax = bbox

        # open figure
        self.fig = plt.gcf()
        self.ax = plt.gca()

        # number of slices
        xslices = np.linspace(xmin,xmax,nslices)
        yslices = np.linspace(ymin,ymax,nslices)
        zslices = np.linspace(zmin,zmax,nslices)

        # grids
        xlin = np.linspace(xmin, xmax, ngrid)
        ylin = np.linspace(ymin, ymax, ngrid)
        zlin = np.linspace(zmin, zmax, ngrid)

        for z in zslices: # plot contours in the XY plane
            X,Y = np.meshgrid(xlin,ylin)
            Z = fn(X,Y,z)
            contourset = self.ax.contour(X, Y, Z+z, [z], zdir='z')
            # [z] defines the only level to plot
            # for this contour for this value of z

        for y in yslices: # plot contours in the XZ plane
            X,Z = np.meshgrid(xlin,zlin)
            Y = fn(X,y,Z)
            contourset = self.ax.contour(X, Y+y, Z, [y], zdir='y')

        for x in xslices: # plot contours in the YZ plane
            Y,Z = np.meshgrid(ylin,zlin)
            X = fn(x,Y,Z)
            contourset = self.ax.contour(X+x, Y, Z, [x], zdir='x')


        # must set plot limits because the contour will likely extend
        # way beyond the displayed level.
        # Otherwise matplotlib extends the plot limits
        # to encompass all values in the contour.
        self.ax.set_zlim3d(zmin,zmax)
        self.ax.set_xlim3d(xmin,xmax)
        self.ax.set_ylim3d(ymin,ymax)

        plt.show()

        return

class RosenthalPlotBuildset:
    def __init__(self,
                 buildset, 
                 padding = (2,2)):
        import math
        from copy import deepcopy
        
        rbs = deepcopy(buildset)
        rbs.dedupe(force=True)
        plotnumber = len(rbs.builds)
        plotgridsize = math.ceil(plotnumber**0.5)
        for i, build in enumerate(rbs.builds):
            subplot = (plotgridsize,plotgridsize,i+1)
            figuretitle = ','.join(rbs.sourcefile)
            RosenthalPlot(build,
                          padding,
                          figuretitle, 
                          subplot)

def test():
    '''
    test plotting using some default values
    '''
    xmin, xmax = -350e-6, 250e-6
    ymin, ymax = -250e-6, 250e-6
    zmin, zmax = -200e-6, 0

    T_m = 280
    T_atm = 25
    n = 0.388
    Q = 200
    k = 174
    v = .25
    a = 6.94e-5

    bbox = xmin, xmax, ymin, ymax, zmin, zmax
    build_parms = T_m, T_atm, n, Q, k, v, a

    fn = lambda x,y,z: RosenthalPlot.rosenthal(x,y,z,build_parms)
    RosenthalPlot.plot_implicit3d(fn,bbox)
    ax = plt.gca()
    ax.set_title('test')


if __name__ == '__main__':
    '''
    playing with some default values - testing
    '''

    from SLMtools.classes import BuildParameters

    build = BuildParameters(testing=True)
    build.beam.power = 200
    build.beam.scanspeed = 1
    rosenthalplot = RosenthalPlot(build)


