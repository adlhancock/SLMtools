# -*- coding: utf-8 -*-
"""

BuildSet class for SLMtools

Created on Fri Jan 29 10:55:52 2016

@author: dhancock
"""

class BuildSet:
    '''
    Set of build parameters for multiple builds:
    contains .name string and a .builds list object
    '''
    from SLMtools.read import xlsx_to_buildset as import_xlsx
    from SLMtools.write import buildset_to_csv as export_csv   
    from SLMtools.write import buildset_to_csv_rows as export_csv_rows

    def __init__(self, testing = False):

        from SLMtools import BuildParameters
        
        self.name = 'Unnamed build set'
        self.builds = [BuildParameters()]
        #self.builds.append(BuildParameters())
        self.sourcefile = "no source file"

        if testing is True:
            print('#'*8,'using test buildset parameters','#'*8)
            self.name = 'testing BuildSet'
            self.builds = [BuildParameters(testing = True),
                           BuildParameters(testing = True)]

    def dedupe(self,
               force=False):
        buildnumbers = []
        unique_parameters= []

        if force is False:
            confirmation = input(
                "are you sure you want to dedupe this buildset? [N,yes]")
            if confirmation not in ['yes','YES','Yes']:
                return
            
        for i, build in enumerate(self.builds):
            parameters = [build.beam.power,
                          build.beam.scanspeed,
                          build.beam.hatchspacing,
                          build.beam.hatchdescription,
                          build.layerthickness]
            if parameters not in unique_parameters:
                buildnumbers.append(i)
                unique_parameters.append(parameters)
        dedupedbuilds = [self.builds[x] for x in buildnumbers]
        self.builds = dedupedbuilds
        return

    def set_parameter(self,
                      parameter_name,
                      value,
                      buildnumbers = 'all',
                      verbose = True):
        success = False
        if buildnumbers == 'all':
            buildnumbers = [x for x,build in enumerate(self.builds)]
        for n in buildnumbers:
            build = self.builds[n-1]
            for section in [build,
                            build.beam,
                            build.part,
                            build.material,
                            build.comments,
                            build.results]:
                
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
        
    def list_contents(self,normalised=False, results=True):
        print('='*70)
        for item in sorted(self.__dict__.keys(), reverse = True):
            print('{0:10} = {1:10}'.format(item,str(self.__dict__[item])))
        for build in self.builds:
            build.list_contents(results,normalised)
        return

if __name__ == '__main__':
    #buildset = BuildSet(testing = True)
    buildset = BuildSet()
    filename = 'F:/Python/Scripts/data/SLMtools/Mo_Birmingham_20160200.xlsx'
    buildset.import_xlsx()
    buildset.export_csv('F:/buildset.csv')
