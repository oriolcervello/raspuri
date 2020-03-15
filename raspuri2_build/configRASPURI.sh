#!/bin/bash  
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
# configRASPURI.sh
# This script is part of RASPURI v2
# Script to compile WRF and WPS and finish installation of dependencies


#bash configRASPURI.sh



eval $(~/.linuxbrew/bin/brew shellenv) 
#check versions
export NETCDF=/root/.linuxbrew/Cellar/netcdf/4.7.3_2 \
HDF5=/root/.linuxbrew/Cellar/hdf5/1.12.0 \
JASPERLIB=/root/grib2/lib \
JASPERINC=/root/grib2/include \
WGRIB=/root/grib2 \
# number of cores to parallel compile
J='-j 4' \
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

cd ../RASPURI
bash links.sh
rm links.sh
#borrar configRASP



#rm configRASPURI.sh



