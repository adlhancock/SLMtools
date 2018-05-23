# -*- coding: utf-8 -*-
"""
SLMtools.classes:
=================
    classes for use in SLMtools

.. py:module:: classes

.. moduleauthor:: dhancock
"""

__all__ = ['BuildParameters',
           'BuildSet',
           'Material',
           'Beam',
           'Part',
           'Results',
           'Comments',
           'NormalisedBuildParameters',
           'normalise']

from SLMtools.classes.buildparameters import BuildParameters
from SLMtools.classes.buildset import BuildSet

from SLMtools.classes.material import Material
from SLMtools.classes.part import Part
from SLMtools.classes.beam import Beam
from SLMtools.classes.results import Results
from SLMtools.classes.comments import Comments


from SLMtools.classes.normalisedparameters import NormalisedBuildParameters
from SLMtools.classes.normalisedparameters import normalise

if __name__ == '__main__':
    buildset = BuildSet(testing = True)
    buildset.list_contents()
