# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:03:42 2016

@author: dhancock
"""

class Beam():
    """ .. class:: beam parameters
    
    describes the following parameters:
        'power':'beam power',
        'coupling':'beam coupling',
        'radius':'beam spot radius',
        'hatchspacing':'hatch spacing',
        'hatchdescription':'hatch description',
        'pointdistance':'point distance',
        'exposuretime':'exposure time',
        'focusoffset':'focus offset',
        'idlespeed':'idle speed',
        'scanspeed':'scan speed'
    
    """
    contents = {'power':'beam power',
                'coupling':'beam coupling',
                'radius':'beam spot radius',
                'hatchspacing':'hatch spacing',
                'hatchdescription':'hatch description',
                'pointdistance':'point distance',
                'exposuretime':'exposure time',
                'focusoffset':'focus offset',
                'idlespeed':'idle speed',
                'scanspeed':'scan speed'}

    def __init__(self, testing = False,**kwargs):

        for item in self.contents:
            if item in kwargs.keys():
                self.__dict__[item] = kwargs[item]
            else:
                self.__dict__[item] = '{:} not given'.format(
                                                    self.contents[item])
        
        if testing is True:
            self.coupling = 0.388
            self.power = 200
            self.radius = 25e-6
            self.hatchspacing = 25e-6
            self.hatchdescription = 'meander'
            self.pointdistance = 35e-6
            self.exposuretime = 150e-6
            self.focusoffset = 0
            self.idlespeed = 2.5
            self.getscanspeed()

    def getscanspeed(self):
        "calculates an equivalent continuous scan speed for a pulsed laser system"
        if type(self.scanspeed) is not str:
            #print('scan speed is already defined as {:} m/s'\
            #                                .format(self.scanspeed))
            return

        try:
            if self.idlespeed == 'not given':
                self.idlespeed = 2.5
                print('using default idle speed (',
                                                 self.idlespeed,')',sep='')
            idletimeperm = 1 / self.idlespeed
            pointsperm = 1 / self.pointdistance
            totalexposuretimeperm = self.exposuretime * pointsperm
            totaltimeperm = totalexposuretimeperm + idletimeperm
            speed = 1 / totaltimeperm
            self.scanspeed = speed
        except:
            print('scan speed not calculated:')
            print('\t{:}'.format(self.idlespeed))
            print('\t{:}'.format(self.pointdistance))
            print('\t{:}'.format(self.exposuretime))
            self.scanspeed = 'scan speed not calculated'
