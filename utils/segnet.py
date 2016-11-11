import numpy as np
import matplotlib.pyplot as plt
import os.path
import scipy
import math
import cv2
import sys
import tempfile

def get_segmented_image(image_path):

  # Setup Caffe SegNet, change accordingly to installation path
  sys.path.append('/usr/local/lib/python2.7/site-packages')
  caffe_root = '/home/drueda/caffe-segnet/'
  sys.path.insert(0, caffe_root + 'python')
  import caffe

  model = 'static/nn_files/segnet_model_driving_webdemo.prototxt'
  weights = 'static/nn_files/segnet_weights_driving_webdemo.caffemodel'
  colours = 'static/nn_files/camvid12.png'

  net = caffe.Net(model,weights, caffe.TEST)
  caffe.set_mode_gpu()

  input_shape = net.blobs['data'].data.shape
  output_shape = net.blobs['argmax'].data.shape

  label_colours = cv2.imread(colours).astype(np.uint8)

  image_tmp = cv2.imread(image_path)
  print image_tmp.shape
  input_image = image_tmp.transpose((2,0,1))
  input_image = np.asarray([input_image])

  out = net.forward_all(data=input_image)

  segmentation_ind = np.squeeze(net.blobs['argmax'].data)
  segmentation_ind_3ch = np.resize(segmentation_ind, (3, input_shape[3], input_shape[2]))
  segmentation_ind_3ch = segmentation_ind_3ch.transpose(1,2,0).astype(np.uint8)
  segmentation_rgb = np.zeros(segmentation_ind_3ch.shape, dtype=np.uint8)

  cv2.LUT(segmentation_ind_3ch, label_colours, segmentation_rgb)
  segmentation_rgb = segmentation_rgb.astype(float)/255


  name = next(tempfile._get_candidate_names())
  path = 'static/segmented/%s.jpg' % (name)
  cv2.imwrite(path, segmentation_rgb)

  return path



