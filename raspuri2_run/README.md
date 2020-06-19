# RUN Image


This image is the one we run to make the predictions. The Dockerfile will load the previous image with the code and will add the files of this directory which contain setings of the processing.

## Build the container

To build the container is as simple as:

    sudo docker build -t raspuri .
    
To do so we will need the previous imgage that can be build or it will be directly downloaded from DockerHub. Also the following files:

### namelist.input and namelist.wps

These files are required for the WRF. In these case are found inside Cat/, there is an image of the regions defined in this files.
These contain the information of the domain we want to forecast and several conditions. These files are not easy to define.

The only parameter that will be overwritten are the times and dates to process.

[WRF Domain Wizard](https://esrl.noaa.gov/gsd/wrfportal/DomainWizard.html) tool can help creating these files. (Do all the process to define the domain, in the last step you will have already created these files. No need to do the processing or having anything else installed, it will ask for the WRF folder, put an empty one).

These two files need to be copied to $BASEDIR/region/, change the Dockerfile if you change the folder Cat/

### raspuri-cron

Is the cron job that will be set for the processing.

We have new data from GFS at 00, 06, 12 and 18 UTC. But it usually is uploaded 3:40h latter. So if we want to process for each data release is wise to put our job at 03:50, 09:50, 15:50 and 21:50 UTC. Otherwise the program will be checking for 3h if the files are there. 

As you can see in the example raspuri-cron we have set a first line to print the time in de cron.log

    49 15 * * *  date >> /root/RASPURI/region/OUT/cron.log 2>&1

And then we have the call to the scrip launching the raspuri

    50 15 * * *  bash /root/RASPURI/bin/raspuriRUN 12 >> /root/RASPURI/region/OUT/cron.log 2>&1

The call to the raspuriRUN script needs an argument (00, 06, 12 and 18) refering to the GFS release of data to which we want to process. In these way we can set out processing anytime latter.


### variables.py

This file is to define the configuration of the raspuri python script. Some important parameters here are the times we want to compute. As the python script will overwrite the dates in namelist.input and namelist.wps with the correct ones for each run of the WRF. Also to plot the output in layers for a map or as an image.

You can look at the file for more detail.

## Run the container

The container will be using 2 volumes in the host memory.

One with the [mandatory data](https://drive.google.com/file/d/16MP99bnZVO9jsD-ybPy8_RFMs5S3QMyT/view?usp=sharing) for the WRF. And anotherone for the outputs. So we will have to create 2 directories in our host, the one with the data and the other one empty.

We can run the container as: 

    sudo docker run --rm --name raspuri_container -d -v path_to/data/geog:/root/RASPURI/geog -v path_to/OUT:/root/RASPURI/region/OUT raspuri

Substitute the path_to with the path in the host.

## Output directory structure

In construction ...
