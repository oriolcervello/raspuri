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
# variables.py
# This script is part of RASPURI v2
# Script to set variables for the program
import numpy as np
#TIMES
T_ZONE = 'CET' #list of possible TZ https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
DAYS_TO_PROCESS = 3 #max 5
START_HH = 10 #local time
END_HH = 18 #local time, max 23
DOMAINS = 2
#HOURS_TO_AVOID = 6 #h to avoid from processing, forecast will start and end h hours latter to avoid forecasting the processing hour
#NAMELIST INPUT AND WPS LINES
BEGIN_INPUT_LINES=2
END_INPUT_LINE=18
BEGIN_WPS_LINES=4
END_WPS_LINE=6
#SOUNDINGS
SOUNDINGS=np.array([[41.494712, 1.209950] , 
                    [42.045788, 0.745994] ,
                    [42.008857, 0.750079] ,
                    [42.227622, 1.324271] ,
                    [42.137173, 1.772629] ,
                    [42.099635, 2.293433] ,
                    [42.523919, 0.499515] ,
                    [42.105681, 1.824481] ,
                    [42.509786, 1.988950] ])
SOUNDINGS_NAMES= ['Belltall',
                  'Ager Desp.',
                  'Ager Vall',
                  'Organya',
                  'Rasos',
                  'Bellmunt',
                  'Castejon de Sos',
                  'Berga - Rampa',
                  'Pic Moros']

#PLOT TYPE
PLOTTYPELAYER=True
#DOTS IN MAPS
DOTY = [41.494712,42.045788,42.227622,42.137173,42.099635,42.523919] #LAT
DOTX = [1.209950,0.745994,1.324271,1.772629,2.293433,0.499515] #LON
DOTTITLE = ['Belltall', 'Ager','Organya','Rasos','Bellmunt','Castejon']
TOPOFILES=['B1','C1'] # look https://visibleearth.nasa.gov/grid
#FTP SETTINGS
SYMULTANEOUS_FTP = 5
WAIT_FTP = 75 # sec, wait time out to download file = WAIT_FTP*12
WAIT_FTP_START = 200 # sec
SERVER = 'ftp.ncep.noaa.gov' #server ftp
#OTHERS
NUM_CPUS_WRF = 7
TESTING=False #for debug

