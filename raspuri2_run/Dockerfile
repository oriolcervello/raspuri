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
# Script to build the local RASPURI
FROM oriolcervello/raspuri:compiled
ENV BASEDIR=/root/RASPURI
COPY Cat/* $BASEDIR/region/
COPY variables.py $BASEDIR/region

COPY raspuri-cron /etc/cron.d/raspuri-cron


# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/raspuri-cron

# Apply cron job
RUN crontab /etc/cron.d/raspuri-cron

# Run the command on container startup
CMD ["cron", "-f"]




#sudo docker build -t raspuri .

#sudo docker run --rm --name raspuri2 -d -v /home/ori/data/geog:/root/RASPURI/geog -v /home/ori/OUT:/root/RASPURI/region/OUT raspuri


