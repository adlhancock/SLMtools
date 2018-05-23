# -*- coding: utf-8 -*-
"""
SLMtools.classes:
=================
    classes for use in SLMtools

.. moduleauthor:: adlhancock

"""

__all__ = ['BuildParameters',
           'BuildSet',
           'Material',
           'Beam',
           'Part',
           'Results',
           'Comments',
           'NormalisedBuildParameters']

from .buildparameters import BuildParameters
from .buildset import BuildSet

from .material import Material
from .part import Part
from .beam import Beam
from .results import Results
from .comments import Comments

from .normalisedparameters import NormalisedBuildParameters

if __name__ == '__main__':
    buildset = BuildSet(testing = True)
    buildset.list_contents()