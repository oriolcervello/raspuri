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




