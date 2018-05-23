# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:16:17 2016

@author: dhancock
"""

class Part():
    contents = {'name':'part name',
                'number':'part number'}

    def __init__(self, testing = False):
        for item in self.contents:
            self.__dict__[item] = '{:} not given'.format(self.contents[item])

        if testing is True:
            self.name = 'test'
            self.description = 'test part'
            self.number = 1.1