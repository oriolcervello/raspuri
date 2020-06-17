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
# Dokerfile
# This script is part of RASPURI v2
# Dokerfile to build image with all dependencies and WRF engine

FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
  build-essential \
  csh \
  file \
  make\
  m4 \
  curl \
  git \
  curl \
  locales \
  coreutils \
  libgfortran3 \
  ftp \
  cron
#  vim 

   

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 \
  LANGUAGE=en_US.UTF-8 \
  LC_ALL=en_US.UTF-8
RUN update-locale 

RUN git clone https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew \
&& mkdir ~/.linuxbrew/bin \
&& ln -s ../Homebrew/bin/brew ~/.linuxbrew/bin \
&& eval $(~/.linuxbrew/bin/brew shellenv) \
&& brew update \
&& brew install gcc@9 \
&& brew install python \
&& brew install zlib \
&& brew install hdf5 \
&& brew install mpich \
&& brew install netcdf \
&& brew install pstree 

RUN eval $(~/.linuxbrew/bin/brew shellenv) \
&& cd root \
&& curl ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz --output wgrib2.tar \
&& cd .. \
&& tar -xvf root/wgrib2.tar -C root/ \
&& rm root/wgrib2.tar \
&& cd root/grib2 \
&& export CC=gcc-9 \
&& export FC=gfortran-9 \
&& make

RUN eval $(~/.linuxbrew/bin/brew shellenv) \
&& pip3 install ntplib \
&& pip3 install pytz \
&& pip3 install numpy \
&& pip3 install matplotlib \
&& pip3 install xarray \
&& pip3 install netCDF4 \
&& pip3 install rasterio \
&& pip3 install scipy  \
&& pip3 install metpy \
&& pip3 install Pillow \
&& pip3 install wrf-python

RUN git clone https://github.com/wrf-model/WRF ~/WRF \
&& git clone https://github.com/wrf-model/WPS ~/WPS 

COPY configRASPURI.sh root/

#WORKDIR /root/

#### INSTRUCTIONS ####
#sudo docker build -t oriolcervello/raspuri:image .
#sudo docker run -it oriolcervello/raspuri:image bash
#check version of netcdf and HDF5
#bash configRASPURI.sh
#rm configRASPURI.sh
#sudo docker container ls --all
#sudo docker commit -m "raspuri" IDcontainer oriolcervello/raspuri:wrf



















