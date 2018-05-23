# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:28:52 2016

@author: dhancock
"""

class Comments():
    contents = {'pre_build':'pre-build comments',
                'post_build':'post-build comments'}

    def __init__(self, testing = False):
        for item in self.contents:
            self.__dict__[item] = '{:} not given'.format(self.contents[item])
        '''
        self.pre_build = 'no_comments'
        self.post_build = 'no_comments'
        '''

        if testing is True:
            self.pre_build = 'pre-build test comment'
            self.post_build = 'post-build test comment'
