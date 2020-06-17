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
# 
# This script is part of RASPURI v2
# Script used to develop and test the skewT graphics
from datetime import datetime
from wrf import to_np, getvar, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords, vinterp, interplevel, ll_to_xy_proj
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from metpy.plots import SkewT
from metpy.units import pandas_dataframe_to_unit_arrays, units
import numpy as np
#from variables import SERVER, WAIT_FTP_START, PLOT_STYLE, SOUNDINGS,SOUNDINGS_NAMES

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
    fig = plt.figure(figsize=(9, 11))

    # Initiate the skew-T plot type from MetPy class loaded earlier
    skew = SkewT(fig, rotation=45)
    
    par1 = skew.twinx()
    par2 = skew.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))

    par2.axis["right"].toggle(all=True)

    # Plot the data using normal plotting functions, in this case using
    # log scaling in Y, as dictated by the typical meteorological plot
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
    skew.plot_barbs(p[::3], u[::3], v[::3], y_clip_radius=0.03)

    # Set some appropriate axes limits for x and y
    #skew.ax.set_xlim(-30, 40)
    skew.ax.set_ylim(1020, 200)
    

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
                           alpha=0.4, color='orangered')
    skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K,
                             alpha=0.4, color='tab:green')
    #skew.plot_mixing_lines(p=np.arange(1000, 99, -20) * units.hPa,
    #                       linestyle='dotted', color='tab:blue')
    p3 = par2.plot(p, z, label="Height")
    # Add some descriptive titles
    plt.title('Sounding '+station +'\n('+str(lat)+' , '+str(lon)+') ', loc='left')
    plt.title('Valid for: '+dt+'\n by RASPURI  ', loc='right')
    UTC_time = time.gmtime()
    plt.figtext(0.99, 0.01, time.strftime('Computed on %d/%m/%y %H:%M:%S UTC \n', UTC_time)+ 'dx: '+str(dx)+'m dy: '+str(dy)+'m ', horizontalalignment='right', fontsize=10) 
    plt.figtext(0.01, 0.01, 'RASPURI by Oriol Cevrelló ', horizontalalignment='right') 
    filename=outdir+station+utch+'.png'
    #plt.show()
    plt.savefig(filename)
    plt.close()



def skewt_processing(dt,utch,outdir,filename,domain):
    ######################################################################
    # INPUTS
    #
    #dt = "2016-10-26 13h CET (12 UTC)"
    #utch="1200"
    station = ['MPX','MPX2']
    #outdir='aa/'
    #filename="wrfout_d02_2020-01-11_15_00_00"
    coordinates=np.array([[46.46981, -9.091553] , [43.254, -6.158]])
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
        ua = getvar(ncfile, "ua") # winds
        va = getvar(ncfile, "va")
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
    try:

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

            try:
                skewt_plots(dt,station[i],pres,t,td,ua,va,outdir,idxij,utch,z)
            except Exception as e: 
                print('****Error skewt_plots , functions.py****')
                print(e)
        else:
            print('****Sounding of station: '+station[i] +' out of bounds for domain '+domain+', functions.py****')




skewt_processing("2016-10-26 13h CET (12 UTC)","02",".","wrfout_d01_2020-01-20_10:00:00","02")
