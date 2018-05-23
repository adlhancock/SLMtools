# -*- coding: utf-8 -*-
"""

SLMtools Results class

Created on Thu Oct 20 14:17:19 2016

@author: dhancock
"""

class Results():
    contents = {'density':'part absolute density',
                'relative_density':'part relative density',
                'porosity':'part porosity',
                'hardness':'part hardness',
                'youngs_modulus':"Young's modulus",
                'thermal_conductivity':'thermal conductivity'}

    def __init__(self, testing = False,**kwargs):
        for item in self.contents:
            if item in kwargs.keys():
                self.__dict__[item] = kwargs[item]
            else:
                self.__dict__[item] = '{:} not given'.format(
                                                    self.contents[item])
        if testing is True:
            pass

    def get_porosity(self):
        try: self.porosity = 1/self.relative_density
        except: print("could not get porosity")
    
    def list_results(self):
        for result in self.__dict__:
            if 'not given' not in str(self.__dict__[result]):
                print('{:10s}:{:10}'.format(result, self.__dict__[result]))