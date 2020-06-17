#==========================================================================
#   RASPURI v2 a RASP(Regional Atmospheric
#   Soaring Predictions) COMPUTER PROGRAM
#   Original Creator: Oriol Cervelló i Nogués ( raspuri [at] protonmail.com )
#   Copyright (C) 2019+ by Oriol Cervelló i Nogués
#==========================================================================
# License: GNU GPLv3.0
# Copyright (C) 2019  Oriol Cervelló
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==========================================================================
#==========================================================================
# plot_examples.py
# This script is part of RASPURI v2
# Script containing the ploting functions
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as arrsty
import rasterio
from rasterio.merge import merge
from matplotlib.colors import LightSource

def plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle):
    try:
        #PLOT TOPO
        fig, ax = plt.subplots(figsize=(14,8),dpi=100)
        plt.rcParams.update({'font.size': 18})
        extent = [bounds.left,bounds.right , bounds.bottom , bounds.top]
        plt.imshow(ls.hillshade(mosaic[0,:,:], vert_exag=ve),extent=extent, cmap='gray')
        #PLOT DATA
        '''
        strm = ax.streamplot(x,y,U,V,color=prop*3.6, density=1.8 ,linewidth=1.8,arrowsize=1.3, cmap='tab20b')
        cbar = fig.colorbar(strm.lines)
        '''
        # Normalise the data for uniform arrow size
        u_norm = U / np.sqrt(U ** 2.0 + V ** 2.0)
        v_norm = V / np.sqrt(U ** 2.0 + V ** 2.0)
        sca=5
        q = ax.quiver(x[::sca,::sca], y[::sca,::sca], u_norm[::sca,::sca], v_norm[::sca,::sca], pivot='middle', alpha=1)        
        CF=ax.contourf(x,y,prop*3.6,cmap="tab20b", alpha=0.35)
        cbar = fig.colorbar(CF)
        cbar.ax.set_ylabel('[km/h]', fontsize=18)
        cbar.ax.tick_params(labelsize=18)

        plt.title(ptitle, loc='left')
        plt.figtext(0.99, 0.96, 'Valid Time: '+valid_t, horizontalalignment='right') 
        plt.figtext(0.99, 0.01, 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right') 
        plt.figtext(0.01, 0.01, 'RASPURI by Oriol Cevrelló ', horizontalalignment='left') 
        #ANOTATIONS
        ax.scatter(dotx, doty,color='red')

        for i, txt in enumerate(dottitle):
            ax.annotate(txt, (dotx[i], doty[i]),fontsize=10)
        ##SAVE    
        plt.savefig(filename)
        plt.close()
    except Exception as e: 
        print('****Error ploting the '+ptitle+', plot.py****')
        print(e)

def plot_cont(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units):
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
        plt.figtext(0.99, 0.96, 'Valid Time: '+valid_t, horizontalalignment='right') 
        plt.figtext(0.99, 0.01, 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right') 
        plt.figtext(0.01, 0.01, 'RASPURI by Oriol Cevrelló ', horizontalalignment='left') 
        #ANOTATIONS
        ax.scatter(dotx, doty,color='red')
        for i, txt in enumerate(dottitle):
            ax.annotate(txt, (dotx[i], doty[i]),fontsize=10)
        ##SAVE    
        plt.savefig(filename)
        plt.close()
    except Exception as e: 
        print('****Error ploting the '+ptitle+', plot.py****')
        print(e)



def plot_general_sce(U,V, prop_fclouds,prop_rain, prop, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy, dotx, doty, dottitle):
    try:    
        #PLOT TOPO
        fig, ax = plt.subplots(figsize=(14,8),dpi=100)
        plt.rcParams.update({'font.size': 18})

        extent = [bounds.left,bounds.right , bounds.bottom , bounds.top]
        plt.imshow(ls.hillshade(mosaic[0,:,:], vert_exag=ve),extent=extent, cmap='gray',aspect='auto',interpolation='bessel')

        #PLOT DATA
        u_norm = U / np.sqrt(U ** 2.0 + V ** 2.0)
        v_norm = V / np.sqrt(U ** 2.0 + V ** 2.0)
        sca=6
        q = ax.quiver(x[::sca,::sca], y[::sca,::sca], u_norm[::sca,::sca], v_norm[::sca,::sca], pivot='middle', alpha=1)


        CF4=ax.contourf(x,y,prop_rain,cmap='RdPu', alpha=0.45)
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
        plt.figtext(0.99, 0.96, 'Valid Time: '+valid_t, horizontalalignment='right') 
        plt.figtext(0.99, 0.01, 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right') 
        plt.figtext(0.01, 0.01, 'RASPURI by Oriol Cevrelló ', horizontalalignment='left') 

        #ANOTATIONS
        ax.scatter(dotx, doty,color='red')

        for i, txt in enumerate(dottitle):
            ax.annotate(txt, (dotx[i], doty[i]),fontsize=10)

        ##SAVE    
        plt.savefig(filename)
        plt.close()
    except Exception as e: 
        print('****Error ploting the general scenario, plot.py****')
        print(e)

def plot_rasp(datadir,hour,valid_t,dx,dy,outdir,topodir,doty,dotx,dottitle,topofiles):
    #########################################################################
    ##################   TOPO
    #########################################################################
    #https://visibleearth.nasa.gov/images/73934/topography
    try:
        flat = datadir+'lats'+hour+'.npy'
        flon = datadir+'lons'+hour+'.npy'
        lat = np.load(flat)
        lon = np.load(flon)
        x = np.linspace(np.min(lon),np.max(lon),lon.shape[1])
        y = np.linspace(np.min(lat),np.max(lat),lat.shape[0])
        dataset=[]
        x=lon
        y=lat

        for i, topo in enumerate(topofiles):
            dataset.append(rasterio.open(topodir+'gebco_08_rev_elev_'+topo+'_grey_geo.tif'))

        bounds=rasterio.coords.BoundingBox(np.min(lon),np.min(lat) ,np.max(lon),np.max(lat) )
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
        fprop = datadir+'wspd10'+hour+'.npy'
        fprop2 = datadir+'wdir10'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'sfcwind'+hour+'.png'
        ptitle='Surface Wind'
    except Exception as e:
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle)
    #########################################################################
    ##################   PLT LOW CLOUDS
    #########################################################################
    try:
        fprop_f = datadir+'cloudfrac_low'+hour+'.npy'
        prop_f = np.load(fprop_f)    
        fprop = datadir+'slp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'cloudlow'+hour+'.png'
        ptitle='Clouds Low Level'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f*100,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT MID CLOUDS
    #########################################################################
    try:
        fprop_f = datadir+'cloudfrac_mid'+hour+'.npy'
        prop_f = np.load(fprop_f)
        fprop = datadir+'slp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'cloudmid'+hour+'.png'
        ptitle='Clouds Mid Level'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f*100,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT HIGH CLOUDS
    #########################################################################
    try:
        fprop_f = datadir+'cloudfrac_high'+hour+'.npy'
        prop_f = np.load(fprop_f)    
        fprop = datadir+'slp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'cloudhigh'+hour+'.png'
        ptitle='Clouds High Level'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f*100,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Cloud Cover
    #########################################################################
    try:
        fprop_f = datadir+'blcldpct'+hour+'.npy'
        prop_f = np.load(fprop_f)
        fprop = datadir+'slp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'blcldpct'+hour+'.png'
        ptitle='BL Cloud Cover'
        cmap='Blues'
        units='[%]'
        vmin=0
        vmax=130
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT HGT TERRAIN
    #########################################################################
    try:
        fprop = datadir+'ter'+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ter'+hour+'.png'
        ptitle='Terrain Height of the Model'
        cmap='gist_earth'
        units='[m]'
        vmin=-np.max(prop)/3
        vmax=np.max(prop)
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
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
        fprop_f = datadir+'rainTot'+hour+'.npy'
        rain = np.load(fprop_f)
        fprop_f = datadir+'blcldpct'+hour+'.npy'
        prop_fclouds = np.load(fprop_f)
        fprop = datadir+'slp'+hour+'.npy'
        slp = np.load(fprop)
        filename=outdir+'general'+hour+'.png'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_general_sce(U,V, prop_fclouds, rain ,slp, filename, bounds, ls, ve, mosaic, x, y, valid_t, dx, dy, dotx, doty, dottitle)
    #########################################################################
    ##################   PLT CAPE
    #########################################################################
    try:
        fprop = datadir+'mcape'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'mcape'+hour+'.png'
        ptitle='CAPE (Convective Available Potential Energy)'
        cmap='jet'
        units='[J/kg]'
        vmin=None
        vmax=None    
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT CIN
    #########################################################################
    try:
        fprop = datadir+'mcin'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'mcin'+hour+'.png'
        ptitle='CIN (Convective Inhibition)'
        cmap='jet'
        units='[J/kg]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)
    
    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT LFC
    #########################################################################
    try:
        fprop = datadir+'lfc'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'lfc'+hour+'.png'
        ptitle='LFC (Level of Free Convection)'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT LCL
    #########################################################################
    try:
        fprop = datadir+'lcl'+hour+'.npy'
        prop = np.load(fprop)

        filename=outdir+'lcl'+hour+'.png'
        ptitle='LCL ( Lifted Condensation Level)'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Precipitable Water
    #########################################################################
    try:
        fprop_f = datadir+'pw'+hour+'.npy'
        prop_f = np.load(fprop_f)
        fprop = datadir+'slp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'pw'+hour+'.png'
        ptitle='Precipitable Water'
        cmap='tab20b'
        units='[mm]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT RAIN
    #########################################################################
    try:
        fprop_f = datadir+'rainTot'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f == 0] = 'nan'
        fprop = datadir+'slp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'rainTot'+hour+'.png'
        ptitle='Rain'
        cmap='jet'
        units='[mm]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT SURFACE TEMP
    #########################################################################
    try:
        fprop = datadir+'sfctemp'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'sfctemp'+hour+'.png'
        ptitle='Surface temperature'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   BL depth
    #########################################################################
    try:
        fprop = datadir+'bldepth'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'bldepth'+hour+'.png'
        ptitle='BL depth'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   Height of BL Top
    #########################################################################
    try:
        fprop = datadir+'hbl'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'hbl'+hour+'.png'
        ptitle='Height of BL Top'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Cloud top temp.
    #########################################################################
    try:
        fprop_f = datadir+'ctt'+hour+'.npy'
        prop_f = np.load(fprop_f)
        filename=outdir+'ctt'+hour+'.png'
        ptitle='Cloud top temp.'
        cmap='Blues'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Sfc. Heating
    #########################################################################
    try:
        fprop_f = datadir+'hfx'+hour+'.npy'
        prop_f = np.load(fprop_f)
        filename=outdir+'hfx'+hour+'.png'
        ptitle='Surface Heating'
        cmap='tab20b'
        units='[W/$m^2$]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT SNOW WATER EQUIVALENT
    #########################################################################
    try:
        fprop_f = datadir+'snow'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f == 0] = 'nan'
        filename=outdir+'snow'+hour+'.png'
        ptitle='Snow Water Equivalent'
        cmap='jet'
        units='[mm]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT PHYSICAL SNOW DEPTH
    #########################################################################
    try:
        fprop_f = datadir+'snowh'+hour+'.npy'
        prop_f = np.load(fprop_f)
        prop_f[prop_f == 0] = 'nan'
        filename=outdir+'snowh'+hour+'.png'
        ptitle='Physical Snow Depth'
        cmap='jet'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop_f,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Geopotential height to 500 hPa
    #########################################################################
    try:
        fprop = datadir+'ht_500'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ht_500'+hour+'.png'
        ptitle='Geopotential height to 500 hPa'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Geopotential height to 700 hPa
    #########################################################################
    try:
        fprop = datadir+'ht_700'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ht_700'+hour+'.png'
        ptitle='Geopotential height to 700 hPa'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Geopotential height to 925 hPa
    #########################################################################
    try:
        fprop = datadir+'ht_925'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'ht_925'+hour+'.png'
        ptitle='Geopotential height to 925 hPa'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Temp. to 500 hPa
    #########################################################################
    try:
        fprop = datadir+'t_500'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'t_500'+hour+'.png'
        ptitle='Temp. to 500 hPa'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Temp. to 700 hPa
    #########################################################################
    try:
        fprop = datadir+'t_700'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'t_700'+hour+'.png'
        ptitle='Temp. to 700 hPa'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Temp. to 925 hPa
    #########################################################################
    try:
        fprop = datadir+'t_925'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'t_925'+hour+'.png'
        ptitle='Temp. to 925 hPa'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Winds to 500 hPa
    #########################################################################
    try:
        fprop = datadir+'wspd_500'+hour+'.npy'
        fprop2 = datadir+'wdir_500'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'wind_500'+hour+'.png'
        ptitle='Winds to 500 hPa'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle)
    #########################################################################
    ##################   PLT Winds to 700 hPa
    #########################################################################
    try:
        fprop = datadir+'wspd_700'+hour+'.npy'
        fprop2 = datadir+'wdir_700'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'wind_700'+hour+'.png'
        ptitle='Winds to 700 hPa'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle)
    #########################################################################
    ##################   PLT Winds to 925 hPa
    #########################################################################
    try:
        fprop = datadir+'wspd_925'+hour+'.npy'
        fprop2 = datadir+'wdir_925'+hour+'.npy'
        prop = np.load(fprop)
        dire = np.radians(np.load(fprop2))
        U = -prop*np.sin(dire)
        V = -prop*np.cos(dire)
        filename=outdir+'wind_925'+hour+'.png'
        ptitle='Winds to 925 hPa'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle)
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
        filename=outdir+'blavgwind'+hour+'.png'
        ptitle='BL Avg Wind'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle)
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
        filename=outdir+'bltopwind'+hour+'.png'
        ptitle='Wind at BL Top'
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_strem(U,V,prop,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle)
    #########################################################################
    ##################   PLT BL Max. Up/Down Motion
    #########################################################################
    try:
        fprop = datadir+'wblMxMn'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'wblMxMn'+hour+'.png'
        ptitle='BL Max. Up/Down Motion'
        cmap='tab20b'
        units='[cm/s]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Explicit Cloud Base [AGL]
    #########################################################################
    try:
        fprop = datadir+'blcwbase'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'blcwbase'+hour+'.png'
        ptitle='BL Explicit Cloud Base [AGL]'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Thermal Updraft Velocity
    #########################################################################
    try:
        fprop = datadir+'wstar'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'wstar'+hour+'.png'
        ptitle='Thermal Updraft Velocity'
        cmap='tab20b'
        units='[cm/s]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Height of Critical Updraft Strength
    #########################################################################
    try:
        fprop = datadir+'hwcrit'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'hwcrit'+hour+'.png'
        ptitle='Height of Critical Updraft Strength'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Cu Cloudbase
    #########################################################################
    try:
        fprop = datadir+'zsfclcl'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'zsfclcl'+hour+'.png'
        ptitle='Cu Cloudbase'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT OvercastDevelopment Cloudbase
    #########################################################################
    try:
        fprop = datadir+'zblcl'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'zblcl'+hour+'.png'
        ptitle='OvercastDevelopment Cloudbase'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Thermalling Height
    #########################################################################
    try:
        fprop = datadir+'hglider'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'hglider'+hour+'.png'
        ptitle='Thermalling Height'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Top Uncertainty/Variability
    #########################################################################
    try:
        fprop = datadir+'bltopvariab'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'bltopvariab'+hour+'.png'
        ptitle='BL Top Uncertainty/Variability'
        cmap='tab20b'
        units='[m]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT BL Vertical Wind Shear
    #########################################################################
    try:
        fprop = datadir+'blwindshear'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'blwindshear'+hour+'.png'
        ptitle='BL Vertical Wind Shear'
        cmap='tab20b'
        units='[m/s]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)
    #########################################################################
    ##################   PLT Dew Point
    #########################################################################
    try:
        fprop = datadir+'td2'+hour+'.npy'
        prop = np.load(fprop)
        filename=outdir+'td2'+hour+'.png'
        ptitle='Surface Dew Point'
        cmap='tab20b'
        units='[ºC]'
        vmin=None
        vmax=None
    except Exception as e: 
        print('****Error reading '+ptitle+', plot.py****')
        print(e)

    plot_cont(prop,None,ptitle,filename,bounds,ls,ve,mosaic,x,y,valid_t,dx,dy,dotx,doty,dottitle,cmap,vmin,vmax,units)


#INPUTS
datadir= 'data/dom01/20200118/'
hour='10'
valid_t= '25 12 2018 - 06 CTE (05 UTC)'
dx=2000
dy=2000
outdir='./'
topodir='./'

#en variables
doty = [41.12,40.44, 40.46]
dotx = [-3.72,-4.48,-5.33]
dottitle = ['Arc', 'Ceb', 'Pie']
topofiles=['B1','C1']


















plot_rasp(datadir,hour,valid_t,dx,dy,outdir,topodir,doty,dotx,dottitle,topofiles)


'''
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import to_np, getvar, smooth2d, latlon_coords, vinterp, interplevel, ll_to_xy_proj
ncfile = Dataset('wrfout_d01_2020-01-20_10:00:00')

slp = getvar(ncfile, "slp")
smooth_slp = smooth2d(slp, 4, cenweight=4)
np.save('slp4',to_np(smooth_slp))

smooth_slp = smooth2d(slp, 3, cenweight=4)
np.save('slp3',to_np(smooth_slp))

smooth_slp = smooth2d(slp, 5, cenweight=4)
np.save('slp5',to_np(smooth_slp))
'''
