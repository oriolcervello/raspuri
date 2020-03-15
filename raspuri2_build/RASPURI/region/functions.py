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
# functions.py
# This script is part of RASPURI v2
# Script containing all the functions called from rasp except the plots
try:
    import sys
    import os
    import time
    from datetime import datetime
    from ftplib import FTP
    import numpy as np
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    from netCDF4 import Dataset
    from wrf import to_np, getvar, smooth2d, latlon_coords, vinterp, interplevel, ll_to_xy_proj
    from metpy.plots import SkewT
    import metpy.calc as mpcalc
    from metpy.units import pandas_dataframe_to_unit_arrays, units
    from variables import SERVER, WAIT_FTP_START, SOUNDINGS,SOUNDINGS_NAMES
    import ncl_jack_fortran
except Exception as e:
    print('****ERROR importing externals, functions.py****')
    print(e)
    exit()



def check_start_download(foldername,folder_h,file_name):
    # check_start_download(foldername,folder_h,file_name)
    # Function to check if data is ready to start downloading
    # ---INPUTS:
    # foldername name of parent folder
    # folder_h hour of downloading
    # filename="wrfout_d02_2020-01-11_15_00_00"#filename to get the data   
    # ---OUTPUTS:
    # boolean
    start=False   
    while(start==False):
        try:
            ftp = FTP(SERVER) #,port)     # connect to host  'anonymous','anonymous'
            ftp.login() 
            #ftp.set_pasv(False)
        except:
            print('****ERROR connecting to FTP server, ftp_call.py****')
            exit()
        try:            
            ftp.cwd( '/pub/data/nccf/com/gfs/prod/')
            ftp_list= []
            ftp_list=ftp.nlst()
            #print(ftp_list)
            if (foldername in ftp_list):
                ftp.cwd(foldername)      
     
                ftp_list= []
                ftp_list=ftp.nlst()
                #print(ftp_list)
                if (folder_h in ftp_list):
                    ftp.cwd(folder_h)        
                
                    ftp_list= []
                    ftp_list=ftp.nlst()
                    if (file_name in ftp_list):
                        start=True
                        ftp.quit()
                    else:
                        ftp.quit()
                        print('****WAITING: to start downloadings, no files yet, wait until retry = ' + str(WAIT_FTP_START)+'s****')
                        time.sleep(WAIT_FTP_START)
                else:
                    ftp.quit()
                    print('****WAITING: to start downloadings, no files yet, wait until retry = ' + str(WAIT_FTP_START)+'s****')
                    time.sleep(WAIT_FTP_START)
            else:
                ftp.quit()
                print('****WAITING: to start downloadings, no files yet, wait until retry = ' + str(WAIT_FTP_START)+'s****')
                time.sleep(WAIT_FTP_START)
                           
        except Exception as e: 
            print('****Error checking start time, check_start_download , functions.py****')
            print(e)
            ftp.quit()        
            exit()



