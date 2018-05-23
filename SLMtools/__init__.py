# -*- coding: utf-8 -*-
""" 
SLMtools
=========

Tools for recording, comparing and assessing SLM build parameters

.. moduleauthor:: adlhancock
"""


__all__ = ['scanspeed',
           'energydensity',
           'BuildSet',
           'BuildParameters',
           'classes',
           'NormalisedEnergyGraph',
           'NormalisedDensityGraph',
           'RosenthalPlot',
           'RosenthalPlotBuildset',
           'EnergyDensityPorosityGraph',
           'tabulatedensity']

#import top level classes
#from SLMtools.classes.buildset import BuildSet
#from SLMtools.classes.buildparameters import BuildParameters

from .classes.buildset import BuildSet
from .classes.buildparameters import BuildParameters

from . import classes

# import calculation tools
from SLMtools.calculators import scanspeed
from SLMtools.calculators.energydensity import energydensity

# import graph types
from SLMtools.slmplot.normalised import NormalisedEnergyGraph
from SLMtools.slmplot.rosenthal import RosenthalPlot, RosenthalPlotBuildset
from SLMtools.slmplot.results import EnergyDensityPorosityGraph

# import tables
from SLMtools.slmplot.results import tabulatedensity
