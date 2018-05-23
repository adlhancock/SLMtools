# -*- coding: utf-8 -*-
"""

material class for SLMtools

Created on Fri Jan 29 11:01:36 2016

@author: dhancock
"""
import materialtools

class Material:
    contents = {'supplier':'powder supplier',
                'name':'material name',
                'shortname':'material abbreviation',
                'conductivity':'thermal conductivity',
                'density':'density',
                'specificheat':'specific heat',
                'liquidus':'melting point',
                'referencetemp':'reference temperature',
                'thermalexpansion':'thermal expansion coefficient',
                'diffusivity':'diffusivity'}
    material_abbreviations = {'Tungsten':'W', 
                              'Molybdenum':'Mo', 
                              'Tantalum':'Ta',
                              'Vanadium':'V',
                              'Copper':'Cu'}

    
    def __init__(self, testing = False):
        for item in self.contents:
            self.__dict__[item] = '{:} not given'.format(self.contents[item])

        if testing is True:
            self.name = 'Molybdenum'
            self.shortname = self.material_abbreviations[self.name]
            self.supplier = 'test supplier'
            print('#'*8,
                  'using testing material properties for',self.name,
                  '#'*8)
            self.conductivity = 138
            self.density = 10200
            self.specificheat = 250
            self.liquidus = 2620
            self.referencetemp = 20
            self.thermalexpansion = 5.43
            self.getdiffusivity()

    def getdiffusivity(self):
        try:
            self.diffusivity = self.conductivity / (
                                        self.density * self.specificheat)
        except:
            print('Could not calculate diffusivity for {}:'.format(self.name))
            for value in ['conductivity','density','specificheat']:
                print('\t{:} = {:}'.format(value,self.__dict__[value]))

    def import_material(self,
                    materialname=None,
                    source = None,
                    referencetemperature = 20,
                    verbose = False,
                    testing = False):
        '''
        imports material properties from a text file or matml formatted
        material data dict object 
        - see `materialtools` for details of the latter.
        '''
        stnetnoc = {value:key for key,value in self.contents.items()}
        
        if testing is True: 
            print("*"*80)
            print("TESTING")
            print("*"*80)
            source = "../../sampledata/material_properties.txt"
        
        if materialname is None:
            try:                 
                materialname = self.name
            except: 
                print("material name not defined")
                materialname = "Enter it now: "
        
        
        # try to turn source into a materialdata object
        if type(source) is str:
            textfile = source
            from materialtools.read import textfile as import_textfile
            if verbose is True: print('v: importing {}'.format(textfile))
            materialdataobj = import_textfile(textfile)
        elif type(source) is materialtools.Material:
            materialdataobj = materialtools.MaterialData()
            materialdataobj[source["MaterialName"]] = source
        elif type(source) is materialtools.MaterialData:
            materialdataobj = source
        else: print("incorrect source format")
        
        # try and extract the material we need
        try: 
            materialobj = materialdataobj[materialname]
            # self.materialobj = materialobj
            #materialobj.list_contents()
        except KeyError: 
            print(materialname, "not found in source")
            print("source is ",type(materialdataobj))

            
        self.name = materialobj["MaterialName"]
        try: self.shortname = self.material_abbreviations[self.name]
        except: print("no abbreviation for {} found".format(self.name))
        self.referencetemp = referencetemperature

        # renaming materialobj for clarity.
        material = materialobj
        
        if verbose is True: print("v: importing {} from {}".format(material.name,source))                                 

        values = {}

        """
        create a dictionary of {"lower case name":"Title Case Name"} 
        for all the parameters in the material
        """        
        
        for propertyname in material.keys():            # go through all the available properties from the imported material
            #print(propertyname,':',propertyname.lower())
            #print(propertyname.)
            if propertyname.lower() in self.contents.values(): # if it's one of the ones we need...

                if verbose is True:
                    print('importing',propertyname,'from',materialname)
                    
                if "Values" in material[propertyname]:
                    
                    if 'Temperature' in material[propertyname]:
                        print(propertyname,'is temperature dependant')
                        temperaturevalues = material[
                                                propertyname][
                                                'Temperature'][
                                                'Values']
                        #print(temperaturevalues)
                        if referencetemperature in temperaturevalues:
                            index = material[
                            propertyname][
                            'Temperature'][
                            'values'].index(referencetemperature)
                            values[propertyname] = material[
                                        propertyname][
                                        propertyname][
                                        'values'][index]
                            print(propertyname,'=',
                                  values[propertyname],
                                  '@',referencetemperature)

                        else: #reference temp not present
                            nearesttemp = min(temperaturevalues,
                                  key = lambda x: abs(x-referencetemperature))
                            index = temperaturevalues.index(nearesttemp)
                            values[propertyname] = (
                                material[propertyname][propertyname]\
                                                        ['Values'][index])
                            print(propertyname,
                            'not present @',referencetemperature,
                            '\n\tnearest value taken',
                            '(',material[propertyname][propertyname]\
                                                        ['Values'][index],
                              '@',temperaturevalues[index],')')
                    else: # not temperature dependent
                        if verbose is True:
                            print('#'*3,'Imported',propertyname,
                                  'is not temperature dependent:')
                            print('\treference temperature',
                                  '({:})'.format(referencetemperature),
                                  'may not match')

                        values[propertyname] = material[propertyname][propertyname]['Values']
                else:
                    values[propertyname] = material[propertyname]
            
                try:
                    vals = values[propertyname]
                    self.__dict__[stnetnoc[propertyname.lower()]] = vals
                    if verbose is True:
                        print("SUCCSESS: imported", 
                              propertyname.lower(),'[{}]\n'.format(vals))
                except:
                    if verbose is True: 
                        print('could not import {}'.format(propertyname))
                    raise

        self.getdiffusivity()

        return materialdataobj

    def list_contents(self):
        print('_'*65)
        print("listing contents of",self.name,':')
        print('-'*65)
        for item in sorted(self.__dict__.keys()):
            try:
                print('{0:30} {1:<40.5g}'.format(
                    self.contents[item],self.__dict__[item]))
            except:
                print('{0:30} {1:<40}'.format(
                    self.contents[item],self.__dict__[item]))
        print('_'*65)


if __name__ == '__main__':

    test = Material()
    test.list_contents()

    W = Material()
    materialdataobj = W.import_material(materialname='Tungsten',
                                               testing=True)
    W.list_contents()

    Mo = Material()
    materialdataobj = Mo.import_material(materialname='Molybdenum',
                                               testing=True)
    Mo.list_contents()