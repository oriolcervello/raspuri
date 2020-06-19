# WRF Image

Here the image with the Dockerfile and the dependencies will be created. Hopefully, only to rebuild it when with major updates in the dependencies. 

To build it:

    sudo docker build -t oriolcervello/raspuri:image .

This will create an image with all the dependencies and download the WRF and WPS code, unfortunately it can not be compiled from the Dockerfile, so we will enter the container:

    sudo docker run -it oriolcervello/raspuri:image bash

And compile the WRF and WPS: (you can see in configRASPURI.sh that there are the paths of some dependencies, if they are updated to newer versions 1.12 ->1.13 the path needs to be changed):

    bash configRASPURI.sh

Once finished we can exit the container, and create an image form it

    sudo docker container ls --all
    sudo docker commit -m "raspuri" IDcontainer oriolcervello/raspuri:wrf
