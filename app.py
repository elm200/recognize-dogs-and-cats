from flask import Flask, render_template, request
import numpy as np
import time
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # pprint(request.files)
    upfile = request.files["upfile"]
    upfile.save("./" + upfile.filename)
    return "<h1>uploaded!</h1>"

if __name__ == '__main__':
    app.debug = True
#    app.run(host='0.0.0.0') # どこからでもアクセス可能に
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10MiB
    app.run()


# app.logger.debug("upfiles = " + str(type(f)))
