#!/bin/bash  
#==========================================================================
#   RASPURI v2. github.com/oriolcervello/raspuri
#   Oriol Cervelló i Nogués, ( raspuri [at] protonmail.com ).
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
# configRASPURI.sh
# This script is part of RASPURI v2
# Script to compile WRF and WPS and finish installation of dependencies


#bash configRASPURI.sh



eval $(~/.linuxbrew/bin/brew shellenv) 
#check versions
NETCDF="$(echo /root/.linuxbrew/Cellar/netcdf/*)"
HDF5="$(echo /root/.linuxbrew/Cellar/hdf5/*)"

# number of cores to parallel compile
J="-j $(nproc)"

export NETCDF \
HDF5 \
JASPERLIB=/root/grib2/lib \
JASPERINC=/root/grib2/include \
WGRIB=/root/grib2 \
J \
CC=gcc-9 \
CXX=g++-9 \
FC=gfortran-9 \
F77=gfortran-9	
export PATH=$WGRIB:$PATH 



cd WRF 
./configure 
#34 1  (dmpar GNU gfortran)
./compile em_real
# fer que sigui compilador v9
#SFC             =       gfortran
#SCC             =       gcc
#CCOMP           =       gcc
cd ../WPS
./clean
./configure
#1 (serial gfortran with GRIB2)
./compile
#./compile plotfmt
#./compile plotgrids




#rm configRASPURI.sh



