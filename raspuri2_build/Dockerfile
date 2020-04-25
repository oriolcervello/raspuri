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
# Dokerfile
# This script is part of RASPURI v2
# Dokerfile to build image with all dependencies

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
COPY RASPURI root/RASPURI

# Copy hello-cron file to the cron.d directory
COPY raspuri-cron /etc/cron.d/raspuri-cron

WORKDIR /root/

#### INSTRUCTIONS ####
#sudo docker build -t oriolcervello/raspuri:image .
#sudo docker run -it oriolcervello/raspuri:image bash
#check version of netcdf and HDF5
#bash configRASPURI.sh
#rm configRASPURI.sh
#sudo docker container ls --all
#sudo docker commit -m "raspuri" IDcontainer oriolcervello/raspuri:compiled



















