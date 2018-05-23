# -*- coding: utf-8 -*-
"""
scanspeed calculator for pulsed SLM system

Finds missing parameters from scan speed, exposure time, and point distance

Created on Thu Jan 14 14:01:47 2016

@author: dhancock
"""


def findspeed(exposuretime=150e-6,pointdistance=35e-6,idlespeed = 2.5):
    idletimeperm = 1 / idlespeed
    pointsperm = 1 / pointdistance
    totalexposuretimeperm = exposuretime * pointsperm
    totaltimeperm = totalexposuretimeperm + idletimeperm
    speed = 1 / totaltimeperm
    return [exposuretime,pointdistance,speed]
    
def findexposuretime(pointdistance = 35e-6, speed = 0.5, idlespeed = 2.5):
    #print('\n\n speed = ',speed,'\n\n')
    totaltimeperm = 1 / speed
    pointsperm = 1 / pointdistance
    idletimeperm = 1 / idlespeed
    totalexposuretime = totaltimeperm - idletimeperm
    exposuretime = totalexposuretime / pointsperm
    return [exposuretime,pointdistance,speed]
    
def findpointdistance(exposuretime = 150e-3 ,speed = 0.5, idlespeed = 2.5):
    totaltimeperm = 1 / speed
    idletimeperm = 1 / idlespeed
    totalexposuretime = totaltimeperm - idletimeperm
    pointsperm = totalexposuretime / exposuretime
    pointdistance = 1 / pointsperm    
    return [exposuretime,pointdistance,speed]

def findall(build = 'test'):
    if build == 'test':
        build = SLMtools.BuildParameters()
        [exposuretime,pointdistance,speed] = findexposuretime(
        build.beam.pointdistance,build.beam.scanspeed,build.beam.idlespeed)
        
        #print('\n\nexposuretime set as ',exposuretime)
        build.beam.exposuretime = exposuretime
    
    speed = build.beam.scanspeed
    #print(build.beam.exposuretime)
    exposuretime = build.beam.exposuretime
    
    pointdistance = build.beam.pointdistance
    if exposuretime == 'not given':
        exposuretime = findexposuretime(speed,pointdistance)[0]    
    if speed == 'not given':
        speed = findspeed(exposuretime,pointdistance)    
    if pointdistance == 'not given':
        pointdistance = findpointdistance(exposuretime,speed)
    
    build.beam.exposuretime = exposuretime
    build.beam.pointdistance = pointdistance
    build.beam.scanspeed = speed
    return build
    

if __name__ == '__main__':
    import SLMtools
    print('\nRunning scanspeedcalculator module as script:\n')
    print('exposuretime =>',findexposuretime())
    print('pointdistance => ',findpointdistance())
    print('speed =>',findspeed())
    build = findall()    
    print('all => [',
                   build.beam.exposuretime, 
                   build.beam.pointdistance, 
                   build.beam.scanspeed, 
                   ']')
