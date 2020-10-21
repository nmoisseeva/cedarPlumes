# nmoisseeva@eoas.ubc.ca
# August 2020

import numpy as np
from scipy.io import netcdf
from scipy import interpolate
import os.path
import wrf
import sys
import imp
import zarr
import xarray as xr

#====================INPUT===================
#loc_tag = ['W5F7R7T']
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
    interppath = plume.wrfdir + 'interp/zarr/' + Case

    if os.path.isfile(interppathtar):
        print('Interpolated data found at: %s' %interppath)
        interpxr = xr.open_zarr(interppath)

    else:
        print('WARNING: no interpolated data found - generating: SLOW ROUTINE!')
        wrfpath = plume.wrfdir + 'wrfout_' + Case
        wrfdata = netcdf.netcdf_file(wrfpath, mode ='r')
        ncdict = wrf.extract_vars(wrfdata, None, ('GRNHFX','W','QVAPOR','T','PHB','PH','U','P','PB','V','tr17_1'),meta=False)
        ncdict['PM25'] = ncdict.pop('tr17_1')

        #get height and destagger vars
        print('.....destaggering')
        zstag = (ncdict['PHB'] + ncdict['PH'])//9.81
        z = wrf.destagger(zstag,1)
        u = wrf.destagger(ncdict['U'],3)
        w = wrf.destagger(ncdict['W'],1)
        v = wrf.destagger(ncdict['V'],2)
        
        #list variables to interpolate
        nT,nZ,nY,nX = np.shape(z)
        winterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        uinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        tinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        vinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        pminterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        
        print('.....interpolating:')
        for t in range(nT):
            print('.......... timestep = %s/%s' %(t,nT))
            for y in range(nY):
                for x in range(nX):
                    z_t = z[t,:,y,x]
                    ft = interpolate.interp1d(z_t,ncdict['T'][t,:,y,x],fill_value="extrapolate")
                    fw = interpolate.interp1d(z_t,w[t,:,y,x],fill_value="extrapolate")
                    fu = interpolate.interp1d(z_t,u[t,:,y,x],fill_value="extrapolate")
                    fv = interpolate.interp1d(z_t,v[t,:,y,x],fill_value="extrapolate")
                    fpm = interpolate.interp1d(z_t,ncdict['PM25'][t,:,y,x],fill_value="extrapolate")
                    winterp[t,:,y,x] = fw(plume.lvl)
                    tinterp[t,:,y,x] = ft(plume.lvl)
                    uinterp[t,:,y,x] = fu(plume.lvl)
                    vinterp[t,:,y,x] = fv(plume.lvl)
                    pminterp[t,:,y,x] = fpm(plume.lvl)
        interpdict = {'W': {'dims': ('time','z','y','x'),'data': winterp},\
                        'T':{'dims': ('time','z','y','x'),'data': tinterp},\
                        'U':{'dims': ('time','z','y','x'),'data': uinterp},\
                        'V':{'dims': ('time','z','y','x'),'data': vinterp},\
                        'PM25':{'dims': ('time','z','y','x'),'data': pminterp},\
                        'GRNHFX':{'dims': ('time','y','x'),'data': ncdict['GRNHFX']}}
        print('.....writing to zarr file')
        interpxr = xr.Dataset.from_dict(interpdict)
        interpxr.to_zarr(interppath)
        print('Interpolated data saved as: %s' %interppath)

    #convert and average data-----------------------------------
    ghfx = interpdict['GRNHFX']['data']/1000.             #convert to kW
    temp = interpdict['T']['data']+300.             #add perturbation and base temperature
    w = interpdict['W']['data']
    u = interpdict['U']['data']
    pm25 = interpdict['PM25']['data']

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
            csdict[variable] = {'dims': ('time','x'), 'data':np.mean(slab,1)}
        elif variable == 'pm25':   
            slab = vars()[variable]
            csdict[variable] = {'dims': ('time','z','x'),'data': np.sum(slab,2)}   #tracers calculated as cross-wind intergrated totals
        else:
            slab = vars()[variable][:,:,xsx-plume.cs:xsx+plume.cs,:]
            csdict[variable] = {'dims': ('time','z','x'), 'data': np.mean(slab,2)}
    csdict['ghfx2D'] = {'dims': ('time','y','x'), 'data': ghfx}

    cspath = plume.wrfdir + 'interp/zarr/cs_' + Case
    csxr = xr.Dataset.from_dict(csdict)
    csxr.to_zarr(cspath,mode='w')
    print('Crosssection data saved as: %s' %cspath)
