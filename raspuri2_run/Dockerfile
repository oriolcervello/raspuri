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
# Dokerfile
# This script is part of RASPURI v2
# Script to build the Running image of RASPURI
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



#### INSTRUCTIONS ####
#sudo docker build -t raspuri .
#sudo docker run --rm --name raspuri2 -d -v /home/ori/data/geog:/root/RASPURI/geog -v /home/ori/OUT:/root/RASPURI/region/OUT raspuri


