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
# Script to test an develop the postprocessing
#########################################################################
##################   SAVE VARS TO PLOT
#########################################################################


from netCDF4 import Dataset
from wrf import to_np, getvar, smooth2d, get_cartopy, cartopy_xlim, cartopy_ylim, latlon_coords, vinterp, interplevel
#import matplotlib.pyplot as plt
#from matplotlib.cm import get_cmap
#import cartopy.crs as crs
import numpy as np
import ncl_jack_fortran

#########################################################################
##################   OPEN FILE
#########################################################################
ncfile = Dataset("wrfout_d02_2020-01-11_15_00_00")
outputdir='aaaaa/'

#########################################################################
##################   GET VARS
#########################################################################


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
t2 = getvar(ncfile, "T2")# TEMP at 2 M (k)
uv  = getvar(ncfile, "uvmet") # u,v NOT rotated to grid   in m/s
p  = getvar(ncfile, "P") #"perturbation pressure"
pb  = getvar(ncfile, "PB") #"BASE STATE PRESSURE"
hfx  = getvar(ncfile, "HFX") #for sfc. sensible heat flux in w/m2	142
thetac =getvar(ncfile, "T")+ 26.85 #"perturbation potential temperature theta-t0"
qvapor  = getvar(ncfile, "QVAPOR") #"Water vapor mixing ratio" 
vhf  = getvar(ncfile, "LH") #"LATENT HEAT FLUX AT THE SURFACE" 
td  = getvar(ncfile, "td") #dew point temperature (C)
snow  = getvar(ncfile, "SNOW")#"SNOW WATER EQUIVALENT"
rainc = getvar(ncfile, "RAINC")#"ACCUMULATED TOTAL CUMULUS PRECIPITATION"
rainnc = getvar(ncfile, "RAINNC")#"ACCUMULATED TOTAL GRID SCALE PRECIPITATION"
snowh  = getvar(ncfile, "SNOWH")#"PHYSICAL SNOW DEPTH"

pblh=bldepth
#lats, lons = latlon_coords(slp)
lats = getvar(ncfile, "XLAT")
lons = getvar(ncfile, "XLONG")

#########################################################################
##################   VARS TRANSFORMATIONS
#########################################################################



#SHAN DE MOURE ELS AXIS

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
smooth_slp = smooth2d(slp, 3, cenweight=4) # Smooth the sea level pressure since it tends to be noisy near the mountains
sfctemp = t2 - 273.16 #Surface temp
hbl_mag = pblh.values + ter.values   #"Height of BL Top
wspd10=wspd_wdir10[0,:]  #Surface wind speed
wdir10=wspd_wdir10[1,:] #Surface wind dir
mcape=cape_2d[0,:,:] 
mcin=cape_2d[1,:,:] 
lcl=cape_2d[2,:,:] 
lfc=cape_2d[3,:,:] 
rainTot = rainc + rainnc

# Auxiliars dr jack
uEW = uv[0,:,:]                           
vNS = uv[1,:,:]                         
pmb=var = 0.01*(p.values+pb.values) # press is vertical coordinate in mb
vhf=np.clip(vhf.values,a_min=0, a_max = np.max(vhf.values)) 
vhf = hfx +  0.000245268*(t[0,:,:]+273.16)*vhf

#########################################################################
##################   SAVE
#########################################################################
np.save(outputdir+'mcape',mcape.values)
np.save(outputdir+'mcin',mcin.values)
np.save(outputdir+'lcl',lcl.values)
np.save(outputdir+'lfc',lfc.values)
np.save(outputdir+'sfctemp',to_np(sfctemp))
np.save(outputdir+'bldepth',to_np(bldepth))
np.save(outputdir+'wspd10',to_np(wspd10))
np.save(outputdir+'wdir10',to_np(wdir10))
np.save(outputdir+'pw',to_np(pw))
np.save(outputdir+'ctt',ctt.values)
np.save(outputdir+'hbl',hbl_mag)
np.save(outputdir+'cloudfrac_low',cloudfrac_low.values)
np.save(outputdir+'cloudfrac_mid',cloudfrac_mid.values)
np.save(outputdir+'cloudfrac_high',cloudfrac_high.values)
np.save(outputdir+'lons',to_np(lons))
np.save(outputdir+'lats',to_np(lats))
np.save(outputdir+'slp',to_np(smooth_slp))
np.save(outputdir+'hfx',to_np(hfx))
np.save(outputdir+'snow',to_np(snow))
np.save(outputdir+'rainTot',to_np(rainTot))
np.save(outputdir+'snowh',to_np(snowh))

np.save(outputdir+'ht_500',ht_500.values)
np.save(outputdir+'wdir_500',wdir_500.values)
np.save(outputdir+'wspd_500',wspd_500.values)
np.save(outputdir+'t_500',t_500.values)

np.save(outputdir+'ht_700',ht_700.values)
np.save(outputdir+'wdir_700',wdir_700.values)
np.save(outputdir+'wspd_700',wspd_700.values)
np.save(outputdir+'t_700',t_700.values)

np.save(outputdir+'ht_925',ht_925.values)
np.save(outputdir+'wdir_925',wdir_925.values)
np.save(outputdir+'wspd_925',wspd_925.values)
np.save(outputdir+'t_925',t_925.values)

#########################################################################
##################   DR jack transf
#########################################################################
# Variables
size=(z.values).shape
nz       = size[0]
ny       = size[1]
nx       = size[2]
'''
wblMxMn = np.zeros((nx, ny))
blcwbase = np.zeros((nx, ny))
ublavgwind = np.zeros((nx, ny))
vblavgwind =np.zeros((nx, ny))
utop =np.zeros((nx, ny))
vtop =np.zeros((nx, ny))
wstar=np.zeros((nx, ny))
hwcrit=np.zeros((nx, ny))
'''
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
time = 0	# Seems time is always 0 for DrJack's code
cdbl = 0.003	# Coefficient of Drag for Boundary Layer 
cwbasecriteria = 0.000010	# Cloud Water criterion

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


# Save
np.save(outputdir+'wblMxMn',np.transpose(wblMxMn))
np.save(outputdir+'blcwbase',np.transpose(blcwbase))
np.save(outputdir+'ublavgwind',np.transpose(ublavgwind))
np.save(outputdir+'vblavgwind',np.transpose(vblavgwind))
np.save(outputdir+'blavgwindspeed',np.transpose(blavgwindspeed))
np.save(outputdir+'utop',np.transpose(utop))
np.save(outputdir+'vtop',np.transpose(vtop))
np.save(outputdir+'bltopwindspeed',np.transpose(bltopwindspeed))
np.save(outputdir+'blcldpct',np.transpose(blcldpct))
np.save(outputdir+'wstar',np.transpose(wstar))
np.save(outputdir+'hwcrit',np.transpose(hwcrit))
np.save(outputdir+'zsfclcl',np.transpose(zsfclcl))
np.save(outputdir+'zblcl',np.transpose(zblcl))
np.save(outputdir+'hglider',np.transpose(hglider))
np.save(outputdir+'bltopvariab',np.transpose(bltopvariab))
np.save(outputdir+'blwindshear',np.transpose(blwindshear))


#
#


