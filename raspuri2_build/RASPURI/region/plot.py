#==========================================================================
#  COPYRIGHT NOTICE
#
#   RASPURI v2 of RASPURI a RASP(Regional Atmospheric
#   Soaring Predictions) COMPUTER PROGRAM
#   Original Creator: Oriol Cervelló i Nogués ( raspuri [at] protonmail.com )
#   Copyright 2019+ by Oriol Cervelló i Nogués, All rights reserved.
# 
#  This program and all scripts, data and information from RASPURI v2 
#  are the property of the creator and copyright holder and is not 
#  to be copied, modified, or distributed to others without obtaining the 
#  permission of the copyright holder during the life of the copyright holder.
#
#  Title to copyright in this program and any associated documentation
#  will at all times remain with the copyright holder until his death.
#
#  Upon the death of the original creator and copyright holder, 
#  this program and all RASPURI v2 programs, scripts, data and 
#  information are to be released under the terms of version 3 o
#  f the GNU General Public License. A copy of that license can 
#  also be obtained from the Free Software Foundation, Inc. on-line at
#  https://www.gnu.org/licenses/.
#==========================================================================
#==========================================================================
# plot_examples.py
# This script is part of RASPURI v2
# Script containing the ploting functions
import numpy as np
from PIL import Image
import os
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as arrsty
import rasterio
from rasterio.merge import merge
from matplotlib.colors import LightSource
from variables import DOTY,DOTX,DOTTITLE,TOPOFILES,PLOTTYPELAYER



#########################################################################
##################   IMAGE PLOTS
#########################################################################

