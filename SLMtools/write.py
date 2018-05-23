# -*- coding: utf-8 -*-
""" write.py

writes SLMtools data to various file formats 

"""

def buildset_to_csv(self,
                filename):
    
    ## import the first build to dict get keys
    data = self.builds[0].export_dict()

    # turn values into list
    for row in data:
        data[row] = [data[row]]
    
    # append values from remaining builds to data
    for build in self.builds[1:]:
        for row in data:
            data[row].append(build.export_dict()[row])

    # stitch together, blanking out missing values                                
    for row in data:
        for i, value in enumerate(data[row]):
            if 'not given' in str(value):
                data[row][i] = ''
        data[row] = ','.join([str(i) for i in data[row]])

    # write text file        
    with open(filename, 'w') as f:
        f.writelines(
            ['{:},{:}\n'.format(row,data[row]) for row in sorted(data)])
    return
    
def buildset_to_csv_rows(self,filename):
    headers = ','.join([str(x) for x in self.builds[0].export_dict().keys()])+'\n'
    # print(headers)
    rows = []
    for build in self.builds:
        data = build.export_dict()
        for x in data:
            if 'not given' in str(data[x]):
                data[x] =''
        row = ','.join([str(data[x]) for x in data])+'\n'
        rows.append(row)
        # print(row)
    
    with open(filename,'w') as f:
        f.write(headers)
        f.writelines(rows)
    
    return
    
def build_to_dict(self,
                  clean = False):
    build = {}
    build['material'] = self.material.name
    build['material supplier'] = self.material.supplier
    for section in [self,
                    self.part,
                    self.beam,
                    self.comments,
                    self.results]:
        for item in section.contents:
            value = section.__dict__[item]
            if 'not given' in str(value) and clean is True:
                pass
            else:
                build[section.contents[item]] = value
    return build
    
def build_to_csv(self,filename):
    data = self.export_dict()
    text = ''
    for row in data:
        text = text + '{}, {}\n'.format(row, data[row])
    with open(filename,'w') as f:
        f.write(text)