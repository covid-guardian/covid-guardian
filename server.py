import os

import yaml
from flask import Flask, request
from werkzeug.utils import secure_filename

from analyser import Analyser

app = Flask('COVIDGuardian')

DEBUG = True


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload():
    with open(os.path.join(os.path.dirname(__file__), "assets" + os.path.sep + 'config.yaml'), 'r') as file:
        result: {} = yaml.load(file, Loader=yaml.FullLoader)

    sdk_path = result['sdk']
    if sdk_path is None or sdk_path == "":
        return 'Please fill in the proper absolute path of Android SDK in assets/config.yaml'

    work_dir = os.path.join(os.path.dirname(__file__), 'upload')
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)
    file = request.files['file']
    file_path = work_dir + secure_filename(file.filename)
    file.save(file_path)

    Analyser.start(file_path, sdk_path)
    return 'ok'


@app.route('/get/<file_name>', methods=['GET'])
def get_report(file_name=None):
    if file_name is None:
        return 'empty file name'
    pass
