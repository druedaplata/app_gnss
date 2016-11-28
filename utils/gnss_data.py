import random
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont


def transform_polar_to_input(r, theta, w, h):
  # Set X from 0 to 500
  print "r, theta: %f --- %f" % (r, theta)
  r = 90 - r
  theta = (-1.0*theta) + 90
  print r,theta
  print
  x = r*math.cos(math.radians(theta))
  y = r*math.sin(math.radians(theta))
  print "r, theta: %f --- %f" % (r, theta)

  print "x, y: %f --- %f" % (x,y)

  xs = ((x/90.0)*500)
  ys = ((y/90.0)*500)
  xs = 540 + xs
  ys = abs(ys - 540)

  print "xs, ys: %f --- %f" % (xs,ys)
  return xs, ys



def generate_random_data(img_path):
  """
  Gets an image path, and randomly generate coordinate points
  for the satellites.
  """
  img = Image.open(img_path)
  w,h = img.size

  # Azimuth
  az = range(0,360)
  # Elevation
  el = range(0,90)

  # Return 3 pairs of el,az
  az_el_pairs = [ (random.choice(az), random.choice(el)) for i in range(10) ]

  #az_el_pairs = [(45,45)]

  data = []

  for (az, el) in az_el_pairs:
    print el, az
    x,y = transform_polar_to_input(el, az, w ,h)
    print x,y
    data.append((x,y))
  return data


def set_points(img_path, data):
  """
  Gets an image path and sets data points

    Attributes:
      img_path: String
      data: list of pairs x,y
  """
  img = Image.open(img_path)
  draw = ImageDraw.Draw(img)
  for (x,y) in data:
    draw.ellipse((x-5, y-5, x+5, y+5), fill=128)

  img.save(img_path)


def set_elevation_lines(img_path):
  """
  Gets an image path and sets elevation lines in it.
  Assuming the horizon is 2/3 down the image.

    Attributes:
      img_path: String
  """
  img = Image.open(img_path)
  w,h = img.size

  bot = 2*h/3

  # Draw horizontal lines
  step = 0
  for i in range(10):
    draw = ImageDraw.Draw(img)
    draw.line((0, step, w, step), fill=128)
    step += bot/9

  # Draw vertical lines
  draw.line((0, 0, 0, h), fill=128)
  draw.line((w/4, 0, w/4, h), fill=128)
  draw.line((2*w/4, 0, 2*w/4, h), fill=128)
  draw.line((3*w/4, 0, 3*w/4, h), fill=128)

  img.save(img_path)


def set_directions(img_path):
  """
  Gets an image path, and sets directions NWSE,
  using arbitrary positions assuming north is always in the center.

  Attributes:
    img_path: String

  """
  img = Image.open(img_path)
  w,h = img.size

  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("utils/font.ttf", 25)
  draw.text((w/2, 10), "N", (255,0,0), font=font)
  draw.text((w/2, h-30), "S", (255,0,0), font=font)
  draw.text((10, h/2), "W", (255,0,0), font=font)
  draw.text((w-30, h/2), "E", (255,0,0), font=font)

  img.save(img_path)

