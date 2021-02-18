# COVIDGuardian
[![DOI](https://zenodo.org/badge/323030673.svg)](https://zenodo.org/badge/latestdoi/323030673)

This is the artifact accompanying the paper "An Empirical Assessment of Global COVID-19 Contact Tracing Applications", accepted by ICSE 2021.

If you would like to use this project in your research, please cite our paper:

```bib
@misc{sun2021empirical,
      title={An Empirical Assessment of Global COVID-19 Contact Tracing Applications}, 
      author={Ruoxi Sun and Wei Wang and Minhui Xue and Gareth Tyson and Seyit Camtepe and Damith C. Ranasinghe},
      year={2021},
      eprint={2006.10933},
      archivePrefix={arXiv},
      primaryClass={cs.CR}
}
```

The original results are produced on a workstation with AMD Ryzen 7 3700X CPU (8 cores, 16 threads, 3.6 GHz), 16 GB RAM, and the operating system is Linux Mint 20. To reproduce the results, a machine with similar CPUs(at least 2 cores and 2.10GHz), 4 GB or larger RAM is required. Running the artifact on a different machine could possibly diverge the execution and lead to different results.   

## Docker Setup
We offer a docker image for convenience. You can follow one of the following instructions to run the docker image.

#### Prebuilt Docker image from DockerHub
```shell
 $ docker pull zachgenius/covidguardian
 $ docker run -it -p 5000:5000 zachgenius/covidguardian:latest
```

or
#### Building Image from Dockerfile
```shell
 $ git clone https://github.com/covid-guardian/covid-guardian.git
 $ cd covid-guardian
 $ docker build -t covidguardian .
 $ docker run -it -p 5000:5000 covidguardian
```

Then the docker's port 5000 is bound to the localhost:5000, and you can access the web page via http://localhost:5000.

## Manual Setup
This project requires python3 and Java environment. 
So please ensure **Python3 (>=3.7)**, **Java (>=8)**, and **Android SDK** have been installed.

__FIRST__, please move into ```src/```

#### 1 Quick setup
If you are using *nix/macOS system, the script ```setup.sh``` can be used for setting up quickly.
```shell
 $ sh setup.sh
```

#### 2 Manual setup
Please run the following commands in PowerShell or CMD prompt in Windows, or shell in *nix/macOS
```shell
 $ python3 -m venv
 $ source venv
 $ python3 -m pip install -r requirements.txt
```

## Configuration
Then, please fill in the proper absolute path of android sdk in ```assets/config.yaml``` 
```text
sdk: 'path_to_android_sdk'
```

If you want to verify apk files through VirusTotal, please input your api_key of VirusTotal in ```assets/config.yaml```
```text
vt_api_key: 'your api key'
```

You can also generate your own source and sink list by replacing ```assets/SourcesAndSinks.txt```.

You can also add your own _**sensitive pii keywords**_ into ```assets/pii_keywords```. _**One**_ keyword per line.

## Usage
COVIDGuard offers two running modes: __Command line mode__ and __Web mode__.

### 1. Clone COVIDGuardian repo.
```bash
  $ git clone https://github.com/covid-guardian/covid-guardian 
```
### 2. Running
#### 2.1 Command line mode
 
```
usage: python main.py [-h] [-n PARALLEL_NUMBER] APK_OR_DIRECTORY_PATH

```
Mandatory arguments:
* `APK_PATH` is used to set the path to the APK file or a directory containing APK files

Optional arguments:
* `-h, --help` is used to show the help message and exit
* `-n PARALLEL_NUMBER` is used to set the number of parallel works, default is the number of CPU cores

#### 2.2 Web mode
You can run the web server by running the script ```server.sh```:
```bash
 $ sh server.sh
```

Then the server will run on the port 5000. Please visit http://localhost:5000 to open the front page.

## Output
The evaluation results will be output in a `yaml` file named by the apk filename, e.g., `COVID Alert 1.0.3.apk.yaml`. There are 5 categories of testing items:
* `app` presents the apk information extracted from the `AndroidManifast.xml` file, which includes
  * `activities_launch_mode`: An Activity should not be having the launch mode attribute set to "singleTask/singleInstance" as it becomes root Activity, and it is possible for other applications to read the contents of the calling Intent. So it is required to use the "standard" launch mode attribute when sensitive information is included in an Intent.
  * `allow_backup`: This flag allows anyone to back up your application data via adb. It allows users who have enabled USB debugging to copy application data off of the device.
  * `app_name`: The name of this app.
  * `debuggable`: Debugging was enabled on the app which makes it easier for reverse engineers to hook a debugger to it. This allows dumping a stack trace and accessing debugging helper classes.
  * `min_sdk`: Minimum SDK version supported by this app.
  * `package_name`: The package name of this app.
  * `permissions`: Permission list. The list is divided into several categories: dangerous, normal, other, signature and signatureOrSystem. The dangerous level denotes to sensitive permissions, e.g. Camera, that the app is requiring.
  * `target_sdk`: Target SDK version. Used in the development.
  * `use_cleartext_traffic`: If this value is true, the app allows network connections to transfer plain text though the Internet without encryption.
  * `version_code`: Version code, e.g. 10.
  * `version_name`: Version name, e.g. 1.0.2.
* `code_analysis` Code analysis. Each section provide a list of correspondence classes.
  * `insecure_certificate_validation`: Insecure Implementation of SSL. Trusting all the certificates or accepting self-signed certificates is a critical Security Hole. This application is vulnerable to MITM attacks
  * `insecure_random_generator`: The App uses an insecure Random Number Generator.
  * `insecure_webview_implementation`: Insecure WebView Implementation. Execution of user controlled code in WebView is a critical Security Vulnerability.
  * `ip_disclosure`: IP Address disclosure.
  * `remote_webview_debugging`: Remote WebView debugging is enabled.
  * `risky_cryptographic_algorithms`: The App uses wrong mode in Cryptographic encryption algorithm. Some modes are known to be weak as they result in the same ciphertext for identical blocks of plaintext.
  * `sql_hardcoded_secrets`: This App uses SQL Cipher. But the secret may be hardcoded.
  * `sql_raw_queries`: App uses SQLite Database and execute raw SQL query. Untrusted user input in raw SQL queries can cause SQL Injection. Also sensitive information should be encrypted and written to the database.
  * `trackers`: Tracker list.
* `pii_taint_result` Sensitive PII keys leaked
  * `leaked_keys`:
* `root_analysis` Whether the app integrates techniques of root and debug detection or not.
  * `debug_detections`: Debug detection
  * `root_detections`: Root detection
  * `root_usage`: Execute root permission
* `virus_total` Information from VirusTotal
  * `md5`:
  * `permalink`:
  * `resource`:
  * `response_code`:
  * `scan_id`:
  * `sha1`:
  * `sha256`:
  * `verbose_msg`: 
