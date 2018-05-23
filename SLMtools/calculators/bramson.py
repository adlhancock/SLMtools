# -*- coding: utf-8 -*-
""" bramson laser coupling calculation tools.

Created on Fri Oct 28 15:34:53 2016

@author: dhancock
"""

def absorptivity(rho,wavelength=1070e-9):
    """
    calculates absorbtivity based on resistivity and wavelength
    """
    
    A = rho/wavelength
    return 0.365*(A)**0.5 - 0.0667*(A)+(A**3)**0.5

def resistivity(rho,T,factor,T0=293):
    """
    calculates temperature dependent resistivity
    """
    return rho*(1 + (T-T0)*factor)
    
    
if __name__ == '__main__':
    materials = ['W','Ta','Mo']
    resistivities = [resistivity(rho,293,factor) for rho,factor in zip([5.6e-8,5.2e-8,53.4e-9],[4.5e-3,0,0])]
    
    for material,rho in zip(materials, resistivities):
        print(material,' = ',absorptivity(rho))
        