import argparse
import concurrent
import multiprocessing
import os
import subprocess
from itertools import repeat

import yaml

from analyser import Analyser


def main():
    parser = argparse.ArgumentParser(
        description="COVIDGuardian: Multi-thread App Privacy Analysis System for Covid apps")
    parser.add_argument('path', metavar='APK_or_directory', type=str,
                        help='Path to the APK file or a directory containing APK files')
    parser.add_argument('-n', metavar='parallel_number', type=str,
                        help='The number of parallel works, default is the number of CPU cores', default=0)

    args = parser.parse_args()
    path = args.path
    number = args.n
    if number == 0:
        number = multiprocessing.cpu_count()

    # detect java (for flowdroid)
    process = subprocess.Popen(['java', '--version'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, stderr = process.communicate()

    if len(stderr) > 0:
        print("Java environment is not detected.")
        print("Please add Java into system Path")
        exit(1)

    file_list: [str] = []

    if os.path.isdir(path):
        for subdir, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith(".apk"):
                    file_list.append(subdir + os.sep + filename)
    elif os.path.isfile(path):
        file_list.append(path)
    else:
        print('file path error')
        exit(1)

    with open(os.path.join(os.path.dirname(__file__), "assets" + os.path.sep + 'config.yaml'), 'r') as file:
        result: {} = yaml.load(file, Loader=yaml.FullLoader)

    sdk_path = result['sdk']
    if sdk_path is None or sdk_path == "":
        print('Please fill in the proper absolute path of Android SDK in assets/config.yaml')
        exit(1)

    folder = os.path.join(os.path.dirname(__file__), "results" + os.path.sep + "flowdroid")
    if not os.path.exists(folder) or not os.path.isdir(folder):
        os.makedirs(folder, 0o777, True)

    with multiprocessing.Pool(processes=number) as pool:
        pool.starmap(run, zip(file_list, repeat(sdk_path)))


def run(path, sdk):
    Analyser.start(path, sdk)


if __name__ == '__main__':
    main()
