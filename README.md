# Raspuri v2

RASPURI v2 is a new developed RASP (Regional Atmospheric Soaring Program). The idea came from updating to a 64 bit architecture and WRF to v4 the original [RASPURI](http://raspuri.mooo.com), which is a original [Dr Jack's RASP](http://www.drjack.info/). RASPURI v2 is full coded in Python and Bash, except the [Fortran subroutines](https://github.com/oriolcervello/ncl_jack_fortran-for-Python) developed by Dr. Jack for some of the postprocessings. The whole application runs through Docker. 

Actual predictions can be found in [raspuri.catio.eu](http://raspuri.catio.eu/). In case the server is down, an example of the output predictions and the web page can be find [here](https://oriolcervello.github.io/).


## Repository

The structure of this RASP (and repo) is divided in 3 Docker images.

1. [WRF Image](https://github.com/oriolcervello/raspuri/tree/master/raspuri2_wrf): This image is the base one, in here all the dependencies and the WRF & WPS engines are downloaded and compiled.
2. [Build Image](https://github.com/oriolcervello/raspuri/tree/master/raspuri2_build): This image uses as base layer the previous image. In this step, only a layer with the Raspuri scripts is added. It is done in this way in order that small changes in the code can be done without the need of downloading and compiling everything again.
3. [Run Image](https://github.com/oriolcervello/raspuri/tree/master/raspuri2_run): This image is the final one we will be runing. It will use the Build Image as base and will copy the parameters of the region for the forecast and set the cron task.

Already build images can be found in [DockerHub oriolcervello/raspuri](https://hub.docker.com/repository/docker/oriolcervello/raspuri).

In addition to the images,  [this mandatory data](https://drive.google.com/file/d/16MP99bnZVO9jsD-ybPy8_RFMs5S3QMyT/view?usp=sharing) is necessary in order that the WRF works and for some plots. As it is very heavy is not in the repo. The data for the WRF can be find individualy in [UCAR data](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html) and the images for the plots in [NASA Images](https://visibleearth.nasa.gov/images/73934/topography).

If your interest is just in the forecasting, check the [Run Image](https://github.com/oriolcervello/raspuri/tree/master/raspuri2_run). Otherwise, check also the other two images (directories).

In the [Web](https://github.com/oriolcervello/raspuri/tree/master/web) directroy there is the Dockerfile to create a simple Nginx server and the html and js of the web. It is quite presonalized to the region you are forecasting, but it can be reused changing the labels in the html and some other variables in the js (like the coordinates to position in the map).

## RASP Workflow

In construction...

## Acknowledgements

* [Oriol's RASPURI](http://raspuri.mooo.com)
* [Noel's Meteonube](http://meteonube.hopto.org/)

Rasp:

* [Dr Jack](http://www.drjack.info/), [Fortran subroutines for Python](https://github.com/oriolcervello/ncl_jack_fortran-for-Python)
* [National Center for Atmospheric Research (NCAR)](https://www.mmm.ucar.edu/), [WRF User Page](https://www2.mmm.ucar.edu/wrf/users/), [WRF & WPS (doi:10.5065/1dfh-6p97)](https://opensky.ucar.edu/islandora/object/opensky:2898)
* [Global Forecast System (GFS) data](https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php)
* [Wgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)
* [NASA Images](https://visibleearth.nasa.gov/images/73934/topography)

Web:

* [Free DNS](https://freedns.afraid.org/)
* [w3schools.com](https://www.w3schools.com/)
* [Leaflet](https://leafletjs.com/)

## Credit & License

Oriol Cervelló i Nogués, ( raspuri [at] protonmail.com ).
RASPURI v2. 2019. [github.com/oriolcervello/raspuri](https://github.com/oriolcervello/raspuri)

Find copy of GNU GPLv3.0 in License.txt
