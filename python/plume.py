#nmoisseeva@eoas.ubc.ca
#March 2019

import numpy as np
import os.path
import glob

#input values for plume analysis
#--------------------------------
wrfdir = '../complete/'
figdir = './figs/'
lvl = np.arange(0,2800,40)         #vertical levels in m
dx = 40.                        #horizontal grid spacing

cs = 10                         #+/- grids for cross-section
wi, wf= 25,375 

ign_over = 20                    #number of history intervals to skip from beginning: 10min (600/15sec) or ignition (ceil(95sec / 15sec))

# dirlist = os.listdir(wrfdir+'interp/')     #get all files in directory
dirpath = wrfdir+'interp/wrfinterp_*'
dirlist = glob.glob(dirpath) #get all  interp files in directory
tag = [i[len(dirpath)-1:-4] for i in dirlist]    #W*S*F*R0

#lists of rns
fireline_runs = ['W4F7R4L1','W4F7R4','W4F7R4L4']

#common functions
#--------------------------------
#tag reading function read_tag(variable type, string array)
def read_tag(str_tag, str_array):
    import re
    out_array = []
    for nTag,tag in enumerate(str_array):
        letters = re.split('\d+', tag)
        numbers = re.findall('\d+', tag)
        if str_tag=='W':
            out_array.append(int(numbers[0]))
        elif str_tag=='S':
            if 'Sn' in letters:
                out_array.append(int(numbers[1])*-1)
            else:
                out_array.append(int(numbers[1]))
        elif str_tag=='F':
            out_array.append(int(numbers[2]))
    out_array = np.array(out_array)
    return out_array
                                                                                                                                                                    
