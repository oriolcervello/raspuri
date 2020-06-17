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

FROM oriolcervello/raspuri:wrf


COPY RASPURI /root/RASPURI


RUN cd /root/RASPURI \
&& bash links.sh \
&& rm links.sh

WORKDIR /root/

#### INSTRUCTIONS ####
#sudo docker build -t oriolcervello/raspuri:compiled .




















