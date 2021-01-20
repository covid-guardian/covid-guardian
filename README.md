# CovidGuardPriv
This is the artifact accompanying the submission "An Empirical Assessment of Global COVID-19 Contact Tracing Applications".

The original results are produced on a workstation with xxx CPU (x cores, x GHz), x GB RAM, and the operating system is xxx. To reproduce the results, a machine with similar CPUs(~2.10GHz), x GB or larger RAM is required. Running the artifact on a different machine could possibly diverge the execution and lead to different results.   

## Setup
This project requires python3 and Java environment. 
So please ensure you have installed **python3 (>=3.7)**, **Java (>=8)** and **Android SDK**.

#### 1 Manual setup
Please run following commands in your PowerShell or CMD prompt in Windows, or shell in *nix/macOS
```shell
 $ python3 -m venv
 $ source venv
 $ python3 -m pip install -r requirement.txt
```

#### 2 Automatic setup
If you are using *nix/macOS system, the script ```setup.sh``` can be used for setting up quickly.
```shell
 $ sh setup.sh
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

Since data flow analysis is conducted by [FLowDroid](https://github.com/secure-software-engineering/FlowDroid),
you can generate your own source and sink list by replacing ```assets/SourcesAndSinks.txt```.

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