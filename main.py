from __future__ import division
from flask import Flask, render_template, request, jsonify
import utils.google_access as ga
import utils.segnet as sg
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process_location', methods=['GET', 'POST'])
def process_location():
  pano_id = request.json['pano_id']
  pano_path = ga.get_raw_panorama(pano_id)
  segment_path = sg.get_segmented_image(pano_path)

  output = {}
  output['raw_panorama'] = pano_path
  output['segmented'] = segment_path

  return jsonify(**output)

if __name__ == "__main__":
    app.run()
