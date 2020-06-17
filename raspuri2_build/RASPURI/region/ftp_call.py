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
# ftp_call.py
# This script is part of RASPURI v2
# Script to download gfs data for the rasp
try:
    import sys
    import os
    import signal
    import time
    from ftplib import FTP
    from variables import SERVER, WAIT_FTP
    sys.stdout = open('OUT/ftppy.log', 'a')
except:
    print('****ERROR importing externals, ftp_call.py****')
    exit()
#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)
foldername = sys.argv[1]
folder_h= sys.argv[2]
file_name = sys.argv[3]

def handler(signum, frame):
   raise Exception("FTP download TimeOut")



while(not os.path.isfile('datagfs/'+file_name)):

    try:
        ftp = FTP(SERVER) #,port)     # connect to host  'anonymous','anonymous'
        ftp.login() 
        #ftp.set_pasv(False)
    except:
        print('****ERROR connecting to FTP server, ftp_call.py****')
        exit()



    try:            
        ftp.cwd( '/pub/data/nccf/com/gfs/prod/')
        ftp_list= []
        ftp_list=ftp.nlst()
        #print(ftp_list)
        if (foldername in ftp_list):
            ftp.cwd(foldername)
             
            ftp_list= []
            ftp_list=ftp.nlst()
            #print(ftp_list)
            if (folder_h in ftp_list):
                ftp.cwd(folder_h)
                      
                ftp_list= []
                ftp_list=ftp.nlst()
                if (file_name in ftp_list):
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(WAIT_FTP*12)
                    try:
                        print('****Downloading: ' + file_name + '****')                    
                        ftp.retrbinary('RETR '+ file_name ,open('datagfs/'+file_name, 'wb').write)
                        ftp.quit()
                        signal.alarm(0)
                    except Exception as e:
                        print(e)
                        ftp.quit()
                        os.system('rm datagfs/'+file_name)
                        continue
                        
                else:
                    ftp.quit()
                    print('****WAITING: ' + file_name + ' not found, wait until retry = ' + str(WAIT_FTP)+'s****')
                    time.sleep(WAIT_FTP)
            else:
                ftp.quit()
                print('****WAITING: ' + file_name + ' not found, wait until retry = ' + str(WAIT_FTP)+'s****')
                time.sleep(WAIT_FTP)
        else:
            ftp.quit()
            print('****WAITING: ' + file_name + ' not found, wait until retry = ' + str(WAIT_FTP)+'s****')
            time.sleep(WAIT_FTP)
            
        
    except Exception as e: 
        print('****Error fetching file: ' + file_name + ' , ftp_call.py****')
        print(e)
        ftp.quit()        
        exit()
                
f = open('downloaded.txt', 'a')
f.write(file_name + '\n')
f.close()

print ('****File: ' + file_name + ' downloaded SUCCESFULY****')




