import json
import os

import requests
import yaml


class VirusAnalyser:

    def __init__(self):
        self.virus_total_result = {}

    def analyse(self, apk_path: str):
        with open(os.path.join(os.path.dirname(__file__), "assets" + os.path.sep + 'virus_total.yaml'), 'r') as file:
            result: {} = yaml.load(file, Loader=yaml.FullLoader)

        # virus total key
        api_key = result['api_key']
        if api_key is None or api_key == "":
            print("Please add api_key of VirusTotal in assets/virus_total.yaml")
            return
        # upload
        with open(apk_path, 'rb') as f:
            x = requests.post("https://www.virustotal.com/vtapi/v2/file/scan", files={'file': f, 'apikey':api_key})
            if x.text == '':
                print("virus total upload:", x)
                return
            result = json.loads(x.text)
            # {
            #  'permalink': 'https://www.virustotal.com/file/d140c...244ef892e5/analysis/1359112395/',
            #  'resource': 'd140c244ef892e59c7f68bd0c6f74bb711032563e2a12fa9dda5b760daecd556',
            #  'response_code': 1,
            #  'scan_id': 'd140c244ef892e59c7f68bd0c6f74bb711032563e2a12fa9dda5b760daecd556-1359112395',
            #  'verbose_msg': 'Scan request successfully queued, come back later for the report',
            #  'sha256': 'd140c244ef892e59c7f68bd0c6f74bb711032563e2a12fa9dda5b760daecd556'
            # }

        # get the report ----- wont receive the report directly
        # resource = result['resource']
        # x = requests.get("https://www.virustotal.com/vtapi/v2/file/report",
        #               params={'resource': resource, 'apikey': api_key})
        # if x.text == '':
        #     print("virus total download report:", x)
        #     return
        # result = json.loads(x.text)
        # print('============w==================')
        # print(result)
        # print('============w==================')
        # {
        #  'response_code': 1,
        #  'verbose_msg': 'Scan finished, scan information embedded in this object',
        #  'resource': '99017f6eebbac24f351415dd410d522d',
        #  'scan_id': '52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c-1273894724',
        #  'md5': '99017f6eebbac24f351415dd410d522d',
        #  'sha1': '4d1740485713a2ab3a4f5822a01f645fe8387f92',
        #  'sha256': '52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c',
        #  'scan_date': '2010-05-15 03:38:44',
        #  'permalink': 'https://www.virustotal.com/file/52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c/analysis/1273894724/',
        #  'positives': 40,
        #  'total': 40,
        #  'scans': {
        #    'nProtect': {
        #      'detected': true,
        #      'version': '2010-05-14.01',
        #      'result': 'Trojan.Generic.3611249',
        #      'update': '20100514'
        #    },
        #    'CAT-QuickHeal': {
        #      'detected': true,
        #      'version': '10.00',
        #      'result': 'Trojan.VB.acgy',
        #      'update': '20100514'
        #    },
        #    'McAfee': {
        #      'detected': true,
        #      'version': '5.400.0.1158',
        #      'result': 'Generic.dx!rkx',
        #      'update': '20100515'
        #    },
        #    'TheHacker': {
        #      'detected': true,
        #      'version': '6.5.2.0.280',
        #      'result': 'Trojan/VB.gen',
        #      'update': '20100514'
        #    },
        #    'VirusBuster': {
        #     'detected': true,
        #      'version': '5.0.27.0',
        #      'result': 'Trojan.VB.JFDE',
        #      'update': '20100514'
        #    }
        #  }
        # }
        self.virus_total_result = result
        pass
