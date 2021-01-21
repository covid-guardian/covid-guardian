import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

import yaml
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

from analyser import Analyser

app = Flask('COVIDGuardian')
executor = ThreadPoolExecutor(cpu_count())

# load the configuration.
with open(os.path.join(os.path.dirname(__file__), "assets" + os.path.sep + 'config.yaml'), 'r') as file:
    result: {} = yaml.load(file, Loader=yaml.FullLoader)

# check whether Android SDK path is specified.
sdk_path = result['sdk']
if sdk_path is None or sdk_path == "":
    print('Please fill in the proper absolute path of Android SDK in assets/config.yaml')
    exit(1)

# create working directories
work_dir = os.path.join(os.path.dirname(__file__), 'upload' + os.sep)
result_dir = os.path.join(os.path.dirname(__file__), 'results')
if not os.path.isdir(work_dir):
    os.mkdir(work_dir)
if not os.path.isdir(result_dir):
    os.mkdir(result_dir)

init_run = False


# if there are tasks uncompleted, resume previous tasks
def load_old_tasks():
    # load all apk files in the directory 'upload'
    for (dir_path, dir_names, filenames) in os.walk(work_dir):
        for filename in filenames:
            if filename[-3:] == 'apk':
                file_path = dir_path + filename
                executor.submit(analysis, file_path)


# root index page
@app.route('/')
def index():
    # load previous tasks
    global init_run
    if not init_run:
        init_run = True
        load_old_tasks()

    # processing tasks
    processing = []
    for (dir_path, dir_names, filenames) in os.walk(work_dir):
        for filename in filenames:
            if filename[-3:] == 'apk':
                processing.append(filename[:-4])

    # generated reports
    analysis_list = []
    for (dir_path, dir_names, filenames) in os.walk(result_dir):
        for filename in filenames:
            if filename[-4:] == 'yaml':
                analysis_list.append(filename[:-9])

    return render_template('index.html', processing=processing, analysis=analysis_list)


# upload file
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = work_dir + secure_filename(file.filename)
    if os.path.exists(file_path):
        return 'this app is processing'

    # save the app to the directory 'upload'
    file.save(file_path)

    # process the analysis in other process
    executor.submit(analysis, file_path)
    return 'ok'


def analysis(file_path):
    Analyser.start(file_path, sdk_path)
    os.remove(file_path)


# get detail report of an app
@app.route('/get/<file_name>', methods=['GET'])
def get_report(file_name=None):
    if file_name is None:
        return 'empty name'
    path = result_dir + os.sep + file_name + '.apk.yaml'
    if not os.path.exists(path):
        return 'result not ready'

    # load report yaml file
    with open(path, 'r') as file:
        # result: {} = yaml.load(file, Loader=yaml.FullLoader)
        result = file.read()

    flowdroid_path = result_dir + os.sep + 'flowdroid' + os.sep + file_name + '.xml'

    # load taint analysis report from FlowDroid
    if os.path.exists(flowdroid_path):
        with open(flowdroid_path, 'r') as file:
            f_context = file.read()
    else:
        f_context = "None"

    return render_template('detail.html', result=result, flowdroid=f_context, name=file_name + '.apk')
