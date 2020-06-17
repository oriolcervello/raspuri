#########################################################################
#########################################################################
##################   RASPURI v2 by Oriol Cervelló
#########################################################################
#########################################################################
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
# rasp.py
# This script is part of RASPURI v2
# Main script runing the rasp

#########################################################################
##################   WELCOME
#########################################################################
try:
    import time
    #import ntplib
    import calendar
    import os
    import re
    from pathlib import Path
    from datetime import datetime
    from pytz import timezone
    from variables import DAYS_TO_PROCESS, START_HH, END_HH, DOMAINS, BEGIN_INPUT_LINES, END_INPUT_LINE, BEGIN_WPS_LINES, END_WPS_LINE, SYMULTANEOUS_FTP, NUM_CPUS_WRF, WAIT_FTP,T_ZONE,TESTING
    import functions 
    import plot 
    import sys
    sys.stdout = open('OUT/rasppy.log', 'a')
except Exception as e: 
    print(e)
    print('****ERROR importing externals, main.py****')
    exit() 
UTC_time = time.gmtime()
UTC_time_sec = calendar.timegm(UTC_time)
#local_time_secs = UTC_time_sec + (HH_ZONE*3600)
#local_time = time.gmtime(local_time_secs)
local_time=datetime.now(timezone(T_ZONE)).timetuple()
local_time_secs=calendar.timegm(local_time)
HH_ZONE=int((local_time_secs-UTC_time_sec)/3600)
print('****WELCOME TO RASPURI****')
print("""==========================================================================
   RASPURI v2 a RASP(Regional Atmospheric
   Soaring Predictions) COMPUTER PROGRAM
   Original Creator: Oriol Cervelló i Nogués ( raspuri [at] protonmail.com )
   Copyright (C) 2019+ by Oriol Cervelló i Nogués
==========================================================================
 License: GNU GPLv3.0
 Copyright (C) 2019  Oriol Cervelló

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
==========================================================================
==========================================================================""")
print('****RASPURI starting at: ' + time.strftime('%Y-%m-%d %H:%M:%S', local_time) +' TZ: '+T_ZONE+'-> '+str(HH_ZONE) +'h****')

#########################################################################
##################   CLEAN PREVIOUS RUN
#########################################################################
os.system("find OUT/data/ -type d -name '20*' -mtime +7 -exec rm -rf {} \;")
os.system("find OUT/plot/ -type d -name '20*' -mtime +7 -exec rm -rf {} \;")
os.system('rm -rf OUT/LOG/*')
os.system('rm -f OUT/data/wrf*')
#########################################################################
##################   SET TIMES
#########################################################################
#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)
hour = int(sys.argv[1])


if(hour == 0):
    plusday=0
    processing_time_str = time.strftime('%Y-%m-%d 00:%M:%S', UTC_time)
    processing_time = time.strptime(processing_time_str, '%Y-%m-%d %H:%M:%S')
    processing_time_secs = calendar.timegm(processing_time)
elif(hour == 6 ):
    plusday=0
    processing_time_str = time.strftime('%Y-%m-%d 06:%M:%S', UTC_time)
    processing_time = time.strptime(processing_time_str, '%Y-%m-%d %H:%M:%S')
    processing_time_secs = calendar.timegm(processing_time)
elif(hour == 12 ):
    plusday=1
    processing_time_str = time.strftime('%Y-%m-%d 12:%M:%S', UTC_time)
    processing_time = time.strptime(processing_time_str, '%Y-%m-%d %H:%M:%S')
    processing_time_secs = calendar.timegm(processing_time)
elif(hour == 18):
    plusday=1
    processing_time_str = time.strftime('%Y-%m-%d 18:%M:%S', UTC_time)
    processing_time = time.strptime(processing_time_str, '%Y-%m-%d %H:%M:%S')
    processing_time_secs = calendar.timegm(processing_time)
else:
    print('****ERROR hour from cron is not valid, main.py****')
    exit() 

