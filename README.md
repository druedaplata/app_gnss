# APP GNSS

## Installation Instructions

1. Install opencv using **sudo apt-get install libopencv-dev python-opencv**

2. Follow the instructions to install [SegNet](https://github.com/alexgkendall/caffe-segnet)

3. Download the necessary model weights from [here](http://mi.eng.cam.ac.uk/%7Eagk34/resources/SegNet/segnet_weights_driving_webdemo.caffemodel)

4. Save the file in **static/nn_files/**

5. Install the requirements **sudo pip install -r requirements.txt**

6. Run the Flask application with **python main.py**


## How it works? - 01/12/2016

1. We start by using a location from Google Maps Api.
![gmaps_api](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/gmaps_api.jpg)

2. We extract a raw panorama image showing a 360° image from Google Maps Api, stitching several tiles from street view.
![raw_panorama](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/pano.jpg)

3. From the raw panorama, we use SegNet to segment the image.
![segment](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/segmented.jpg)

4. We extract the sky from the previous image using a mask for the color gray, and draw elevation and cardinal lines.
   The north must be set manually (at the moment)
![sky_extract]()

5. We now use a stereographic projection in the panorama image, to display the enitre sky in the center region.
   And we (at the moment) generate random (elevation, azimut) pairs of data and correctly display them in the image.
![normal_stereographic]()
![extracted_stereographic]()




