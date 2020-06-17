#==========================================================================
#   Oriol Cervelló i Nogués, ( raspuri [at] protonmail.com ).
#   RASPURI v2. github.com/oriolcervello/raspuri
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
#Dockerfile
#To build nginx server
FROM nginx

RUN rm /etc/nginx/conf.d/default.conf \
&& rm /etc/nginx/nginx.conf

COPY web-rasp/ /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/
COPY default.conf /etc/nginx/conf.d/

# sudo docker build -t webrasp .
# sudo docker run --name webR --rm -p 80:80 -d -v /home/ori/OUT:/usr/share/nginx/html/OUT webrasp