start_HH_UTC = START_HH - HH_ZONE
end_HH_UTC = END_HH - HH_ZONE
#########################################################################
##################   GET GFS FILESNAMES
#########################################################################
try:
    flienames = []
    hours_downloaded = []
    foldername = 'gfs.' +time.strftime('%Y%m%d', processing_time)
    foldername_h = str('{0:02}'.format(hour))
    end_hh_aux=END_HH+1
    if (end_hh_aux>23):
        end_hh_aux=23
    if (DAYS_TO_PROCESS>5):  
          DAYS_TO_PROCESS=5
    for i in range(0,DAYS_TO_PROCESS):    
        for j in range(START_HH,end_hh_aux):
            download_hour = j - HH_ZONE - (processing_time.tm_hour) + plusday*24
            if(download_hour < 0):          
                flienames.append('gfs.t'+str('{0:02}'.format(hour))+'z.pgrb2.0p25.f'+str('{0:03}'.format(download_hour + 24 + i*24)))
                hours_downloaded.append(download_hour + 24 + i*24)
            else:            
                flienames.append('gfs.t'+str('{0:02}'.format(hour))+'z.pgrb2.0p25.f'+str('{0:03}'.format(download_hour + i*24)))
                hours_downloaded.append(download_hour + i*24)

    flienames.sort()

except Exception as e: 
    print(e)
    print('****ERROR something went wrong getting the filenames, main.py****')
    exit() 
#########################################################################
##################   MANAGE TIMES
#########################################################################
try:
    hours_downloaded.sort()
    namelist_times = []

    for i in range(0,len(hours_downloaded)):
        namelist_times.append(time.gmtime((processing_time_secs) + (hours_downloaded[i]*60*60)))
         
    process_rounds = 0    
    start_h = hours_downloaded[0]
    run_h = []
    start_tims_s = [namelist_times[0]]
    end_tims_s = []
    aux_h = 0

    for z in range(1,len(hours_downloaded)):
        if(start_h+1 == hours_downloaded[z]):
            aux_h = aux_h +1
            start_h = hours_downloaded[z]
        else:
            #namelist_times[z-1]= time.gmtime(calendar.timegm(namelist_times[z-1]) +3600)
            end_tims_s.append(namelist_times[z-1])
            start_tims_s.append(namelist_times[z])
            process_rounds = process_rounds +1 
            start_h = hours_downloaded[z]
            run_h.append(aux_h)
            aux_h = 0

    end_tims_s.append(namelist_times[len(hours_downloaded) -1 ])
    process_rounds = process_rounds +1
    run_h.append(aux_h)

    print('****Processings scheduled: ' + str(process_rounds) + ' ****')
    for round in range(0,process_rounds):
        print('****Processing round : ' + str(round+1) + ' Starts at:' + time.strftime('%Y-%m-%d %H:00:00Z ', start_tims_s[round]) + ' Ends at:' + time.strftime('%Y-%m-%d %H:00:00Z ', end_tims_s[round]) + ' Round of: ' + str(run_h[round]) + 'h****')
except Exception as e: 
    print(e)
    print('****ERROR something went wrong managing times, main.py****')
    exit() 


#########################################################################
##################   DOWNLOAD GFS FILES
#########################################################################

count = 0
count_downloading = 0
count_downloaded = 0
list_downloaded=[]
f = open('downloaded.txt', 'w')
f.close() 
#CHECK TO START DOWNLOADING
functions.check_start_download(foldername,foldername_h,flienames[0])
try:
    while(count_downloaded != len(flienames)):
        if(count_downloading <= SYMULTANEOUS_FTP and count < len(flienames)):
            print('****Calling ftp download for: ' + flienames[count] + '****')
            os.system('bash ftp_bash.sh ' + foldername + ' ' + foldername_h + ' ' + flienames[count] )
            count = count + 1
            count_downloading = count_downloading + 1
            time.sleep(WAIT_FTP/4)
        else:    
            count_downloaded = 0  
            list_downloaded=[]
            f = open('downloaded.txt', 'r')
            list_downloaded = f.read().splitlines()
            f.close()             
            for i in range(0,len(flienames)):
                if(flienames[i] in list_downloaded):
                    count_downloaded = count_downloaded + 1
            print('**** ' + str(count_downloaded) + ' files downloaded out of ' + str(len(flienames)) + '****')
            if(count - count_downloaded < SYMULTANEOUS_FTP and count < len(flienames)):
                count_downloading = count - count_downloaded
            elif(count_downloaded == len(flienames)):
                pass
            else:
                print('****Waiting for files to downlaod ' + str(WAIT_FTP) + ' s****')
                time.sleep(WAIT_FTP)
        print('****Downloading ' + str(count_downloading) + ' files****')
    
    print('****All files downloadad, continuing...****')
    os.system('rm downloaded.txt')
except Exception as e: 
    print(e)
    print('****ERROR something went wrong with the FTP downloading, main.py****')
    exit() 

