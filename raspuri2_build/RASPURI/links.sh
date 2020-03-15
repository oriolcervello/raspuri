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
# links.sh
# This script is part of RASPURI v2
# Script to set som links during the configuration process
#***BIN FOLDERS***           cal???

ln -s ../../.linuxbrew/lib /bin/.lib
mkdir bin/geogrid
ln -s ../../../WPS/geogrid/GEOGRID.TBL bin/geogrid/GEOGRID.TBL
ln -s ../../../WPS/geogrid/GEOGRID.TBL.ARW bin/geogrid/GEOGRID.TBL.ARW
mkdir bin/metgrid
ln -s ../../../WPS/metgrid/METGRID.TBL bin/metgrid/METGRID.TBL
ln -s ../../../WPS/metgrid/METGRID.TBL.ARW bin/metgrid/METGRID.TBL.ARW
mkdir bin/ungrib
ln -s ../../../WPS/ungrib/Variable_Tables bin/ungrib/Variable_Tables

#***BIN FILES***
ln -s ../../grib2/wgrib2 bin/wgrib
ln -s ../../grib2/wgrib2 bin/cnvgrib
#NO esta cnvgrib
#grib_set -s edition=2 yourgribfile.grib
#wgrib2 -g21 grib2filename -o converted_grib1_file.out
#cnvgrib -g21 input(grib2) output(grib1)
#cnvgrib -g12 input(grib1) output(grib2)


ln -s ../../WPS/metgrid.exe bin/metgrid.exe
ln -s ../../WPS/geogrid.exe bin/geogrid.exe
ln -s ../../WPS/ungrib.exe bin/ungrib.exe
ln -s ../../WPS/link_grib.csh bin/link_grib.csh
ln -s ../../WPS/util/g1print.exe bin/g1print.exe
ln -s ../../WPS/util/g2print.exe bin/g2print.exe
ln -s ../../WPS/util/height_ukmo.exe bin/height_ukmo.exe
ln -s ../../WPS/util/int2nc.exe bin/int2nc.exe
ln -s ../../WPS/util/mod_levs.exe bin/mod_levs.exe
ln -s ../../WPS/util/avg_tsfc.exe bin/avg_tsfc.exe
ln -s ../../WPS/util/calc_ecmwf_p.exe bin/calc_ecmwf_p.exe
ln -s ../../WPS/util/plotfmt_nc.ncl bin/plotfmt_nc.ncl
#ln -s ../../WPS/util/plotgrids.exe  bin/plotgrids.exe 
#ln -s ../../WPS/util/plotfmt.exe  bin/plotfmt.exe
ln -s ../../WPS/util/plotgrids.ncl bin/plotgrids.ncl
ln -s ../../WPS/util/rd_intermediate.exe bin/rd_intermediate.exe


ln -s ../../WRF/run/ndown.exe bin/ndown.exe
ln -s ../../WRF/run/real.exe bin/real.exe
ln -s ../../WRF/run/wrf.exe bin/wrf.exe
ln -s ../../WRF/run/tc.exe bin/tc.exe






#***TABLES***      
mkdir RUN.TABLES
ln -s ../../WRF/run/GENPARM.TBL RUN.TABLES/GENPARM.TBL
ln -s ../../WRF/run/VEGPARM.TBL RUN.TABLES/VEGPARM.TBL
ln -s ../../WRF/run/SOILPARM.TBL RUN.TABLES/SOILPARM.TBL
ln -s ../../WRF/run/LANDUSE.TBL RUN.TABLES/LANDUSE.TBL
ln -s ../../WRF/run/RRTM_DATA RUN.TABLES/RRTM_DATA
ln -s ../../WRF/run/ETAMPNEW_DATA.expanded_rain RUN.TABLES/ETAMPNEW_DATA.expanded_rain

ln -s ../../WPS/geogrid/GEOGRID.TBL RUN.TABLES/GEOGRID.TBL
ln -s ../../WPS/metgrid/METGRID.TBL.ARW RUN.TABLES/METGRID.TBL
ln -s ../../WPS/metgrid/METGRID.TBL.ARW RUN.TABLES/METGRID.TBL.ARW

ln -s ../../WPS/ungrib/Variable_Tables/Vtable.GFS RUN.TABLES/Vtable.GFS
ln -s ../../WPS/ungrib/Variable_Tables/Vtable.GFS RUN.TABLES/Vtable
ln -s ../../WPS/ungrib/Variable_Tables/Vtable.NAM RUN.TABLES/Vtable.NAM


#***REGION***
ln -s ../../WRF/run/ETAMPNEW_DATA.expanded_rain region/ETAMPNEW_DATA.expanded_rain
cd region
ln -s ../../WRF/run/*_DATA .
ln -s ../../WRF/run/*.TBL .
ln -s ../../WRF/run/tr* .
ln -s ../../WRF/run/*.txt .
ln -s ../../WRF/run/*.tbl .
ln -s ../../WRF/run/ozone* .
cd ..

ln -s ../../WPS/metgrid/METGRID.TBL region/
ln -s ../../WPS/geogrid/GEOGRID.TBL region/
ln -s ../../WPS/ungrib/Variable_Tables/Vtable.GFS region/Vtable
