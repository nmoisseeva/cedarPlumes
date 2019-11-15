# nmoisseeva@eoas.ubc.ca
# January 2018

import numpy as np
from scipy.io import netcdf
from scipy import interpolate
import os.path
import wrf
import sys
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import animation
import imp
#====================INPUT===================
loc_tag = [str(sys.argv[1])]
#=================end of input===============
import plume        #all our data

#====================INPUT===================
#all common variables are stored separately
imp.reload(plume)     #force load each time
#=================end of input===============

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
        print('WARNING: no interpolated data found - generating: SLOW ROUTINE!')
        wrfpath = plume.wrfdir + 'wrfout_' + Case
        wrfdata = netcdf.netcdf_file(wrfpath, mode ='r')
        ncdict = wrf.extract_vars(wrfdata, None, ('GRNHFX','W','QVAPOR','T','PHB','PH','U','P','PB','V','tr17_1'))
        ncdict['PM25'] = ncdict.pop('tr17_1')

        #get height and destagger vars
        zstag = (ncdict['PHB'] + ncdict['PH'])//9.81
        z = wrf.destagger(zstag,1)
        u = wrf.destagger(ncdict['U'],3)
        w = wrf.destagger(ncdict['W'],1)
        v = wrf.destagger(ncdict['V'],2)
        
        #list variables to interpolate
        nT,nZ,nY,nX = np.shape(z)

        #qinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        winterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        uinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        tinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        vinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        pminterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan

        for t in range(nT):
            print('.... tsetp = %s/%s' %(t,nT))
            for y in range(nY):
                for x in range(nX):
                    z_t = z[t,:,y,x]
                    #fq = interpolate.interp1d(z_t,ncdict['QVAPOR'][t,:,y,x],fill_value="extrapolate")
                    ft = interpolate.interp1d(z_t,ncdict['T'][t,:,y,x],fill_value="extrapolate")
                    fw = interpolate.interp1d(z_t,w[t,:,y,x],fill_value="extrapolate")
                    fu = interpolate.interp1d(z_t,u[t,:,y,x],fill_value="extrapolate")
                    fv = interpolate.interp1d(z_t,v[t,:,y,x],fill_value="extrapolate")
                    fpm = interpolate.interp1d(z_t,ncdict['PM25'][t,:,y,x],fill_value="extrapolate")
                    #qinterp[t,:,y,x] = fq(plume.lvl)
                    winterp[t,:,y,x] = fw(plume.lvl)
                    tinterp[t,:,y,x] = ft(plume.lvl)
                    uinterp[t,:,y,x] = fu(plume.lvl)
                    vinterp[t,:,y,x] = fv(plume.lvl)
                    pminterp[t,:,y,x] = fpm(plume.lvl)
                    #interpdict = {'QVAPOR': qinterp, 'W':winterp, 'T':tinterp, 'U':uinterp,'P':pinterp, 'V':vinterp}
                    interpdict = {'W':winterp, 'T':tinterp, 'U':uinterp,'V':vinterp,'PM25':pminterp,'GRNHFX': ncdict['GRNHFX']}
        writefile = open(interppath, 'wb')
        pickle.dump(interpdict, writefile, protocol=4)
        writefile.close()
        print('Interpolated data saved as: %s' %interppath)
        wrfdata.close()

    #convert and average data-----------------------------------
    ghfx = interpdict['GRNHFX']/1000.             #convert to kW
    temp = interpdict['T']+300.             #add perturbation and base temperature
    w = interpdict['W']
    u = interpdict['U']
    pm25 = interpdict['PM25']

    #get dimensions
    dimt, dimy, dimx = np.shape(ghfx)
    print('Dimensions of data: %s x %s x %s:'%(dimt,dimy,dimx))
    xsx = int(round(dimy/2.))

    var_list = ['ghfx','temp','w','u','pm25']
    csdict = {}

    for variable in var_list:
    #create fire cross-section
        if variable == 'ghfx':
            slab = vars()[variable][:,xsx-plume.cs:xsx+plume.cs,:]
            csdict[variable] = np.mean(slab,1)
        elif variable == 'pm25':   
            slab = vars()[variable]
            csdict[variable] = np.sum(slab,2)   #tracers calculated as cross-wind intergrated totals
        else:
            slab = vars()[variable][:,:,xsx-plume.cs:xsx+plume.cs,:]
            csdict[variable] = np.mean(slab,2)
    csdict['ghfx2D'] = ghfx

    #create time-average around peak flux--------------------------
    xmax = np.argmax(csdict['ghfx'],axis=1)
    tavedict = {}

    for variable in var_list:
        tvar = []
        if variable == 'ghfx':
            for nP, pt in enumerate(xmax[plume.ign_over:]):             #excludes steps containing ignition
                subset = csdict[variable][plume.ign_over+nP,pt-plume.wi:pt+plume.wf]
                tvar.append(subset)
        else:
            for nP, pt in enumerate(xmax[plume.ign_over:]):             #excludes steps containing ignition
                subset = csdict[variable][plume.ign_over+nP,:,pt-plume.wi:pt+plume.wf]
                tvar.append(subset)
        tavedict[variable] = np.mean(tvar,0)

    avepath = plume.wrfdir + 'interp/wrfave_' + Case + '.npy'
    np.save(avepath, tavedict)
    print('Averaged data saved as: %s' %avepath)
    
    cspath = plume.wrfdir + 'interp/wrfcs_' + Case + '.npy'
    np.save(cspath,csdict)
    print('Crosssection data saved as: %s' %cspath)

