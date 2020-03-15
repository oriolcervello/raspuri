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
# 
# This script is part of RASPURI v2
# Script to check ncl_jack_fortran lib
import ncl_jack_fortran
print(ncl_jack_fortran.__doc__)
print(ncl_jack_fortran.calc_wblmaxmin.__doc__)
print(ncl_jack_fortran.calc_blcloudbase.__doc__)
print(ncl_jack_fortran.calc_blavg.__doc__)
print(ncl_jack_fortran.calc_bltopwind.__doc__)
print(ncl_jack_fortran.calc_subgrid_blcloudpct_grads.__doc__)
print(ncl_jack_fortran.calc_wstar.__doc__)
print(ncl_jack_fortran.calc_hcrit.__doc__)
print(ncl_jack_fortran.calc_sfclclheight.__doc__)
print(ncl_jack_fortran.calc_blclheight.__doc__)
print(ncl_jack_fortran.calc_bltop_pottemp_variability.__doc__)
print(ncl_jack_fortran.calc_blwinddiff.__doc__)
#bparam = ncl_jack_fortran.calc_wblmaxmin(linfo,wa,z,ter,pblh,bparam,[isize,jsize,ksize])




#########################################################################
##################   NEEDED
#########################################################################


#pip3 install wrf-python
#pip3 install netCDF4
#pip3 install numpy wrapt setuptools matplotlib
#pip install xarray
#pip install scipy 

#f2py3.6 -c -m ncl_jack_fortran ncl_jack_fortran.f

