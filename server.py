import os
from multiprocessing import get_context, cpu_count
from multiprocessing.context import Process
from xml.etree import ElementTree

import xmltodict
import yaml
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from analyser import Analyser

app = Flask('COVIDGuardian')
executor = ThreadPoolExecutor(cpu_count())

with open(os.path.join(os.path.dirname(__file__), "assets" + os.path.sep + 'config.yaml'), 'r') as file:
    result: {} = yaml.load(file, Loader=yaml.FullLoader)

sdk_path = result['sdk']
if sdk_path is None or sdk_path == "":
    print('Please fill in the proper absolute path of Android SDK in assets/config.yaml')
    exit(1)

work_dir = os.path.join(os.path.dirname(__file__), 'upload' + os.sep)
result_dir = os.path.join(os.path.dirname(__file__), 'results')
if not os.path.isdir(work_dir):
    os.mkdir(work_dir)
if not os.path.isdir(result_dir):
    os.mkdir(result_dir)

init_run = False


def load_old_tasks():
    for (dir_path, dir_names, filenames) in os.walk(work_dir):
        for filename in filenames:
            if filename[-3:] == 'apk':
                file_path = dir_path + filename
                executor.submit(analysis, file_path)


@app.route('/')
def index():
    global init_run
    if not init_run:
        init_run = True
        load_old_tasks()

    processing = []
    for (dir_path, dir_names, filenames) in os.walk(work_dir):
        for filename in filenames:
            if filename[-3:] == 'apk':
                processing.append(filename[:-4])

    analysis_list = []
    for (dir_path, dir_names, filenames) in os.walk(result_dir):
        for filename in filenames:
            if filename[-4:] == 'yaml':
                analysis_list.append(filename[:-5])

    return render_template('index.html', processing=processing, analysis=analysis_list)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = work_dir + secure_filename(file.filename)
    if os.path.exists(file_path):
        return 'this app is processing'
    file.save(file_path)

    executor.submit(analysis, file_path)
    return 'ok'


def analysis(file_path):
    Analyser.start(file_path, sdk_path)
    os.remove(file_path)


@app.route('/get/<file_name>', methods=['GET'])
def get_report(file_name=None):
    if file_name is None:
        return 'empty name'
    path = result_dir + os.sep + file_name + '.yaml'
    if not os.path.exists(path):
        return 'result not ready'

    with open(path, 'r') as file:
        result: {} = yaml.load(file, Loader=yaml.FullLoader)

    flowdroid_path = result_dir + os.sep + 'flowdroid' + os.sep + file_name + '.xml'

    with open(flowdroid_path, 'r') as file:
        f_context = file.read()
        flowdroid = xmltodict.parse(f_context)

    return render_template('detail.html', result=result, flowdroid=flowdroid)
