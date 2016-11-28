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

@app.route('/process_location', methods=['GET', 'POST'])
def process_location():
  pano_id = request.json['pano_id']
  pano_path = ga.get_raw_panorama(pano_id)

  normal_path = sg.get_normal_image(pano_path)
  segment_path = sg.get_segmented_image(normal_path)
  cropped_path = sg.get_cropped_image(normal_path, segment_path)

  gd.set_elevation_lines(normal_path)
  gd.set_elevation_lines(cropped_path)

  data = gd.generate_random_data(normal_path)

  planet_normal = pl.get_planet_image(normal_path)
  planet_cropped = pl.get_planet_image(cropped_path)


  gd.set_points(planet_normal, data)
  gd.set_points(planet_cropped, data)


  gd.set_directions(planet_normal)
  gd.set_directions(planet_cropped)


  output = {}
  output['panorama'] = normal_path
  output['segmented'] = segment_path
  output['cropped'] = cropped_path
  output['planet_normal'] = planet_normal
  output['planet_cropped'] = planet_cropped

  return jsonify(**output)

if __name__ == "__main__":
    app.run()
