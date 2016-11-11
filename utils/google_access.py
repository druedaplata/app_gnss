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

  url = "http://cbk0.google.com/cbk?output=tile&panoid=%s&zoom=3&x=[0-6]&y=[0-2]" % (pano_id)
  command = "-o"
  name = "static/tiles/tile_#1_#2.jpg"
  cmd = ["curl", url, command, name]

  subprocess.call(cmd)

  image_paths = list(map(str.strip, glob.glob('static/tiles/*.jpg')))
  image_paths.sort(key=natural_keys)

  images_data = map(Image.open, image_paths)
  widths, heights = zip(*(i.size for i in images_data))

  total_w = sum(widths[0:7])
  total_h = sum(heights[0:3])

  panorama = Image.new('RGB', (total_w, total_h))

  x_off = 0
  y_off = 0
  for im in images_data:
    panorama.paste(im, (x_off, y_off))
    y_off += im.size[0]
    if y_off == 3*im.size[0]:
      y_off = 0
      x_off += im.size[0]

  name = next(tempfile._get_candidate_names())
  w,h = panorama.size
  panorama.crop((0,0, 2.15*h, h)).save("static/panorama/%s.png" % (name))

  print "Raw panorama image has been saved in [static/panorama/%s.png]" % (name)
  return "static/panorama/%s.png" % (name)