#########################################################################
##################   START PROCESSING
#########################################################################
UTC_time = time.gmtime()
UTC_time_sec = calendar.timegm(UTC_time)
proc_time_secs = UTC_time_sec + (HH_ZONE*3600)
proc_time = time.gmtime(proc_time_secs)
print('****Processing starting at: ' + time.strftime('%Y-%m-%d %H:%M:%S', proc_time) + ' ****')


for round in range(0,process_rounds):
    #########################################################################
    ##################   WRITE NAMELISTS TIMES
    #########################################################################
    try:
        print('****Updating namelist dates****')
        if(os.path.isfile('namelist.input') and os.path.isfile('namelist.wps')):
            name_inp_times = [ 'run_days                 = 0,',
                        'run_hours                = ' + str(run_h[round]) + ',',
                        'run_minutes              = 0,',
                        'run_seconds              = 0,',
                        'start_year               = ' + str(start_tims_s[round].tm_year) + ', ',
                        'start_month              = '+ str(start_tims_s[round].tm_mon) +', ',
                        'start_day                = '+ str(start_tims_s[round].tm_mday) +', ',
                        'start_hour               = '+ str(start_tims_s[round].tm_hour) + ', ',
                        'start_minute             = 00, ',
                        'start_second             = 00, ',
                        'end_year                 = ' + str(end_tims_s[round].tm_year) + ', ',
                        'end_month                = '+ str(end_tims_s[round].tm_mon) +', ',
                        'end_day                  = '+ str(end_tims_s[round].tm_mday) +', ',
                        'end_hour                 = '+ str(end_tims_s[round].tm_hour) + ', ',
                        'end_minute               = 00, ',
                        'end_second               = 00, ',
                        'interval_seconds         = '  + str(run_h[round] * 3600) +',']

            name_wps_times = [ 'start_date           = ' + time.strftime('\'%Y-%m-%d_%H:00:00\'', start_tims_s[round]) + ', ',
                            'end_date             = ' + time.strftime('\'%Y-%m-%d_%H:00:00\'', end_tims_s[round]) + ', ',
                            'interval_seconds         = '  + str(run_h[round] * 3600) +',']

            for dom in range(1,DOMAINS):
                name_inp_times[4] = name_inp_times[4]+ str(start_tims_s[round].tm_year) + ', '
                name_inp_times[5] = name_inp_times[5]+ str(start_tims_s[round].tm_mon) +', '
                name_inp_times[6] = name_inp_times[6]+ str(start_tims_s[round].tm_mday) +', '
                name_inp_times[7] = name_inp_times[7]+ str(start_tims_s[round].tm_hour) + ', '
                name_inp_times[8] = name_inp_times[8] +' 00, '
                name_inp_times[9] = name_inp_times[9]+' 00, '
                name_inp_times[10] = name_inp_times[10] + str(end_tims_s[round].tm_year) + ', '
                name_inp_times[11] = name_inp_times[11]+ str(end_tims_s[round].tm_mon) +', '
                name_inp_times[12] = name_inp_times[12]+ str(end_tims_s[round].tm_mday) +', '
                name_inp_times[13] = name_inp_times[13] + str(end_tims_s[round].tm_hour) + ', '
                name_inp_times[14] = name_inp_times[14]+' 00, '
                name_inp_times[15] = name_inp_times[15]+' 00, '
                name_wps_times[0] = name_wps_times[0] + time.strftime('\'%Y-%m-%d_%H:00:00\'', start_tims_s[round]) + ', '
                name_wps_times[1] = name_wps_times[1] + time.strftime('\'%Y-%m-%d_%H:00:00\'', end_tims_s[round]) + ', '
                
                
                
            with open("namelist.input", "r") as f:
                lines_input = f.readlines()

            with open("namelist.input", "w") as f:
                for line in range(0,len(lines_input)):
                    if (line>=(BEGIN_INPUT_LINES-1) and line <=(END_INPUT_LINE-1) ):
                        f.write(name_inp_times[line - (BEGIN_INPUT_LINES-1)] + '\n')
                    else:
                        f.write(lines_input[line])


            with open("namelist.wps", "r") as f:
                lines_wps = f.readlines()

            with open("namelist.wps", "w") as f:
                for line in range(0,len(lines_wps)):
                    if (line>=(BEGIN_WPS_LINES-1) and line <=(END_WPS_LINE-1) ):
                        f.write(name_wps_times[line - (BEGIN_WPS_LINES-1)] + '\n')
                    else:
                        f.write(lines_wps[line])
        else:
            print('****ERROR files namelist.input and/or namelist.wps not found, main.py****')
            exit() 
    except Exception as e: 
        print(e)
        print('****ERROR editing dates on namelist files, main.py****')
        exit() 


    
     
    #########################################################################    
    ##################   RUN GEOGRID    
    #########################################################################
    try:
        succes=False
        Path('OUT/LOG/round'+str(round)+'/').mkdir(parents=True, exist_ok=True)
        print('****Running geogrid.exe****')
        os.system('geogrid.exe > OUT/LOG/round'+str(round)+'/'+'geogrid.out') 
        with open('OUT/LOG/round'+str(round)+'/'+'geogrid.out') as origin_file:
            for line in origin_file:
                if re.search(r'Successful completion of ', line) is not None:
                    print('****SUCCESFUL geogrid.exe****')
                    succes=True
            if(succes==False):
                print('****ERROR geogrid.exe on round '+str(round)+', jumping to next round, look LOG ****')
        os.system('cp geogrid.log OUT/LOG/round'+str(round)+'/')
        os.system('rm geogrid.log ')
    except Exception as e: 
        print(e)
        print('****ERROR geogrid.exe, main.py, look LOG****')
        os.system('cp geogrid.log OUT/LOG/round'+str(round)+'/')
        exit()

   

    #########################################################################
    ##################   RUN UNGRIB    
    #########################################################################
    try:
        if(succes==True):
            succes=False
            print('****Running ungrib.exe****')
            os.system('link_grib.csh datagfs/') 
            os.system('ungrib.exe > OUT/LOG/round'+str(round)+'/'+'ungrib.out')
            with open('OUT/LOG/round'+str(round)+'/'+'ungrib.out') as origin_file:
                for line in origin_file:
                    if re.search(r'Successful completion of ', line) is not None:
                        print('****SUCCESFUL ungrib.exe****')
                        succes=True
            if(succes==False):
                print('****ERROR ungrib.exe on round '+str(round)+', jumping to next round, look LOG ****')
            os.system('cp ungrib.log OUT/LOG/round'+str(round)+'/')
            os.system('rm ungrib.log ')
            
        #needs to be a VTable.GFS link in directory
    except Exception as e: 
        print(e)
        print('****ERROR ungrib.exe, main.py, look LOG****')
        os.system('cp ungrib.log OUT/LOG/round'+str(round)+'/')
        exit()

    

    #########################################################################
    ##################   RUN METAGRID    
    #########################################################################
    try:
        
        if(succes==True):
            succes=False
            print('****Running metgrid.exe****')
            os.system('metgrid.exe > OUT/LOG/round'+str(round)+'/'+'metgrid.out') 
            with open('OUT/LOG/round'+str(round)+'/'+'metgrid.out') as origin_file:
                for line in origin_file:
                    if re.search(r'Successful completion of ', line) is not None:
                        print('****SUCCESFUL metgrid.exe****')
                        succes=True
            if(succes==False):
                print('****ERROR metgrid.exe on round '+str(round)+', jumping to next round, look LOG ****')
            os.system('cp metgrid.log OUT/LOG/round'+str(round)+'/')
            os.system('rm metgrid.log ')
    except Exception as e: 
        print(e)
        print('****ERROR metgrid.exe, main.py, look LOG****')
        os.system('cp metgrid.log OUT/LOG/round'+str(round)+'/')
        exit()

    

    #########################################################################
    ##################   RUN REAL    
    #########################################################################
    try:
        if(succes==True):
            succes=False
            print('****Running real.exe****')
            os.system('mpirun -np 1 real.exe')
            with open('rsl.out.0000') as origin_file:
                for line in origin_file:
                    if re.search(r'SUCCESS COMPLETE ', line) is not None:
                        print('****SUCCESFUL real.exe****')
                        succes=True
            if(succes==False):
                print('****ERROR real.exe on round '+str(round)+', jumping to next round, look LOG ****')           
            os.system('cp rsl.* OUT/LOG/round'+str(round)+'/')
            os.system('rm rsl* ')
    except Exception as e: 
        print(e)
        print('****ERROR real.exe, main.py, look LOG****')
        os.system('cp rsl.* OUT/LOG/round'+str(round)+'/')
        exit()

    
    #########################################################################
    ##################   RUN WRF  
    #########################################################################  
    try:
        if(succes==True):
            succes=False
            print('****Running wrf.exe****')
            cmd = 'mpirun -np ' + str(NUM_CPUS_WRF) + ' wrf.exe'
            os.system(cmd)
            with open('rsl.out.0000') as origin_file:
                for line in origin_file:
                    if re.search(r'SUCCESS COMPLETE ', line) is not None:
                        print('****SUCCESFUL wrf.exe****')
                        succes=True
            if(succes==False):
                print('****ERROR wrf.exe on round '+str(round)+', jumping to next round, look LOG ****')               
            os.system('cp rsl.* OUT/LOG/round'+str(round)+'/')
            os.system('rm rsl* ')
    except Exception as e: 
        print(e)
        print('****ERROR wrf.exe call, main.py, look LOG****')
        os.system('cp rsl.* OUT/LOG/round'+str(round)+'/')
        exit()

    
    #if (TESTING==True):
        #os.system('cp met_em* LOG/round'+str(round)+'/')
        #os.system('cp UNGRIB* LOG/round'+str(round)+'/')
        #os.system('cp geo_em* LOG/round'+str(round)+'/')
        #os.system('cp GRIBFILE.* LOG/round'+str(round)+'/')
    
    
    os.system('cp wrf* OUT/data/')
    os.system('rm -f wrf* ')
    os.system('rm -f UNGRIB*')
    os.system('rm -f met_em* ')
    os.system('rm -f geo_em* ')
    os.system('rm -f rsl* ')
    os.system('rm -f GRIBFILE.* ')

    #########################################################################
    ##################   PLOTS
    #########################################################################

    try:
        if(succes==True):
            print('****Making postprocessing ****')
            
            for i in range(0,DOMAINS):  
                                     
                for j in range(0,run_h[round] +1):
                    try:                    
                        plot_time = start_tims_s[round] 
                        plot_time_sec = calendar.timegm(plot_time)
                        plot_time_sec = plot_time_sec + (j*3600)
                        plot_time_sec_local = plot_time_sec + (HH_ZONE*3600)
                        plot_time = time.gmtime(plot_time_sec)#UTC time
                        plot_time_local = time.gmtime(plot_time_sec_local)#Local time
                        
                        dom=str('{0:02}'.format(i+1))
                        plotfile='OUT/data/wrfout_d' + str('{0:02}'.format(i+1)) + time.strftime('_%Y-%m-%d_%H:00:00', plot_time) 
                        datadir='OUT/data/dom' +str('{0:02}'.format(i+1)) +'/'+ time.strftime('%Y%m%d', plot_time)+'/'
                        #datadir='OUT/data/round'+str(round)+'/dom' +str('{0:02}'.format(i+1)) +'/'
                        plotdir='OUT/plot/dom' +str('{0:02}'.format(i+1)) +'/'+ time.strftime('%Y%m%d', plot_time)+'/'
                        valid_time=time.strftime('%d %m %Y - %H ', plot_time_local)+ T_ZONE + time.strftime(' (%H ', plot_time) + 'UTC)'
                        utchh=time.strftime('%H', plot_time)
                        
                        Path(datadir).mkdir(parents=True, exist_ok=True)
                        Path(plotdir).mkdir(parents=True, exist_ok=True)
                        
                        dx,dy=functions.postprocessing(plotfile,datadir,utchh)
                        functions.skewt_processing(valid_time,utchh,plotdir,plotfile,dom)
                        plot.plot_rasp(datadir,utchh,valid_time,dx,dy,plotdir)
                        print('****SUCCESFUL ploting****')
                    except Exception as e: 
                        print(e)
                        print('****ERROR ploting, '+ valid_time+' main.py****')
    except Exception as e: 
        print(e)
        print('****ERROR ploting, '+ time.strftime('_%Y-%m-%d_%H:00:00', plot_time)+' main.py****')
        
        #exit()

    





#########################################################################
##################   CLEAN AT ENDING
#########################################################################
os.system('rm -f UNGRIB*')
os.system('rm -f *.log')
os.system('rm -f met_em* ')
os.system('rm -f geo_em* ')
os.system('rm -f rsl* ')
os.system('rm -f GRIBFILE.* ')
if (TESTING==False):
    os.system('rm -f datagfs/*')
#CLAEN LLISTES?
UTC_time_end = time.gmtime()
UTC_time_sec_end = calendar.timegm(UTC_time_end)
local_time_secs_end = UTC_time_sec_end + (HH_ZONE*3600)
local_time_end = time.gmtime(local_time_secs_end)
print('****RASPURI ENDED, See u next run!****')
print('****Starting time:           ' + time.strftime('%Y-%m-%d %H:%M:%S', local_time) + ' ****')
print('****Processing starting at:  ' + time.strftime('%Y-%m-%d %H:%M:%S', proc_time) + ' ****')
print('****Ending time:             ' + time.strftime('%Y-%m-%d %H:%M:%S', local_time_end) + ' ****')
































