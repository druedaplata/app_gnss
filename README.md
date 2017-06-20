# APP GNSS

## Installation Instructions

0. Clone this repository *git clone https://github.com/druedaplata/app_gnss.git*

1. Install opencv using **sudo apt-get install libopencv-dev python-opencv python-tk**

2. Follow the instructions to install [SegNet](https://github.com/alexgkendall/caffe-segnet)
    * Change variable **caffe_root** in file **utils/segnet.py** to your caffe-segnet installation path.

3. Download the necessary model weights from [here](http://mi.eng.cam.ac.uk/%7Eagk34/resources/SegNet/segnet_weights_driving_webdemo.caffemodel) using "Save Link as"

4. Save the file in **static/nn_files/**

5. Install the requirements **sudo pip install -r requirements.txt**

6. Run the Flask application with **python main.py**

7. Open the application at *localhost:5000*

## Run as Docker Container

0. Clone this repository *git clone https://github.com/druedaplata/app_gnss.git*

1. Install [Docker](https://docs.docker.com/engine/installation/)

2. Build the container **docker build -t youruser/app_gnss /path/to/Dockerfile**. This may take a while.

3. Run the container with **docker run -t -i -p 5000:5000 youruser/app_gnss python main.py**

4. Open the application at **localhost:5000**

## How it works? - 23/01/2017

1. We start by clicking in any Street, and click on Search. 
![gmaps_api](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/gmaps_api.jpg)

2. We create an equirectangular image showing a 360° view of the location from Google Maps Api, we do this by stitching several tiles obtained from Google Street View Api.
![raw_panorama](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/panorama.jpg)

3. From the equirectangular image, we use SegNet to segment the image.
![segment](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/segmented.jpg)

4. We use a Stereographic projection in the equirectangular panorama image, to display the entire sky in the center region.
   And generate random (elevation, azimut) pairs of data and correctly display them in the image.
![stereo_images](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/stereo.jpg)

5. Using a mask for the sky in the segmented image, we create a stereographic projection that show only the visible sky at the location. Images are rotated in order to have North always on top.
![segmented_stereo](https://raw.githubusercontent.com/sandiego206/app_gnss/master/static/images/readme_images/segmented_stereo.jpg)

## To Do:
1. Inform the user when there is no StreetView data available for a location.
2. Use real satellite data and draw them correctly in the images.

