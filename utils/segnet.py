from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os.path
import scipy
import math
import cv2
import sys
import image_slicer
from resizeimage import resizeimage
import tempfile


def join_images_horizontally(images):
  """ Receives two images in a list, in numpy array format
      and joins them horizontally

      Attributes:
        images: numpy array list
  """
  return np.concatenate((images[0], images[1]), axis=1)



def slice_and_resize(img_path):
  """ Receives a panorama picture of 3600x1600 pixels aprox,
      slice the image in two parts horizontally,
      and resize each part to 480x360

      Attributes:
        img_path: String panorama path
  """
  # read image
  img = Image.open(img_path)
  width, height = img.size

  #slice image in 2 parts horizontally, not looping
  image_parts = []
  step = width/2

  image_parts.append(img.crop((0, 0, step, height)))
  image_parts.append(img.crop((step, 0, step*2, height)))

  # resize images
  resized_images = [ resizeimage.resize_cover(img, [480,360]) for img in image_parts ]

  # Convert PIL Image to OpenCV image
  images = [ cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in resized_images ]

  return images


def get_masked_image(normal_image, segmented_image):

  """ Gets a normal image and a segmented image,
      and uses the segmented sky (gray) from segmented image
      to crop from the normal image. Save it and return the path.

      Attributes:
        normal_image: numpy array
        segmented_image: numpy array
  """
  color = [128, 128, 128]
  # create boundaries, same color but needs two arguments later on
  lower = np.array(color, dtype="uint8")
  upper = np.array(color, dtype="uint8")

  # find the colors within the boundaries and apply the mask
  mask = cv2.inRange(segmented_image, lower, upper)
  output = cv2.bitwise_and(normal_image, normal_image, mask = mask)

  name = next(tempfile._get_candidate_names())
  path = "static/images/cropped/%s.png" % (name)
  cv2.imwrite(path, output)
  return path


def get_normal_segmented_and_cropped_image(image_path):

  """ Gets a path for a panorama image of 3600x1600 pixels,
      resize the image to two 480x360 images,
      uses caffe segnet to segment them,
      and crop the sky from the normal image.

      Attributes:
        image_path: string panorama path
  """

  # 1. Resize the panorama image in two 480x360 images
  resized_images = slice_and_resize(image_path)

  # 2. Join the images in a full normal panorama image and save it
  normal_full_img = join_images_horizontally(resized_images)
  name = next(tempfile._get_candidate_names())
  normal_path = "static/images/panorama/%s_resized.png" % (name)
  cv2.imwrite(normal_path, normal_full_img)

  # 3. Setup caffe Segnet, change accordingly to installation path
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

  # 4. Use Segnet to segment each image separately

  def segment_image(image):
    input_image = image.transpose((2,0,1))
    input_image = image.transpose((2,0,1))
    input_image = np.asarray([input_image])

    out = net.forward_all(data=input_image)

    segmentation_ind = np.squeeze(net.blobs['argmax'].data)
    segmentation_ind_3ch = np.resize(segmentation_ind, (3, input_shape[2], input_shape[3]))
    segmentation_ind_3ch = segmentation_ind_3ch.transpose(1,2,0).astype(np.uint8)
    segmentation_rgb = np.zeros(segmentation_ind_3ch.shape, dtype=np.uint8)

    cv2.LUT(segmentation_ind_3ch, label_colours, segmentation_rgb)

    return segmentation_rgb

  segmented_images = map(segment_image, resized_images)

  # 5. Create a single full image from the segmented parts
  segmented_full_image = join_images_horizontally(segmented_images)
  name = next(tempfile._get_candidate_names())
  segment_path = "static/images/segmented/%s_resized.png" % (name)
  cv2.imwrite(segment_path, segmented_full_image)

  """
  Commented out, code to include trees in top half

  # 5.a Change top half of trees into sky color
  height, width, c = segmented_full_image.shape

  # OpenCV works in BGR format
  for x in range(width):
    for y in range(height/2):
      if segmented_full_image[y,x].tolist() == [0, 128, 128]:
        segmented_full_image[y,x] = [128, 128, 128]

  cv2.imwrite('tmp.png', segmented_full_image)
  """

  # 6. Crop the sky from the segmented image, color #808080 or 128,128,128
  cropped_path = get_masked_image(normal_full_img, segmented_full_image)


  return normal_path, segment_path, cropped_path