def postprocessing(filename,outputdir,utch):
    # postprocessing(filename,outputdir,utch)
    # Function compute and save in outputdir all the variables named in
    # RASPURI/postprocessing/file_index in form of matrix ready to plot.
    # ---INPUTS:
    # filename="wrfout_d02_2020-01-11_15_00_00"#filename to get the data   
    # outputdir='data/' #output directory
    # utch string utc time for filename
    # ---OUTPUTS:
    # matrix data on output dir 

    #########################################################################
    ##################   OPEN FILE
    #########################################################################
    try:
        ncfile = Dataset(filename)
        #outputdir='aaaaa/'
    except Exception as e: 
        print('****Error opening file postprocessing , functions.py****')
        print(e)
    #########################################################################
    ##################   GET VARS
    #########################################################################
    try:

        slp = getvar(ncfile, "slp") # Sea Level Pressure

        z = getvar(ncfile, "z") # Geopotential Height
        p = getvar(ncfile, "pressure") # Pressure (hPa) 
        t = getvar(ncfile, "tc") # temperature in Celsius
        ua = getvar(ncfile, "ua") # winds
        va = getvar(ncfile, "va")
        wa = getvar(ncfile, "wa")
        wspd_wdir = getvar(ncfile, "wspd_wdir")
        #uv10 = getvar(ncfile, "uvmet10")
        wspd_wdir10 = getvar(ncfile, "wspd_wdir10")
        cape_2d = getvar(ncfile, "cape_2d")
        cloudfrac = getvar(ncfile, "cloudfrac") # clouds
        ctt = getvar(ncfile, "ctt") # Cloud Top Temperature
        pw = getvar(ncfile, "pw")# Precipitable water
        bldepth = getvar(ncfile, "PBLH")#bl depth (metres)    
        ter = getvar(ncfile, "HGT")#Terrain Height (metres)    
        qcloud = getvar(ncfile, "QCLOUD")#"Cloud water mixing ratio"
        t2 = getvar(ncfile, "T2")# TEMP at 2 M 
        uv  = getvar(ncfile, "uvmet") # u,v NOT rotated to grid   in m/s
        p  = getvar(ncfile, "P") #"perturbation pressure"
        pb  = getvar(ncfile, "PB") #"BASE STATE PRESSURE"
        hfx  = getvar(ncfile, "HFX") #for sfc. sensible heat flux in w/m2    142
        thetac =getvar(ncfile, "T")+ 26.85 #"perturbation potential temperature theta-t0"
        qvapor  = getvar(ncfile, "QVAPOR") #"Water vapor mixing ratio" 
        vhf  = getvar(ncfile, "LH") #"LATENT HEAT FLUX AT THE SURFACE" 
        td  = getvar(ncfile, "td") #dew point temperature (C)
        td2  = getvar(ncfile, "td2") #dew point temperature at 2 M (C)
        snow  = getvar(ncfile, "SNOW")#"SNOW WATER EQUIVALENT"
        rainc = getvar(ncfile, "RAINC")#"ACCUMULATED TOTAL CUMULUS PRECIPITATION"
        rainnc = getvar(ncfile, "RAINNC")#"ACCUMULATED TOTAL GRID SCALE PRECIPITATION"
        snowh  = getvar(ncfile, "SNOWH")#"PHYSICAL SNOW DEPTH"

        pblh=bldepth
        #lats, lons = latlon_coords(slp)
        lats = getvar(ncfile, "XLAT")
        lons = getvar(ncfile, "XLONG")
        dx=slp.projection.dx 
        dy=slp.projection.dy
    except Exception as e: 
        print('****Error reading vars postprocessing , functions.py****')
        print(e)
    #########################################################################
    ##################   VARS TRANSFORMATIONS
    #########################################################################
    try:
        ###
        wspd_all=wspd_wdir[0,:]
        wdir_all=wspd_wdir[1,:]


        # Interpolate geopotential height, u, and v winds to 500 hPa ->5000m
        ht_500 = interplevel(z, p, 500.)
        wdir_500 = interplevel(wdir_all, p, 500)
        wspd_500 = interplevel(wspd_all, p, 500)
        t_500 = interplevel(t, p, 500)

        # Interpolate geopotential height, u, and v winds to 700 hPa ->3000m
        ht_700 = interplevel(z, p, 700.)
        wdir_700 = interplevel(wdir_all, p, 700)
        wspd_700 = interplevel(wspd_all, p, 700)
        t_700 = interplevel(t, p, 700)

        # Interpolate geopotential height, u, and v winds to 925 hPa ->762m
        ht_925 = interplevel(z, p, 925.)
        wdir_925 = interplevel(wdir_all, p, 925)
        wspd_925 = interplevel(wspd_all, p, 925)
        t_925 = interplevel(t, p, 925)

        # Clouds
        cloudfrac_low=cloudfrac[0,:,:] #300m
        cloudfrac_mid=cloudfrac[1,:,:] #2000m
        cloudfrac_high=cloudfrac[2,:,:] #6000m

        # Surface
        smooth_slp = smooth2d(slp, 7, cenweight=3) # Smooth the sea level pressure since it tends to be noisy near the mountains
        sfctemp = t2 - 273.16 #Surface temp
        hbl_mag = pblh.values + ter.values   #"Height of BL Top
        wspd10=wspd_wdir10[0,:]  #Surface wind speed
        wdir10=wspd_wdir10[1,:] #Surface wind dir
        mcape=cape_2d[0,:,:] 
        mcin=cape_2d[1,:,:] 
        lcl=cape_2d[2,:,:] 
        lfc=cape_2d[3,:,:] 
        rainTot = rainc + rainnc

        # Aux dr jack
        uEW = uv[0,:,:]                           
        vNS = uv[1,:,:]                         
        pmb=var = 0.01*(p.values+pb.values) # press is vertical coordinate in mb
        vhf=np.clip(vhf.values,a_min=0, a_max = np.max(vhf.values)) 
        vhf = hfx +  0.000245268*(t[0,:,:]+273.16)*vhf
    except Exception as e: 
        print('****Error transforming vars postprocessing , functions.py****')
        print(e)
    #########################################################################
    ##################   SAVE
    #########################################################################
    try:
        np.save(outputdir+'lons',(lons.values))
        np.save(outputdir+'lats',(lats.values))        
        np.save(outputdir+'ter',(ter.values))
        np.save(outputdir+'mcape'+utch,mcape.values)
        np.save(outputdir+'mcin'+utch,mcin.values)
        np.save(outputdir+'lcl'+utch,lcl.values)
        np.save(outputdir+'lfc'+utch,lfc.values)
        np.save(outputdir+'sfctemp'+utch,(sfctemp.values))
        np.save(outputdir+'bldepth'+utch,(bldepth.values))
        np.save(outputdir+'wspd10'+utch,(wspd10.values))
        np.save(outputdir+'wdir10'+utch,(wdir10.values))
        np.save(outputdir+'pw'+utch,(pw.values))
        np.save(outputdir+'ctt'+utch,ctt.values)
        np.save(outputdir+'hbl'+utch,hbl_mag)
        np.save(outputdir+'cloudfrac_low'+utch,cloudfrac_low.values)
        np.save(outputdir+'cloudfrac_mid'+utch,cloudfrac_mid.values)
        np.save(outputdir+'cloudfrac_high'+utch,cloudfrac_high.values)
        np.save(outputdir+'slp'+utch,(smooth_slp.values))
        np.save(outputdir+'hfx'+utch,(hfx.values))
        np.save(outputdir+'snow'+utch,(snow.values))
        np.save(outputdir+'rainTot'+utch,(rainTot.values))
        np.save(outputdir+'snowh'+utch,(snowh.values))
        np.save(outputdir+'td2'+utch,td2.values)

        np.save(outputdir+'ht_500'+utch,ht_500.values)
        np.save(outputdir+'wdir_500'+utch,wdir_500.values)
        np.save(outputdir+'wspd_500'+utch,wspd_500.values)
        np.save(outputdir+'t_500'+utch,t_500.values)

        np.save(outputdir+'ht_700'+utch,ht_700.values)
        np.save(outputdir+'wdir_700'+utch,wdir_700.values)
        np.save(outputdir+'wspd_700'+utch,wspd_700.values)
        np.save(outputdir+'t_700'+utch,t_700.values)

        np.save(outputdir+'ht_925'+utch,ht_925.values)
        np.save(outputdir+'wdir_925'+utch,wdir_925.values)
        np.save(outputdir+'wspd_925'+utch,wspd_925.values)
        np.save(outputdir+'t_925'+utch,t_925.values)
    except Exception as e: 
        print('****Error saving vars postprocessing , functions.py****')
        print(e)
    #########################################################################
    ##################   DR jack transf
    #########################################################################
    try:
        # Variables
        size=(z.values).shape
        nz       = size[0]
        ny       = size[1]
        nx       = size[2]
        # Transforms
        '''For NCL arrays, the fastest-varying dimension is the rightmost, while for Fortran it is the leftmost dimension. Therefore, if XA is a Fortran array dimensioned idim x jdim, this array will be dimensioned jdim x idim in NCL'''
        pblh=np.transpose(pblh.values)
        ter=np.transpose(ter.values)
        wa=np.transpose(wa.values)
        z=np.transpose(z.values)
        qcloud=np.transpose(qcloud.values)
        uEW=np.transpose(uEW.values)
        vNS=np.transpose(vNS.values)
        qvapor=np.transpose(qvapor.values)
        tc=np.transpose(t.values)
        pmb=np.transpose(pmb)
        vhf=np.transpose(vhf.values)
        td=np.transpose(td.values)
        thetac=np.transpose(thetac.values)
        ua=np.transpose(ua.values)
        va=np.transpose(va.values)
        # Other Constants
        time = 0    # Seems time is always 0 for DrJack's code
        cdbl = 0.003    # Coefficient of Drag for Boundary Layer 
        cwbasecriteria = 0.000010    # Cloud Water criterion

        #"BL Max. Up/Down Motion"
        wblMxMn = ncl_jack_fortran.calc_wblmaxmin(0,wa,z,ter,pblh) 
        #"BL Explicit Cloud Base [AGL]"
        laglcwbase = 1
        criteriondegc = 1.0
        maxcwbasem = 5486.40 
        blcwbase = ncl_jack_fortran.calc_blcloudbase( qcloud, z, ter, pblh, cwbasecriteria, maxcwbasem, laglcwbase)
        #"BL Avg Wind"
        ublavgwind = ncl_jack_fortran.calc_blavg(uEW,z,ter,pblh )
        vblavgwind = ncl_jack_fortran.calc_blavg(vNS,z,ter,pblh )
        blavgwindspeed = np.sqrt(np.power(ublavgwind,2) + np.power(vblavgwind,2))
        #"Wind at BL Top"
        utop,vtop = ncl_jack_fortran.calc_bltopwind(uEW,vNS,z,ter,pblh  )
        bltopwindspeed = np.sqrt(np.power(utop,2) + np.power(vtop,2))
        #"BL Cloud Cover"
        blcldpct = ncl_jack_fortran.calc_subgrid_blcloudpct_grads( qvapor, qcloud, tc,pmb, z, ter, pblh, cwbasecriteria  )
        #"Thermal Updraft Velocity"
        wstar = ncl_jack_fortran.calc_wstar( vhf, pblh,0 )
        #"Height of Critical Updraft Strength"
        hwcrit= ncl_jack_fortran.calc_hcrit( wstar, ter, pblh)
        #"Cu Cloudbase ~I~where Cu Potential > 0~P~"
        zsfclcl=  ncl_jack_fortran.calc_sfclclheight( pmb, tc, td, z, ter, pblh )
        #"OvercastDevelopment Cloudbase"
        qvaporblavg=ncl_jack_fortran.calc_blavg(qvapor,z,ter,pblh )
        zblcl=ncl_jack_fortran.calc_blclheight( pmb, tc, qvaporblavg, z, ter, pblh )
        #"Thermalling Height"
        hglider_aux=np.minimum(hwcrit,zsfclcl)
        hglider=np.minimum(hglider_aux,zblcl)
        #"BL Top Uncertainty/Variability"
        bltopvariab= ncl_jack_fortran.calc_bltop_pottemp_variability( thetac, z, ter, pblh, criteriondegc)
        #"BL Vertical Wind Shear"
        blwindshear =ncl_jack_fortran.calc_blwinddiff(ua,va,z,ter,pblh)
    except Exception as e: 
        print('****Error computing dr jack vars postprocessing , functions.py****')
        print(e)

    # Save
    try:
        np.save(outputdir+'wblMxMn'+utch,np.transpose(wblMxMn))
        np.save(outputdir+'blcwbase'+utch,np.transpose(blcwbase))
        np.save(outputdir+'ublavgwind'+utch,np.transpose(ublavgwind))
        np.save(outputdir+'vblavgwind'+utch,np.transpose(vblavgwind))
        np.save(outputdir+'blavgwindspeed'+utch,np.transpose(blavgwindspeed))
        np.save(outputdir+'utop'+utch,np.transpose(utop))
        np.save(outputdir+'vtop'+utch,np.transpose(vtop))
        np.save(outputdir+'bltopwindspeed'+utch,np.transpose(bltopwindspeed))
        np.save(outputdir+'blcldpct'+utch,np.transpose(blcldpct))
        np.save(outputdir+'wstar'+utch,np.transpose(wstar))
        np.save(outputdir+'hwcrit'+utch,np.transpose(hwcrit))
        np.save(outputdir+'zsfclcl'+utch,np.transpose(zsfclcl))
        np.save(outputdir+'zblcl'+utch,np.transpose(zblcl))
        np.save(outputdir+'hglider'+utch,np.transpose(hglider))
        np.save(outputdir+'bltopvariab'+utch,np.transpose(bltopvariab))
        np.save(outputdir+'blwindshear'+utch,np.transpose(blwindshear))
    except Exception as e: 
        print('****Error saving dr jacks vars postprocessing , functions.py****')
        print(e)
    return dx,dy



