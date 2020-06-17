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

