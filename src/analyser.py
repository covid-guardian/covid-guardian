import os

import yaml
from androguard.core.bytecodes import apk
from androguard.misc import AnalyzeAPK, Analysis

from code_analyser import CodeAnalyser
from manifest_analyser import ManifestAnalyser
from root_analyser import RootAnalyser
from taint_analyser import TaintAnalyser
from virus_analyser import VirusAnalyser


class Analyser:

    @staticmethod
    def start(apk_path, sdk_path):
        instance = Analyser()

        instance.__decompile(apk_path)
        instance.__root_detection__()
        instance.__analyse_manifest__()
        instance.__analyse_code__()
        instance.__virus_analysis__(apk_path)
        instance.__dataflow_analysis__(apk_path, sdk_path)
        instance.__generate_results__()

    email_list = []

    def __init__(self):
        pass

    def __del__(self):
        del self.__apk
        del self.__dx
        del self.__df
        del self.__manifest_analyser
        del self.__code_analyser
        del self.__root_analyser
        del self.__virus_analyser
        pass

    def __decompile(self, apk_path):
        print("start analyse")
        a, df, dx = AnalyzeAPK(apk_path)
        self.__apk: apk.APK = a
        self.__df = df
        self.__dx: Analysis = dx


    def __analyse_manifest__(self):
        print("start analysing manifest")
        self.__manifest_analyser = ManifestAnalyser()
        self.__manifest_analyser.analyse(self.__apk)
        pass

    def __analyse_code__(self):
        print("start analysing code")
        self.__code_analyser = CodeAnalyser()
        self.__code_analyser.analyse(self.__apk, self.__dx)
        pass

    def __dataflow_analysis__(self, apk_path, sdk_path):
        print("start analysing dataflow")
        self.__taint_analyser = TaintAnalyser()
        self.__taint_analyser.analyse(self.__apk, self.__df[0], self.__dx, apk_path, sdk_path)
        pass

    def __virus_analysis__(self, apk_path):
        print("start analysing virus")
        self.__virus_analyser = VirusAnalyser()
        self.__virus_analyser.analyse(apk_path)
        pass

    def __root_detection__(self):
        print("start root detection")
        self.__root_analyser = RootAnalyser()
        self.__root_analyser.analyse(self.__apk, self.__dx)
        pass

    def __generate_results__(self):
        print("start generating results")
        result = {
            'app': self.__manifest_analyser.reports(),
            'code_analysis': self.__code_analyser.reports(),
            'root_analysis': self.__root_analyser.reports(),
            'virus_total': self.__virus_analyser.virus_total_result,
            'pii_taint_result': self.__taint_analyser.reports()
        }
        filename = self.__apk.get_filename() + ".yaml"
        filename = filename.split(os.path.sep)[-1]

        folder = os.path.join(os.path.dirname(__file__), "results")
        if not os.path.exists(folder) or not os.path.isdir(folder):
            os.makedirs(folder, 0o777, True)
        with open(os.path.join(folder, filename), 'w') as file:
            yaml.dump(result, file)
        pass