def plot_strem_image(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy):
    try:
        #PLOT TOPO
        fig, ax = plt.subplots(figsize=(14,8),dpi=100)
        plt.rcParams.update({'font.size': 18})
        extent = [bounds.left,bounds.right , bounds.bottom , bounds.top]
        plt.imshow(ls.hillshade(mosaic[0,:,:], vert_exag=ve),extent=extent, cmap='gray',aspect='auto',interpolation='bessel')
        #PLOT DATA
        
        #strm = ax.streamplot(x,y,U,V,color=prop*3.6, density=1.8 ,linewidth=1.8,arrowsize=1.3, cmap='tab20b')
        #cbar = fig.colorbar(strm.lines)
        
        # Normalise the data for uniform arrow size
        u_norm = U / np.sqrt(U ** 2.0 + V ** 2.0)
        v_norm = V / np.sqrt(U ** 2.0 + V ** 2.0)
        sca=5
        CF=ax.contourf(x,y,prop*3.6,cmap="tab20b", alpha=0.30)
        q = ax.quiver(x[::sca,::sca], y[::sca,::sca], u_norm[::sca,::sca], v_norm[::sca,::sca], pivot='middle', alpha=1)        

        cbar = fig.colorbar(CF)
        cbar.ax.set_ylabel('[km/h]', fontsize=18)
        cbar.ax.tick_params(labelsize=18)

        plt.title(ptitle, loc='left')
        plt.figtext(0.99, 0.96, 'Valid for: '+valid_t, horizontalalignment='right') 
        UTC_time = time.gmtime()
        plt.figtext(0.99, 0.01, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
        plt.figtext(0.01, 0.01, 'RASPURI', horizontalalignment='left') 
        #ANOTATIONS
        ax.scatter(DOTX, DOTY,color='red')

        for i, txt in enumerate(DOTTITLE):
            ax.annotate(txt, (DOTX[i], DOTY[i]),fontsize=10)
        ##SAVE    
        plt.savefig(filename+'.png')
        plt.close()
    except Exception as e: 
        print('****Error ploting the '+ptitle+', plot.py****')
        print(e)

def plot_cont_image(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units):
    try:
        #PLOT TOPO
        fig, ax = plt.subplots(figsize=(14,8),dpi=100)
        plt.rcParams.update({'font.size': 18})
        extent = [bounds.left,bounds.right , bounds.bottom , bounds.top]
        plt.imshow(ls.hillshade(mosaic[0,:,:], vert_exag=ve),extent=extent, cmap='gray',aspect='auto',interpolation='bessel')
        #PLOT DATA
        CF=ax.contourf(x,y,prop_f,cmap=cmap, alpha=0.35,vmin=vmin,vmax=vmax)
        cbar = fig.colorbar(CF)
        cbar.ax.set_ylabel(units, fontsize=18)
        cbar.ax.tick_params(labelsize=18)
        if(prop is not None):
            CS = ax.contour(x, y, prop,colors='k')    
            ax.clabel(CS, fontsize=9, inline=1)
        plt.title(ptitle, loc='left')
        plt.figtext(0.99, 0.96, 'Valid for: '+valid_t, horizontalalignment='right') 
        UTC_time = time.gmtime()
        plt.figtext(0.99, 0.01, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
        plt.figtext(0.01, 0.01, 'RASPURI', horizontalalignment='left') 
        #ANOTATIONS
        ax.scatter(DOTX, DOTY,color='red')
        for i, txt in enumerate(DOTTITLE):
            ax.annotate(txt, (DOTX[i], DOTY[i]),fontsize=10)
        ##SAVE    
        plt.savefig(filename+'.png')
        plt.close()
    except Exception as e: 
        print('****Error ploting the '+ptitle+', plot.py****')
        print(e)

def plot_general_sce_image(U,V, prop_fclouds,prop_rain, prop, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy):
    try:    
        #PLOT TOPO
        fig, ax = plt.subplots(figsize=(14,11),dpi=100)
        plt.rcParams.update({'font.size': 18})

        extent = [bounds.left,bounds.right , bounds.bottom , bounds.top]
        plt.imshow(ls.hillshade(mosaic[0,:,:], vert_exag=ve),extent=extent, cmap='gray',aspect='auto',interpolation='bessel')

        #PLOT DATA
        u_norm = U / np.sqrt(U ** 2.0 + V ** 2.0)
        v_norm = V / np.sqrt(U ** 2.0 + V ** 2.0)
        sca=6
        q = ax.quiver(x[::sca,::sca], y[::sca,::sca], u_norm[::sca,::sca], v_norm[::sca,::sca], pivot='middle', alpha=1)


        CF4=ax.contourf(x,y,prop_rain,cmap='RdPu', alpha=0.45,vmin=0,vmax=np.max(prop_rain))
        CF1=ax.contourf(x,y,prop_fclouds,cmap='Blues', alpha=0.25,vmin=0,vmax=130)

        #clouds=(prop_fhigh+prop_fmid+prop_flow)*100
        #CF1=ax.contourf(x,y,np.clip(clouds,0,100),cmap='Blues', alpha=0.20,vmin=0,vmax=130)
        cbar = fig.colorbar(CF1)
        cbar.ax.set_ylabel('BL Cloud Cover[%]', fontsize=18)
        cbar.ax.tick_params(labelsize=18)
        
        cbar2 = fig.colorbar(CF4,orientation='horizontal')
        cbar2.ax.set_xlabel('Rain [mm]', fontsize=18)
        cbar2.ax.tick_params(labelsize=18)

        CS = ax.contour(x, y, prop,colors='k')    
        ax.clabel(CS, fontsize=9, inline=1)

        plt.title('General Scenario', loc='left')
        plt.figtext(0.99, 0.96, 'Valid for: '+valid_t, horizontalalignment='right') 
        UTC_time = time.gmtime()
        plt.figtext(0.99, 0.01, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
        plt.figtext(0.01, 0.01, 'RASPURI', horizontalalignment='left') 

        #ANOTATIONS
        ax.scatter(DOTX, DOTY,color='red')

        for i, txt in enumerate(DOTTITLE):
            ax.annotate(txt, (DOTX[i], DOTY[i]),fontsize=10)

        ##SAVE    
        plt.savefig(filename+'.png')
        plt.close()
    except Exception as e: 
        print('****Error ploting the general scenario, plot.py****')
        print(e)



#########################################################################
##################   LAYER PLOTS
#########################################################################

def plot_crop(filename):
    im = Image.open(filename+'.png')
    #w, h = im.size
    im.crop((1096, 26, 1385, 761)).save(filename+'L.png')
    im.crop((176, 97, 1043, 712)).save(filename+'.png')


def plot_cont_layer(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units):
    try:
        fig, ax = plt.subplots(figsize=(14,8),dpi=100)

        #PLOT DATA
        CF=ax.contourf(x,y,prop_f,cmap=cmap, alpha=0.35,vmin=vmin,vmax=vmax)
        cbar = fig.colorbar(CF)
        cbar.ax.set_ylabel(units, fontsize=18)
        cbar.ax.tick_params(labelsize=18)
        if(prop is not None):
            CS = ax.contour(x, y, prop,colors='k')    
            ax.clabel(CS, fontsize=9, inline=1)
        plt.figtext(0.99, 0.92, 'Valid for: \n'+valid_t, horizontalalignment='right',fontsize=14) 
        UTC_time = time.gmtime()
        plt.figtext(0.99, 0.05, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
        plt.figtext(0.93, 0.30, ptitle+'\n by RASPURI', horizontalalignment='center', rotation='vertical',fontsize=20) 

        ##SAVE    
        plt.savefig(filename+'.png', transparent=True)
        plt.close()
        plot_crop(filename)
    except Exception as e: 
        print('****Error ploting the '+ptitle+', plot.py****')
        print(e)


def plot_strem_layer(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy):
    try:
        fig, ax = plt.subplots(figsize=(14,8),dpi=100)

        #PLOT DATA
        # Normalise the data for uniform arrow size
        u_norm = U / np.sqrt(U ** 2.0 + V ** 2.0)
        v_norm = V / np.sqrt(U ** 2.0 + V ** 2.0)
        sca=4
        CF=ax.contourf(x,y,prop*3.6,cmap="tab20b", alpha=0.30)
        q = ax.quiver(x[::sca,::sca], y[::sca,::sca], u_norm[::sca,::sca], v_norm[::sca,::sca], pivot='middle', alpha=1)        

        cbar = fig.colorbar(CF)
        cbar.ax.set_ylabel('[km/h]', fontsize=18)
        cbar.ax.tick_params(labelsize=18)


        plt.figtext(0.99, 0.92, 'Valid for: \n'+valid_t, horizontalalignment='right',fontsize=14) 
        UTC_time = time.gmtime()
        plt.figtext(0.99, 0.05, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
        plt.figtext(0.93, 0.30, ptitle+'\n by RASPURI', horizontalalignment='center', rotation='vertical',fontsize=20)  

        ##SAVE    
        plt.savefig(filename+'.png', transparent=True)
        plt.close()
        plot_crop(filename)
    except Exception as e: 
        print('****Error ploting the '+ptitle+', plot.py****')
        print(e)


def plot_general_sce_layer(U,V, prop_fclouds,prop_rain, prop, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy):
    try:    

        fig, ax = plt.subplots(figsize=(14,8),dpi=100)

        #PLOT DATA
        u_norm = U / np.sqrt(U ** 2.0 + V ** 2.0)
        v_norm = V / np.sqrt(U ** 2.0 + V ** 2.0)
        sca=5
        q = ax.quiver(x[::sca,::sca], y[::sca,::sca], u_norm[::sca,::sca], v_norm[::sca,::sca], pivot='middle', alpha=1)

        CF4=ax.contourf(x,y,prop_rain,cmap='RdPu', alpha=0.45,vmin=0,vmax=np.max(prop_rain))
        CF1=ax.contourf(x,y,prop_fclouds,cmap='Blues', alpha=0.25,vmin=0,vmax=130)

        cbar = fig.colorbar(CF1)
        cbar.ax.set_ylabel('BL Cloud Cover[%]', fontsize=18)
        cbar.ax.tick_params(labelsize=18)
        
        CS = ax.contour(x, y, prop,colors='k')    
        ax.clabel(CS, fontsize=9, inline=1)

        plt.figtext(0.99, 0.92, 'Valid for: \n'+valid_t, horizontalalignment='right',fontsize=14) 
        UTC_time = time.gmtime()
        plt.figtext(0.99, 0.05, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
        plt.figtext(0.93, 0.30, 'General by RASPURI', horizontalalignment='center', rotation='vertical',fontsize=20) 

        ##SAVE    
        plt.savefig(filename+'.png', transparent=True)
        plt.close()
        plot_crop(filename)
    except Exception as e: 
        print('****Error ploting the general scenario, plot.py****')
        print(e)





def plot_cont(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units):
    if(PLOTTYPELAYER):
        plot_cont_layer(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    else:
        plot_cont_image(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)


def plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy):
    if(PLOTTYPELAYER):
        plot_strem_layer(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    else:
        plot_strem_image(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)

def plot_general_sce(U,V, prop_fclouds,prop_rain, prop, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy):
    if(PLOTTYPELAYER):
        plot_general_sce_layer(U,V, prop_fclouds,prop_rain, prop, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy)
    else:
        plot_general_sce_image(U,V, prop_fclouds,prop_rain, prop, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy


#########################################################################
##################   CALL TO PLOTS
#########################################################################

def plot_rasp(datadir,hour,valid_t,dx,dy,outdir):
    hour_i=int(hour)    
    #hour='_'+hour
    
    #########################################################################
    ##################   TOPO
    #########################################################################
    #https://visibleearth.nasa.gov/images/73934/topography
    try:
        topodir='../geog/topo/'
        flat = datadir+'lats.npy'
        flon = datadir+'lons.npy'
        lat = np.load(flat)
        lon = np.load(flon)
        x = np.linspace(np.min(lon),np.max(lon),lon.shape[1])
        y = np.linspace(np.min(lat),np.max(lat),lat.shape[0])
        dataset=[]
        x=lon
        y=lat

        for i, topo in enumerate(TOPOFILES):
            dataset.append(rasterio.open(topodir+'gebco_08_rev_elev_'+topo+'_grey_geo.tif'))

        bounds=rasterio.coords.BoundingBox(np.min(lon),np.min(lat) ,np.max(lon),np.max(lat) )
        with open(outdir+'bounds.txt', 'w') as f:
            print(str(bounds.left)+'\n'+str(bounds.right) +'\n'+str(bounds.bottom)+'\n'+str(bounds.top), file=f)
        mosaic, out_trans = merge(dataset,bounds)
        for i in range(0,len(dataset)):
            dataset[i].close()

        ls = LightSource(azdeg=315, altdeg=45)
        ve=0.7
    except Exception as e:
        print('****Error reading TOPO, plot.py****')
        print(e)
    #########################################################################
    ##################   PLT SURFACE WIND
    #########################################################################
    try:
        ptitle='Surface Wind'        
        fprop = datadir+'wspd10'+hour+'.npy'
        fprop2 = datadir+'wdir10'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'sfcwind_'+hour
        
    except Exception as e:
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    #########################################################################
    ##################   PLT LOW CLOUDS
    #########################################################################
    try:
        fprop_f = datadir+'cloudfrac_low'+hour+'.npy'
        prop_f = np.load(fprop_f)  
        prop_f[prop_f <= 0.15] ='nan'  
        #fprop = datadir+'slp'+hour+'.npy'
        #prop = np.load(fprop)
        filename=outdir+'cloudlow_'+hour
        ptitle='Clouds Low Level'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f*100,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT MID CLOUDS
    #########################################################################
    try:
        fprop_f = datadir+'cloudfrac_mid'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f <= 0.15] ='nan'
        #fprop = datadir+'slp'+hour+'.npy'
        #prop = np.load(fprop)
        filename=outdir+'cloudmid_'+hour
        ptitle='Clouds Mid Level'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f*100,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT HIGH CLOUDS
    #########################################################################
    try:
        fprop_f = datadir+'cloudfrac_high'+hour+'.npy'
        prop_f = np.load(fprop_f)  
        prop_f[prop_f <= 0.15] ='nan'  
        #fprop = datadir+'slp'+hour+'.npy'
        #prop = np.load(fprop)
        filename=outdir+'cloudhigh_'+hour
        ptitle='Clouds High Level'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f*100,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Cloud Cover
    #########################################################################
    try:
        fprop_f = datadir+'blcldpct'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f <= 0.15] ='nan'
        #fprop = datadir+'slp'+hour+'.npy'
        #prop = np.load(fprop)
        filename=outdir+'blcldpct_'+hour
        ptitle='BL Cloud Cover'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT HGT TERRAIN
    #########################################################################
    try:
        fprop = datadir+'ter'+'.npy'
        prop = np.load(fprop)
        prop[prop <= 5.] ='nan'
        filename=outdir+'ter_'+hour
        ptitle='Terrain Height of the Model'
        cmap='tab20b'
        units='[m]'
        vmin=None #-np.max(prop)/3
        vmax=None #np.max(prop)

    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)

    #########################################################################
    ##################   PLT CAPE
    #########################################################################
    try:
        fprop = datadir+'mcape'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'mcape_'+hour
        ptitle='CAPE'
        cmap='jet'
        units='[J/kg]'
        vmin=None
        vmax=None    
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT CIN
    #########################################################################
    try:
        fprop = datadir+'mcin'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'mcin_'+hour
        ptitle='CIN (Convective Inhibition)'
        cmap='jet'
        units='[J/kg]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)
    
    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT LFC
    #########################################################################
    try:
        fprop = datadir+'lfc'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'lfc_'+hour
        ptitle='LFC (Level of Free Convection)'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT LCL
    #########################################################################
    try:
        fprop = datadir+'lcl'+hour+'.npy'
        prop = np.load(fprop)

        filename=outdir+'lcl_'+hour
        ptitle='LCL ( Lifted Condensation Level)'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Precipitable Water
    #########################################################################
    try:
        fprop_f = datadir+'pw'+hour+'.npy'
        prop_f = np.load(fprop_f)
        #fprop = datadir+'slp'+hour+'.npy'
        #prop = np.load(fprop)
        filename=outdir+'pw_'+hour
        ptitle='Precipitable Water'
        cmap='tab20b'
        units='[mm]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT RAIN
    #########################################################################
    try:
        fprop_f = datadir+'rainTot'+hour+'.npy'
        prop_f = np.load(fprop_f)
        if(os.path.exists(datadir+'rainTot_'+str('{0:02}'.format(hour_i-1))+'.npy')):
            fprop_f2 = datadir+'rainTot_'+str('{0:02}'.format(hour_i-1))+'.npy'
            prop_f2 = np.load(fprop_f2)
            prop_f2=prop_f-prop_f2
        else:
            prop_f2=prop_f
        prop_f2[prop_f2 <= 0] = 'nan'
        #fprop = datadir+'slp'+hour+'.npy'
        #prop = np.load(fprop)
        filename=outdir+'rainTot_'+hour
        ptitle='Rain'
        cmap='jet'
        units='[mm]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f2,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT GENERAL SCENARIO
    #########################################################################
    try:
        fprop = datadir+'wspd10'+hour+'.npy'
        fprop2 = datadir+'wdir10'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        #fprop_f = datadir+'rainTot'+hour+'.npy'
        rain = prop_f2#np.load(fprop_f)
        fprop_f = datadir+'blcldpct'+hour+'.npy'
        prop_fclouds = np.load(fprop_f)
        prop_fclouds[prop_fclouds <= 0.15] ='nan'
        fprop = datadir+'slp'+hour+'.npy'
        slp = np.load(fprop)
        filename=outdir+'general_'+hour
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_general_sce(U,V, prop_fclouds, rain ,slp, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy)
    #########################################################################
    ##################   PLT SURFACE TEMP
    #########################################################################
    try:
        fprop = datadir+'sfctemp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'sfctemp_'+hour
        ptitle='Surface temperature'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   BL depth
    #########################################################################
    try:
        fprop = datadir+'bldepth'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'bldepth_'+hour
        ptitle='BL depth'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   Height of BL Top
    #########################################################################
    try:
        fprop = datadir+'hbl'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'hbl_'+hour
        ptitle='Height of BL Top'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Cloud top temp.
    #########################################################################
    try:
        fprop_f = datadir+'ctt'+hour+'.npy'
        prop_f = np.load(fprop_f)
        filename=outdir+'ctt_'+hour
        ptitle='Cloud top temp.'
        cmap='Blues'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Sfc. Heating
    #########################################################################
    try:
        fprop_f = datadir+'hfx'+hour+'.npy'
        prop_f = np.load(fprop_f)
        filename=outdir+'hfx_'+hour
        ptitle='Surface Heating'
        cmap='tab20b'
        units='[W/$m^2$]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT SNOW WATER EQUIVALENT
    #########################################################################
    try:
        fprop_f = datadir+'snow'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f == 0] = 'nan'
        filename=outdir+'snow_'+hour
        ptitle='Snow Water Equivalent'
        cmap='jet'
        units='[mm]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT PHYSICAL SNOW DEPTH
    #########################################################################
    try:
        fprop_f = datadir+'snowh'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f == 0] = 'nan'
        filename=outdir+'snowh_'+hour
        ptitle='Physical Snow Depth'
        cmap='jet'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Geopotential height at 500 hPa
    #########################################################################
    try:
        fprop = datadir+'ht_500'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ht_500_'+hour
        ptitle='Geopotential height at 500 hPa'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Geopotential height at 700 hPa
    #########################################################################
    try:
        fprop = datadir+'ht_700'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ht_700_'+hour
        ptitle='Geopotential height at 700 hPa'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Geopotential height at 925 hPa
    #########################################################################
    try:
        fprop = datadir+'ht_925'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ht_925_'+hour
        ptitle='Geopotential height at 925 hPa'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Temp. at 500 hPa
    #########################################################################
    try:
        fprop = datadir+'t_500'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'t_500_'+hour
        ptitle='Temp. at 500 hPa'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Temp. at 700 hPa
    #########################################################################
    try:
        fprop = datadir+'t_700'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'t_700_'+hour
        ptitle='Temp. at 700 hPa'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Temp. at 925 hPa
    #########################################################################
    try:
        fprop = datadir+'t_925'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'t_925_'+hour
        ptitle='Temp. at 925 hPa'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Winds at 500 hPa
    #########################################################################
    try:
        fprop = datadir+'wspd_500'+hour+'.npy'
        fprop2 = datadir+'wdir_500'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'wind_500_'+hour
        ptitle='Winds at 500 hPa'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    #########################################################################
    ##################   PLT Winds at 700 hPa
    #########################################################################
    try:
        fprop = datadir+'wspd_700'+hour+'.npy'
        fprop2 = datadir+'wdir_700'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'wind_700_'+hour
        ptitle='Winds at 700 hPa'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    #########################################################################
    ##################   PLT Winds at 925 hPa
    #########################################################################
    try:
        fprop = datadir+'wspd_925'+hour+'.npy'
        fprop2 = datadir+'wdir_925'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'wind_925_'+hour
        ptitle='Winds at 925 hPa'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    #########################################################################
    ##################   PLT BL Avg Wind
    #########################################################################
    try:
        fprop = datadir+'ublavgwind'+hour+'.npy'
        fprop2 = datadir+'vblavgwind'+hour+'.npy'
        U = np.load(fprop)
        V = np.load(fprop2)
        fprop = datadir+'blavgwindspeed'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'blavgwind_'+hour
        ptitle='BL Avg Wind'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    #########################################################################
    ##################   PLT Wind at BL Top
    #########################################################################
    try:
        fprop = datadir+'utop'+hour+'.npy'
        fprop2 = datadir+'vtop'+hour+'.npy'
        U = np.load(fprop)
        V = np.load(fprop2)
        fprop = datadir+'bltopwindspeed'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'bltopwind_'+hour
        ptitle='Wind at BL Top'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy)
    #########################################################################
    ##################   PLT BL Max. Up/Down Motion
    #########################################################################
    try:
        fprop = datadir+'wblMxMn'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'wblMxMn_'+hour
        ptitle='BL Max. Up/Down Motion'
        cmap='tab20b'
        units='[cm/s]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Explicit Cloud Base [AGL]
    #########################################################################
    try:
        fprop = datadir+'blcwbase'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'blcwbase_'+hour
        ptitle='BL Explicit Cloud Base [AGL]'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Thermal Updraft Velocity
    #########################################################################
    try:
        fprop = datadir+'wstar'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'wstar_'+hour
        ptitle='Thermal Updraft Velocity'
        cmap='tab20b'
        units='[cm/s]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Height of Critical Updraft Strength
    #########################################################################
    try:
        fprop = datadir+'hwcrit'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'hwcrit_'+hour
        ptitle='Height of Critical Updraft Strength'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Cu Cloudbase
    #########################################################################
    try:
        fprop = datadir+'zsfclcl'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'zsfclcl_'+hour
        ptitle='Cu Cloudbase'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT OvercastDevelopment Cloudbase
    #########################################################################
    try:
        fprop = datadir+'zblcl'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'zblcl_'+hour
        ptitle='OvercastDevelopment Cloudbase'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Thermalling Height
    #########################################################################
    try:
        fprop = datadir+'hglider'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'hglider_'+hour
        ptitle='Thermalling Height'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Top Uncertainty/Variability
    #########################################################################
    try:
        fprop = datadir+'bltopvariab'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'bltopvariab_'+hour
        ptitle='BL Top Uncertainty/Variability'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Vertical Wind Shear
    #########################################################################
    try:
        fprop = datadir+'blwindshear'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'blwindshear_'+hour
        ptitle='BL Vertical Wind Shear'
        cmap='tab20b'
        units='[m/s]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Dew Point
    #########################################################################
    try:
        fprop = datadir+'td2'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'td2_'+hour
        ptitle='Surface Dew Point'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,cmap,vmin,vmax,units)

