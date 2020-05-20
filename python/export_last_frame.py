# nmoisseeva@eoas.ubc.ca
# January 2018

import numpy as np
import os.path
import sys
import pickle
import imp
#====================INPUT===================
#loc_tag = [str(sys.argv[1])]
#=================end of input===============
import plume        #all our data

#====================INPUT===================
#all common variables are stored separately
imp.reload(plume)     #force load each time
#=================end of input===============

loc_tag = plume.tag

print('INTERPOLATION AND AVERAGING SCRIPT FOR PLUME RUNS')
print('===================================')

for nCase,Case in enumerate(loc_tag):
    print('Examining case: %s ' %Case)
    #----------check for interpolated data----------------------------
    interppath = plume.wrfdir + 'interp/wrfinterp_' + Case + '.npy'
    #wrfpath = wrfdir + 'wrfout_' + Case
    #wrfdata = netcdf.netcdf_file(wrfpath, mode ='r')

    if os.path.isfile(interppath):
        '''
        print('Interpolated data found at: %s' %interppath)
        interpdict = np.load(interppath).item()   # load here the above pickle
        ncdict = wrf.extract_vars(wrfdata, None, ('GRNHFX'))
        '''

        print('Interpolated data found at: %s' %interppath)
        interpfile = open(interppath,'rb')
        interpdict = pickle.load(interpfile)   # load here the above pickle

    else:
        print('No interpolated data found: run submit_interp.bash first!')
        sys.exit()

    #save data-----------------------------------
    var_list = ['GRNHFX','T','U','V','W','PM25']
    enddict = {}

    for variable in var_list:
        if variable == 'GRNHFX':
            enddict[variable] = interpdict[variable][-1,:,:]
        else:
            enddict[variable] = interpdict[variable][-1,:,:,:]
    
    endpath = plume.wrfdir + 'interp/end/wrfend_' + Case + '.npy'
    np.save(endpath,enddict)
    print('Last frame data saved as: %s' %endpath)

