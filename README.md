# APP GNSS

## Installation Instructions

1. Install opencv using **sudo apt-get install libopencv-dev python-opencv python-tk**

2. Follow the instructions to install [SegNet](https://github.com/alexgkendall/caffe-segnet)
    * Change variable **caffe_root** in file **utils/segnet.py** to your caffe-segnet installation path.

3. Download the necessary model weights from [here](http://mi.eng.cam.ac.uk/%7Eagk34/resources/SegNet/segnet_weights_driving_webdemo.caffemodel) using "Save Link as"

4. Save the file in **static/nn_files/**

5. Install the requirements **sudo pip install -r requirements.txt**

6. Run the Flask application with **python main.py**


## How it works? - 01/12/2016

1. We start by using a location from Google Maps Api.
![gmaps_api](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/gmaps_api.jpg)

2. We create an equirectangular image showing a 360° view of the location from Google Maps Api, we do this by stitching several tiles obtained from Street View Api.
![raw_panorama](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/pano.jpg)

3. From the equirectangular image, we use SegNet to segment the image.
![segment](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/segmented.jpg)

4. We extract the sky from the previous image using a mask for the color gray, and draw elevation and cardinal lines.
   The north must be set manually (at the moment)
![sky_extract](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/sky_extract.jpg)

5. We now use a stereographic projection in the equirectangular panorama image, to display the enitre sky in the center region.
   And we (at the moment) generate random (elevation, azimut) pairs of data and correctly display them in the image.
![stereo_images](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/stereo_images.jpg)


## To Do:

1. Correctly get the North in each position, and automatically draw in the image.
2. Find a way to draw the elevation lines accurately according to the stereographic projection.
3. Be able to create a route in Google Maps Api and generate a video with the final result.