def skewt_plots(dt,station,p,T,Td,u,v,outdir,idxij,utch,z):
    # skewt_plots(dt,station,p,T,Td,u,v,outdir,idxij,utch)
    # Function to make the graphic ploting of the sounding.
    # ---INPUTS:
    # dt = "2016-10-26 13h CET (12 UTC)" # string of valid time
    # station = "Piedtahita" station name
    # p pressure colmn on coordinates
    # T temp colmn on coordinates
    # Td dew point colmn on coordinates
    # u,v wind vectors colmn on coordinates    
    # outdir='plots/' #output directory
    # idxij matrix coordinates of the sounding
    # utch="1200" #string of utc hour for filename
    # z geopotential height
    # ---OUTPUTS:
    # plot in outdir 
    
    p=p.interp(south_north=idxij[1],west_east=idxij[0])
    lon=p.XLONG.values
    lat=p.XLAT.values
    dx=p.projection.dx
    dy=p.projection.dy
    p=p.values
    T=T.interp(south_north=idxij[1],west_east=idxij[0]).values
    Td=Td.interp(south_north=idxij[1],west_east=idxij[0]).values
    u=u.interp(south_north=idxij[1],west_east=idxij[0]).values
    v=v.interp(south_north=idxij[1],west_east=idxij[0]).values
    z=z.interp(south_north=idxij[1],west_east=idxij[0]).values
    ######################################################################
    # Make Skew-T Plot
    # ----------------
    # The code below makes a basic skew-T plot using the MetPy plot module
    # that contains a SkewT class.

    # Change default to be better for skew-T
    fig = plt.figure(figsize=(11, 9))
    plt.rcParams.update({'font.size': 12})
    # Initiate the skew-T plot type from MetPy class loaded earlier
    skew = SkewT(fig, rotation=45)

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
    skew.plot_barbs(p[::3], u[::3], v[::3], y_clip_radius=0.03)

    # Set some appropriate axes limits for x and y
    #skew.ax.set_xlim(-30, 40)
    skew.ax.set_ylim(1020, 200)
    skew.ax.set_ylabel('Pressure [hPa]') 
    skew.ax.set_xlabel('Temperature [ºC]') 

    heights = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]) * units.km
    std_pressures = mpcalc.height_to_pressure_std(heights)
    for height_tick, p_tick in zip(heights, std_pressures):
        trans, _, _ = skew.ax.get_yaxis_text1_transform(0)
        skew.ax.text(0.02, p_tick, '---{:~d}'.format(height_tick), transform=trans)

    
    # Calculate LCL height and plot as black dot. Because `p`'s first value is
    # ~1000 mb and its last value is ~250 mb, the `0` index is selected for
    # `p`, `T`, and `Td` to lift the parcel from the surface. If `p` was inverted,
    # i.e. start from low value, 250 mb, to a high value, 1000 mb, the `-1` index
    # should be selected.
    lcl_pressure, lcl_temperature = mpcalc.lcl(p[0]* units.hPa, T[0]* units.degC, Td[0]* units.degC)
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    # Calculate full parcel profile and add to plot as black line
    prof = mpcalc.parcel_profile(p* units.hPa, T[0]* units.degC, Td[0]* units.degC).to('degC')
    skew.plot(p, prof, 'k', linewidth=2)

    # Shade areas of CAPE and CIN
    skew.shade_cin(p* units.hPa, T* units.degC, prof)
    skew.shade_cape(p* units.hPa, T* units.degC, prof)
    
    # An example of a slanted line at constant T -- in this case the 0
    # isotherm
    skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)
    
    # Add the relevant special lines to plot throughout the figure
    skew.plot_dry_adiabats(t0=np.arange(233, 533, 10) * units.K,
                           alpha=0.6, color='orangered')
    skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K,
                             alpha=0.6, color='tab:green')
    #skew.plot_mixing_lines(p=np.arange(1000, 99, -20) * units.hPa,
    #                       linestyle='dotted', color='tab:blue')
    
    # Add some descriptive titles
    plt.title('Sounding '+station +'\n('+str('{0:.6f}'.format(lat))+' , '+str('{0:.6f}'.format(lon))+') ', loc='left')
    plt.title('Valid for: '+dt+'\n by RASPURI  ', loc='right')
    UTC_time = time.gmtime()
    plt.figtext(0.99, 0.01, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
    #plt.figtext(0.01, 0.01, 'RASPURI by Oriol Cevrelló ', horizontalalignment='right') 
    plt.tight_layout()
    filename=outdir+station+utch+'.png'
    #plt.show()
    plt.savefig(filename)
    plt.close()



def skewt_processing(dt,utch,outdir,filename,domain):
    #skewt_processing(dt,utch,outdir,filename,domain)
    #This functions computes and calls the plot for
    # a skewt Sounding plot, from the coordinates in
    # the var file.
    # ---INPUTS:
    # dt = "2016-10-26 13h CET (12 UTC)" # string of valid time
    # utch="1200" #string of utc hour for filename
    # outdir='plots/' #output directory
    # filename="wrfout_d02_2020-01-11_15_00_00"#filename to get the data
    # domain="02" #number of domain   
    # ---OUTPUTS:
    # none
    station = SOUNDINGS_NAMES#['MPX','MPX2']
    coordinates=SOUNDINGS#np.array([[46.46981, -9.091553] , [43.254, -6.158]])
    #########################################################################
    ##################   OPEN FILE
    #########################################################################
    try:
        ncfile = Dataset(filename)
    except Exception as e: 
        print('****Error opening file SkewT , functions.py****')
        print(e)
    #########################################################################
    ##################   READ VARS
    #########################################################################
    try:
        pres = getvar(ncfile, "pressure") # Pressure (hPa) 
        t = getvar(ncfile, "tc") # temperature in Celsius
        ua = getvar(ncfile, "ua", units="kt") # winds
        va = getvar(ncfile, "va", units="kt")        
        td  = getvar(ncfile, "td") #dew point temperature (C)
        lats = getvar(ncfile, "XLAT")
        lons = getvar(ncfile, "XLONG")
        z = getvar(ncfile, "z")
        lats=lats.values
        lons=lons.values
    except Exception as e: 
        print('****Error reading vars SkewT , functions.py****')
        print(e)
        
    for i in range(0,len(coordinates[:,0])):
        #########################################################################
        ##################   GET COORDINATES
        #########################################################################
        if(coordinates[i,0]<np.max(lats) and coordinates[i,0]>np.min(lats)
            and coordinates[i,1]<np.max(lons) and coordinates[i,1]>np.min(lons)):
            try:
                idxij=ll_to_xy_proj( latitude=coordinates[i,0],\
                longitude=coordinates[i,1],\
                as_int = False,\
                map_proj=ua.projection.map_proj,\
                truelat1=ua.projection.truelat1,\
                truelat2=ua.projection.truelat1,\
                stand_lon=ua.projection.stand_lon,\
                ref_lat=lats[0,0] , ref_lon=lons[0,0],\
                known_x=0 , known_y=0,\
                pole_lat=ua.projection.pole_lat , pole_lon=ua.projection.pole_lon,\
                dx=ua.projection.dx ,dy=ua.projection.dy)
            except Exception as e: 
                print('****Error geting coordinates SkewT, functions.py****')
                print(e)

        #########################################################################
        ##################   MAKE PLOT
        #########################################################################
            try:
                skewt_plots(dt,station[i],pres,t,td,ua,va,outdir,idxij,utch,z)
            except Exception as e: 
                print('****Error skewt_plots , functions.py****')
                print(e)
        else:
            print('****Sounding of station: '+station[i] +' out of bounds for domain '+domain+', functions.py****')


    
    
               
