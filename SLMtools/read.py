# -*- coding: utf-8 -*-
""" read.py
Created on Fri Mar 17 14:03:49 2017

@author: dhancock
"""
import tkinter as tk
from tkinter import filedialog

def xlsx_to_builds(importfile):
    """
    imports a set of builds from a single excel file
    
    Keyword Arguments:
        - importfile: String with file path and name
    Returns:
        - builds: list of SLMtools.Buildparameters objects
    """
    from SLMtools import BuildParameters
    from xlrd import open_workbook

    ''' import data '''
    sheet = open_workbook(importfile).sheet_by_index(0)
    
    labels = [label.value for label in sheet.row(0)]
    rows = [[label.value for label in sheet.row(x)] \
                for x in range(1,len(sheet.col(0)))]
    
    ''' make a set of dicts with labels and values'''
    data = [{label.lower():row[i] for i,label in enumerate(labels)} \
                        for row in rows]
    #print(data)
    ''' assign values to build parameters in build objects'''
    builds = []
    for row in data:
        build = BuildParameters()
        for section in [build,
                        build.material,
                        build.beam,
                        build.part,
                        build.comments,
                        build.results]:
            for item,value in section.contents.items():
                try:
                    if row[value] is not "":
                        #print(item,'\t\t',row[value])
                        section.__dict__[item] = row[value]
                        #print(value,'\t',row[value])
                except:
                    #print("ping")
                    #print("{:50}.{:20}:{:30}:{:}".format(str(type(section)),item,value,'NOT FOUND'))
                    pass
        #print(build.material.name)        
        # calculate scan speed if necessary
        build.beam.getscanspeed()

        ## tidy up dates and numbers
        #for item in ('date','number'):
        for item in ('date'):
            try: build.__dict__[item] = int(build.__dict__[item])
            except: pass
	 
        #try: build.part.number = int(build.part.number)
        #except: pass
	 
        builds.append(build)
     
    print("\timported {:} builds from {:}".format(len(builds),importfile))
    #[print(build.material.name) for build in builds]
    return builds

'''
def xlsx_to_build(self, 
                 filename,
                 row=1):
    """ imports a single, selected build from a spreadsheet
    
    """
    from SLMtools import BuildSet

    temp_buildset = BuildSet()
    temp_buildset.import_excel(importfile=filename)

    print("importing column {:} from {:}".format(row,filename))
    print("\tbuild #'s {}".format(
        [build.number for build in temp_buildset.builds]))
    print("\tpart #'s  {}".format(
        [build.part.number for build in temp_buildset.builds]))
    
    build = temp_buildset.builds[row-1]
    for item in build.__dict__:
        self.__dict__[item] = build.__dict__[item]
    return
'''


def xlsx_to_buildset(self,
                     files = None,
                     testing = False,
                     verbose = False,
                     materialsource = 'auto'):
    """
    imports build parameters from one or more excel files and adds them to the
    BuildSet object, using xlsx_to_builds()
    """
                    
    if testing is True:
        files = ('../sampledata/sampledata.xlsx')
    if files is None:   
        print('Opening file selection dialogue...')

        root = tk.Tk()
        #root.lift()
        root.withdraw()
        files = filedialog.askopenfilenames(
                        #initialdir='./',
                        title = "Select buildset spreadsheet to open",
                        initialdir = 'F:/Python/Scripts/data/SLMtools',
                        filetypes = [('Buildset spreadsheet','*.xlsx')])
        root.destroy()
    elif type(files) is str:
        files = (files,)
    else:
        pass            
    if verbose is True:
        print('Importing: {}'.format(files))

    builds = []
    for file in files:
        builds = builds + xlsx_to_builds(file)
    self.builds = builds
   
    # give the buildset a name, if you can"
    try:
        self.name = ', '.join([f[f.rfind('/')+1:f.rfind('.')] for f in files])
    except:
        self.name = "no buildset name given"

    # record where you got the data!
    self.sourcefile = files
    
    # try to import material
    try:
        import_material(self,materialsource)
    except:
        if type(materialsource) is str:
            print("xls_to buildset: could not import material data from",materialsource)
        else: 
            print("xls_to buildset: could not import material data from materialsource")
        #raise

    return self.builds
    
def import_material(self,materialsource,verbose=False):
    """ adds material property data to a buildset object
    
    """
    from materialtools import Material, MaterialData
    
    if materialsource == 'auto':
        materialsource = '../resources/material_properties.txt'
        print('\nread.import_material():',
              'Trying to automatically import material data',
              'from {}\n'.format(materialsource))

    elif type(materialsource) is str:
        try:
            with open(materialsource,'r') as f:
                f.close()
                pass
        except FileNotFoundError:
            print('{} not found, '.format(materialsource)+
                'Opening file selection dialogue...')
    
            root = tk.Tk()
            root.withdraw()
            materialsource = filedialog.askopenfilename(
                        #initialdir='./',
                        title = "Select material property text file",
                        initialdir = 'F:/Python/Scripts/data/SLMtools',
                        filetypes = [('Material property file','*.txt')])
    elif type(materialsource) not in (Material, MaterialData):
        print("materialsource must be either a path to a file,",
              "a materialtools.Material or materialtools.MaterialData",
              "object containing the correct material property data")
        

    for build in self.builds:
        try:
            materialname = build.material.name
        except:
            print("build has no material name")
            raise
        try:
            build.material.import_material(materialname = materialname,
                                           source = materialsource)
        except:
            print(
            "read.import_material(): unable to import material properties"+
            " from {}".format(materialsource))
            raise

    return [build.material for build in self.builds]
    
    
if __name__ == "__main__":
    import SLMtools
    #buildset = SLMtools.BuildSet()
    builds = xlsx_to_builds("/python/data/SLMtools/buildsets/Mo_Birmingham_20160700_Tekna.xlsx")

 