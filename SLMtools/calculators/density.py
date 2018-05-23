# -*- coding: utf-8 -*-
"""
tools for calculating density
Created on Wed Oct 26 13:51:10 2016

@author: dhancock
"""


def archimedes(mass_in_air,
                 mass_in_liquid,
                 density_material_theoretical,
                 density_liquid):
    """
    uses results from Archimedes measurements, including absolute uncertainty
    values, to provide part densities and percentage uncertainty. 
    
    Each variable must be given as a tuple in the form (value, uncertainty).
    
        Keyword Arguments:
            - mass_in_air:  measured mass of the part in air (mass, absolute uncertainty)
            - mass_in_liquid:  measured mass of the part when suspended in liquid (mass, absolute uncertainty)
            - density_material_theoretical: theoretical density of the material (density, absolute uncertainty)
            - density_liquid: density of the liquid used (density, absolute uncertainty)
        
        Returns:
            - (measured density of material / theoretical density of material), percentage error of density
        Formulae:
            
        
                mass_displaced_liquid = (mass_in_air[0]-mass_in_liquid[0],mass_in_air[1]+mass_in_liquid[1])
                
                density_material = density_liquid[0] * mass_in_air[0] / mass_displaced_liquid[0]
                
                Percentage error is calculated using sum in quadrature method.
        
    
    """
    mass_displaced_liquid = (mass_in_air[0]-mass_in_liquid[0],mass_in_air[1]+mass_in_liquid[1])
    density_material = density_liquid[0] * mass_in_air[0] / mass_displaced_liquid[0]
    
    measurements =   [density_liquid,
                      mass_in_air,
                      mass_displaced_liquid,
                      density_material_theoretical]
    
    pc_error_density = (sum([(x[1]/x[0])**2 for x in measurements]))**0.5
    
    return density_material / density_material_theoretical[0], pc_error_density


def experimental_error(buildset,
                        liquid = 'water',
                        mass_uncertainty_g = 0.01,
                        theoretical_density_uncertainty = 0.1):
    """
    estimates experimental uncertainty in archimedes measurements
    
    Keyword Arguments:
        - buildset - SLMtools.BuildSet object
        - liquid - currently only 'water' or 'ethanol' accepted
        - mass_uncertainty - error in mass measurement [g]
        - theoretical_density_uncertainty [g/cm^3]
    """
    if liquid == 'water':
        density_liquid = (0.998, 0.01)
    if liquid == 'ethanol':
        density_liquid = (0.789, 0.01)
    try:
        part_masses = [(b.part.mass, 0.01) for b in buildset.builds]
        theoretical_densities = [(b.material.density,0.1) for b in buildset.builds]
                
    except:
        print("cannot calculate errors: do not have mass for all components")

    mass_displaced_liquid = (mass_in_air/density_material_theoretical)*density_liquid
    measurements =  [density_liquid,
                      mass_in_air,
                      mass_displaced_liquid,
                      density_material_theoretical]
        
    pc_error_density = (sum([(x[1]/x[0])**2]for x in measurements))**0.5
    
    return