import re
import glob
from PIL import Image
import tempfile
import subprocess



def atoi(text):
  return int(text) if text.isdigit() else text

def natural_keys(text):
  """
  alist.sort(key=natural_keys) sorts in human order [1,10,2] becomes [1,2,10]
  """
  return [ atoi(c) for c in re.split('(\d+)', text) ]



def get_raw_panorama(pano_id):

  """ Gets a pano_id from streetview javascript api,
      uses it to download all image tiles for this location
      and joins them to create a panorama image of 3600x1600 pixels aprox.
      Returns a path to this image.
  """

  # 1. Download all images using a curl subprocess
  url = "http://cbk0.google.com/cbk?output=tile&panoid=%s&zoom=3&x=[0-6]&y=[0-2]" % (pano_id)
  command = "-o"
  name = "static/images/tiles/tile_#1_#2.jpg"
  cmd = ["curl", url, command, name]

  subprocess.call(cmd)

  # 2. Read the images back from file
  image_paths = list(map(str.strip, glob.glob('static/images/tiles/*.jpg')))
  image_paths.sort(key=natural_keys)

  # 3. Open all the images, and get the total width and height
  images_data = map(Image.open, image_paths)
  widths, heights = zip(*(i.size for i in images_data))

  total_w = sum(widths[0:7])
  total_h = sum(heights[0:3])

  # 4. Create a new image with the total width and height
  panorama = Image.new('RGB', (total_w, total_h))

  # 5. Join all image tiles in a new single panorama image
  x_off = 0
  y_off = 0
  for im in images_data:
    panorama.paste(im, (x_off, y_off))
    y_off += im.size[0]
    if y_off == 3*im.size[0]:
      y_off = 0
      x_off += im.size[0]

  # 6. Save the new panorama image
  # 6.1 We crop the width of the panorama image by hand, to have a 360 degrees view without repetition.
  name = next(tempfile._get_candidate_names())
  w,h = panorama.size
  pano_path = "static/images/panorama/%s.png" % (name)

  panorama.crop((0,0, 2.15*h, h)).save(pano_path)

  return pano_path


