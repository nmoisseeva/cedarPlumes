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
do_animations = 1
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
        ncdict = wrf.extract_vars(wrfdata, None, ('GRNHFX','W','QVAPOR','T','PHB','PH','U','P','PB','V'))

        #get height and destagger vars
        zstag = (ncdict['PHB'] + ncdict['PH'])//9.81
        z = wrf.destagger(zstag,1)
        u = wrf.destagger(ncdict['U'],3)
        w = wrf.destagger(ncdict['W'],1)

        nT,nZ,nY,nX = np.shape(z)
        qinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        winterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        uinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        tinterp = np.empty((nT,len(plume.lvl),nY,nX)) * np.nan
        for t in range(nT):
            print('.... tsetp = %s/%s' %(t,nT))
            for y in range(nY):
                for x in range(nX):
                    z_t = z[t,:,y,x]
                    fq = interpolate.interp1d(z_t,ncdict['QVAPOR'][t,:,y,x],fill_value="extrapolate")
                    ft = interpolate.interp1d(z_t,ncdict['T'][t,:,y,x],fill_value="extrapolate")
                    fw = interpolate.interp1d(z_t,w[t,:,y,x],fill_value="extrapolate")
                    fu = interpolate.interp1d(z_t,u[t,:,y,x],fill_value="extrapolate")
                    qinterp[t,:,y,x] = fq(plume.lvl)
                    winterp[t,:,y,x] = fw(plume.lvl)
                    tinterp[t,:,y,x] = ft(plume.lvl)
                    uinterp[t,:,y,x] = fu(plume.lvl)
                    #interpdict = {'QVAPOR': qinterp, 'W':winterp, 'T':tinterp, 'U':uinterp,'P':pinterp, 'V':vinterp}
                    interpdict = {'QVAPOR': qinterp, 'W':winterp, 'T':tinterp, 'U':uinterp,'GRNHFX': ncdict['GRNHFX']}
        writefile = open(interppath, 'wb')
        pickle.dump(interpdict, writefile, protocol=4)
        writefile.close()
        print('Interpolated data saved as: %s' %interppath)
        wrfdata.close()

    #convert and average data-----------------------------------
    ghfx = interpdict['GRNHFX']/1000.             #convert to kW
    qvapor = interpdict['QVAPOR']*1000.        #convert to g/kg
    temp = interpdict['T']+300.             #add perturbation and base temperature
    w = interpdict['W']
    u = interpdict['U']

    #get dimensions
    dimt, dimy, dimx = np.shape(ghfx)
    print('Dimensions of data: %s x %s x %s:'%(dimt,dimy,dimx))
    xsx = int(round(dimy/2.))

    var_list = ['ghfx','qvapor','temp','w','u']
    csdict = {}

    for variable in var_list:
    #create fire cross-section
        if variable == 'ghfx':
            slab = vars()[variable][:,xsx-plume.cs:xsx+plume.cs,:]
            csdict[variable] = np.mean(slab,1)
        elif variable == 'qvapor':
            slab = vars()[variable][:,:,xsx-plume.cs:xsx+plume.cs,:]
            csdict[variable] = np.nansum(slab,2)   #using total, not average for vapour
        else:
            slab = vars()[variable][:,:,xsx-plume.cs:xsx+plume.cs,:]
            csdict[variable] = np.mean(slab,2)


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

    if do_animations:
         #--------------- animation of vertical velocity contours and water vapor-----------------------
        print('.....creating vertical crossection of W + H2O animation')
        fig = plt.figure(figsize=(6,6))
        ax = plt.gca()
        # create initial frame
        # ---w contours and colorbar
        cntrf = ax.contourf(csdict['w'][0,:,:], cmap=plt.cm.PRGn_r, levels=np.arange(-7,7.1,0.5))
        cbarf = fig.colorbar(cntrf, orientation='horizontal',fraction=0.046, pad=0.1)
        cbarf.set_label('vertical velocity $[m s^{-2}]$')
        ax.set_xlabel('x grid (#)')
        ax.set_ylabel('height AGL [m]')
        ax.set_xlim([0,dimx])
        # ---non-filled vapor contours and colorbar
        cntr = ax.contour(csdict['qvapor'][0,:,:], cmap=plt.cm.Greys,levels=np.arange(0,2.1,0.3),linewidths=2)
        # ains = inset_axes(plt.gca(), width='40%', height='2%', loc=1)
        # cbar = fig.colorbar(cntr, cax=ains, orientation='horizontal')
        # cbar = fig.colorbar(cntr,  orientation='horizontal')
        # cbar.set_label('$H_2O$ mixing ratio $[g kg^{-1}]$',size=8)
        # cbar.ax.tick_params(labelsize=8)
        # ---heat flux
        axh = ax.twinx()
        axh.set_ylabel('ground heat flux $[kW m^{-2}]$', color='r')
        axh.set_ylim([0,140])
        axh.set_xlim([0,dimx])
        axh.tick_params(axis='y', colors='red')
        ln = axh.plot(csdict['qvapor'][0,:], 'r-')

        def update_plot(n,csdict,cntrf,cntr):
            ax.clear()
            cntrf = ax.contourf(csdict['w'][n,:,:],cmap=plt.cm.PRGn_r, levels=np.arange(-7,7.1,0.5),extend='both')
            cntr = ax.contour(csdict['qvapor'][n,:,:], cmap=plt.cm.Greys,levels=np.arange(0,2.1,0.3),linewidths=0.6)
            ax.set_xlabel('x grid (#)')
            ax.set_ylabel('height AGL [m]')
            ax.set_yticks(np.arange(0,len(plume.lvl),10))
            ax.set_yticklabels(plume.lvl[::10])
            axh.clear()
            axh.set_ylim([0,140])
            axh.set_xlim([0,dimx])
            ln = axh.plot(csdict['ghfx'][n,:], 'r-')
            axh.set_ylabel('ground heat flux $[kW m^{-2}]$', color='r')
            # time_text.set_text('Time (sec) = %s' %(n*dt))
            return cntrf, ln, cntr,

        #plot all frames
        ani=animation.FuncAnimation(fig, update_plot, dimt, fargs=(csdict,cntrf,cntr), interval=3)
        ani.save(plume.figdir + 'anim/w/%s.mp4' %Case, writer='ffmpeg',fps=10, dpi=250)
        plt.close()
        print('.....saved in: %s' %(plume.figdir + 'anim/w/%s.mp4' %Case))

    #writefile = open(interppath, 'wb')
    #pickle.dump(interpdict, writefile, protocol=4)
    #writefile.close()
    #print('Interpolated data saved as: %s' %interppath)
