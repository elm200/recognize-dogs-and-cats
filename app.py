import time
import os
import random
from flask import Flask, render_template, request
from glob import glob
from pprint import pprint
import json

from lib import nn

app = Flask(__name__)
predictor = None

@app.route('/')
def index():
    return render_template('index.html', items=predictor.get_sample_items())

@app.route('/upload', methods=['POST'])
def upload():
    upfile = request.files["upfile"]
    img_file = "image" + str(random.randint(0, 999999)) + os.path.splitext(upfile.filename)[1]
    img_path = os.path.join("./tmp/", img_file)
    upfile.save(img_path)
    item = predictor.get_image_item(img_path)
    os.remove(img_path)
    return json.dumps(item)

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10MiB
    predictor = nn.Predictor()
    app.run()
