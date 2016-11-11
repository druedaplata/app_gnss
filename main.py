from __future__ import division
from flask import Flask, render_template, request, jsonify
import utils.google_access as ga
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_raw_panorama', methods=['GET', 'POST'])
def get_raw_panorama():
  pano_id = request.json['pano_id']
  pano_path = ga.get_raw_panorama(pano_id)
  return pano_path

if __name__ == "__main__":
    app.run()
