# -*- coding: utf-8 -*-
"""
SLMtools.buildparameters:
========================
    Build parameters class object

Created on Fri Jan 29 11:00:51 2016
@author: dhancock
"""

class BuildParameters:
    '''
    Object to contain SLM build parameters and results from a build
    '''
    import SLMtools.classes
    from SLMtools.classes.beam import Beam
    from SLMtools.classes.material import Material
    from SLMtools.classes.part import Part
    from SLMtools.classes.results import Results
    from SLMtools.classes.comments import Comments
    
    from SLMtools.calculators import normalise
    
    from SLMtools.write import build_to_csv as export_csv
    from SLMtools.write import build_to_dict as export_dict
    #from SLMtools.read import xlsx_to_build as import_xlsx
    


    contents = {'date':'build date',
                'machine':'machine',
                'location':'location',
                'operator':'operator',
                'number':'build number',
                'file':'file name',
                'layerthickness':'layer thickness',
                'bedtemperature':'bed temperature',
                'materialname':'material name'}

    def __init__(self,testing = False):

        for item in self.contents:
            self.__dict__[item] = '{:} not given'.format(self.contents[item])

        self.comments = self.Comments()
        self.part = self.Part()
        self.beam = self.Beam()
        self.material = self.Material()
        self.results = self.Results()

        if testing is True:
            print('#'*8,'Using test build parameters','#'*8)

            self.date = 'TEST'
            self.number = '1'
            self.mtt_file = '20160118_??'
            self.layerthickness = 30e-6
            self.bedtemperature = 25

            self.comments = self.Comments(testing = True)
            self.part = self.Part(testing = True)
            self.beam = self.Beam(testing = True)
            self.material = self.Material(testing = True)


    def get_relative_density(self,verbose = False):
        try:
            print("relative density already given as {:f}".format(
                                                self.relative_density))
            return
        except:
            pass
        try:
            parentdensity = self.material.density
        except:
            if verbose is True:
                print('parent material density: {}'.format(
                                                    self.material.density))
            else:
                pass
        try:
            self.results.relative_density=self.results.density/parentdensity
        except:
            if verbose is True:
                print('part absolute density: {}'.format(self.results.density))
            else:
                pass
        return

    def set_parameter(self,parameter_name,value,verbose = True):
        success = False
        for section in [self,
                        self.beam,
                        self.part,
                        self.material,
                        self.comments,
                        self.results]:
            
            i = dict(zip(section.contents.values(),
                         section.contents.keys()))
            if parameter_name in i.keys():
                section.__dict__[i[parameter_name]] = value
                success = True
        if success is True:
            if verbose is True:
                print('Set {} as {}'.format(parameter_name,value))
        else:
            print('{} not found'.format(parameter_name))
        return
        
    def get_energydensity(self):
        from SLMtools.calculators.energydensity import energydensity
        self.energydensity = energydensity(self)
        return self.energydensity
        
    def list_contents(self, 
                      results=True, 
                      normalised=False):
        """ 
        Lists contents of a build parameter object, normalising if requested 
        """
        
        print()
        print('_'*70)
        print(self.date,':',self.location,':',self.number,':',self.part.number)
        print()

        ## remove unwanted groups of values and normalise if needed
        groups = list(self.__dict__.keys())
        if normalised is False and 'normalised' in groups:
            groups.pop(groups.index('normalised'))
        elif normalised is True and 'normalised' not in groups:
            self.normalise()
            groups.append('normalised')
            
        if results is False and 'results' in groups:
            groups.pop(groups.index('results'))
        
        ## list contents
        for group in sorted(groups):
            print(group,'=',self.__dict__[group])
            if '__dict__' in dir(self.__dict__[group]):
                for value in sorted(self.__dict__[group].__dict__.keys()):
                    print('\t{0:20} = {1:45}{2:20}'.format(
                        value,
                        str(self.__dict__[group].__dict__[value]),
                        str(type(self.__dict__[group].__dict__[value]))))
            print()

        
if __name__ == '__main__':
    import SLMtools
    build = SLMtools.BuildParameters(testing = True)
    #build.normalise()
    #build = BuildParameters()
    #build.list_contents(normalised=True, results=True)
    #build2=SLMtools.BuildParameters()
    #build2.import_excel("F:/Python/Scripts/data/SLMtools/Ta_Birmingham_20161003.xlsx",2)
    #build2.list_contents()
    #dictionary = build.build_to_dict(clean=True)
    build.export_csv('./build.csv')
    #print(dictionary)
