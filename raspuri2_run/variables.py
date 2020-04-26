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
HOURS_TO_AVOID = 6 #h to avoid from processing, forecast will start and end h hours latter to avoid forecasting the processing hour
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

