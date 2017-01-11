from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os.path
import os
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
  array = np.concatenate((images[0], images[1]), axis=1)
  return Image.fromarray(np.uint8(array))



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

  return resized_images


def get_normal_image(image_path):
  """
  Gets a panorama image of 3600x1600 pixels aprox.
  and returns a path to a resized 960x360 image.

    Attributes:
      image_path: String
  """
  resized_images = slice_and_resize(image_path)

  normal_full_img = join_images_horizontally(resized_images)

  folder = "static/images/panorama"

  name = next(tempfile._get_candidate_names())
  normal_path = "%s/%s_resized.png" % (folder, name)
  normal_full_img.save(normal_path)

  return normal_path

def get_segmented_image(image_path):
  """
  Gets a panorama image of 960x360 pixels,
  and returns a path to a segmented 960x360 image.

    Attributes:
      image_path: String
  """

  # Setup Caffe Segnet
  sys.path.append('/usr/local/lib/python2.7/site-packages')
  caffe_root = '/opt/caffe-segnet/'
  sys.path.insert(0, caffe_root + 'python')
  import caffe

  model = 'static/nn_files/segnet_model_driving_webdemo.prototxt'
  weights = 'static/nn_files/segnet_weights_driving_webdemo.caffemodel'
  colours = 'static/nn_files/camvid12.png'

  net = caffe.Net(model,weights, caffe.TEST)
  caffe.set_mode_cpu()

  input_shape = net.blobs['data'].data.shape
  output_shape = net.blobs['argmax'].data.shape
  label_colours = cv2.imread(colours).astype(np.uint8)

  resized_images = slice_and_resize(image_path)

  images = [ cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in resized_images ]



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

  segmented_images = map(segment_image, images)

  # 5. Create a single full image from the segmented parts
  segmented_full_image = join_images_horizontally(segmented_images)

  folder = "static/images/segmented"
  os.system("rm %s/*.png" % (folder))

  name = next(tempfile._get_candidate_names())
  segment_path = "%s/%s_resized.png" % (folder, name)
  segmented_full_image.save(segment_path)
  return segment_path


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

  folder = "static/images/cropped"
  os.system("rm %s/*.png" % (folder))

  name = next(tempfile._get_candidate_names())
  path = "%s/%s.png" % (folder, name)
  cv2.imwrite(path, output)
  return path


def get_cropped_image(normal_path, segment_path):

  """ Gets two paths for a normal and a segment image,
      and return a path to a cropped sky image.

      Attributes:
        normal_path: String
        segment_path: String
  """
  normal_img = cv2.imread(normal_path)
  segment_img = cv2.imread(segment_path)

  cropped_path = get_masked_image(normal_img, segment_img)

  return cropped_path



