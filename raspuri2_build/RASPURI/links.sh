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
# links.sh
# This script is part of RASPURI v2
# Script to set some links during the creation of the Docker image


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
