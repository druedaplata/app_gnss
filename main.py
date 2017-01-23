from __future__ import division
from flask import Flask, render_template, request, jsonify
import utils.google_access as ga
import utils.segnet as sg
import utils.planet as pl
import utils.gnss_data as gd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/download_tiles', methods=['POST'])
def download_tiles():
  pano_id = request.json['pano_id']
  pano_path = ga.get_raw_panorama(pano_id)

  output = {'panorama': pano_path}
  return jsonify(**output)


@app.route('/segment_image', methods=['POST'])
def segment_image():
  pano_path = request.json['pano_path']
  north_heading = request.json['north_heading']

  normal_path = sg.get_normal_image(pano_path)
  segment_path = sg.get_segmented_image(normal_path)
  cropped_path = sg.get_cropped_image(normal_path, segment_path)

  # get the north pixel in the image, according to center heading
  north_w_point = gd.get_north_w_point_from_heading(normal_path, north_heading)

  # add cardinal lines
  gd.set_elevation_lines(normal_path, north_w_point)
  gd.set_elevation_lines(cropped_path, north_w_point)

  output = {'normal':  normal_path, 'segmented': segment_path, 'cropped': cropped_path, 'north': north_w_point}

  return jsonify(**output)


@app.route('/get_stereo_projections', methods=['POST'])
def get_stereo_projections():
  nort_w_point = request.json['north']
  normal_path = request.json['normal']
  cropped_path = request.json['cropped']

  data = gd.generate_random_data(normal_path, nort_w_point)

  planet_normal = pl.get_planet_image(normal_path)
  planet_cropped = pl.get_planet_image(cropped_path)

  gd.set_points(planet_normal, data)
  gd.set_points(planet_cropped, data)

  gd.rotate_and_set_directions(planet_normal, nort_w_point)
  gd.rotate_and_set_directions(planet_cropped, nort_w_point)

  output = {'planet_normal': planet_normal, 'planet_cropped': planet_cropped}

  return jsonify(**output)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
