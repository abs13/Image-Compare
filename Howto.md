
# <u> How To (Image Compare) </u>

Image compare is a python script that reads an input csv file and compare two images provided on each row. 
- The utility uses [imagehash](https://pypi.org/project/ImageHash/) module for core image comparison.
- Algorithm used was *phash* or perceptual hash.
- The perceptual hash of two images is calculated followed by the hamming distance.

## Assumptions:
    The users uses a OS specific input csv file with approriate root dir 
    (e.g. windows paths begin with '<dirve name>:\' and linux/macOS paths begin with '/' )
    If wrong platform paths are detected, the image files are considered to be missing and the comparison is skipped for the row

## Platform Support
- The pre-built executable can be run on Windows 10, Linux and Mac OSX (Mojave and Catalina). 

- For other platforms, use the python script *image_compare.py*
## Distributions:

### Pre-build exe files
- Available for Windows 10, Linux and macOS.
- These can be found under individual directories under dist folder. 

![distribution_dir_tree](resources/dist_dir_tree.PNG)

##### Linux : 
The utility has been tested on Centos 7, Centos 8, Ubuntu 20.04.1 LTS and Vagrant.

[linux](dist/linux/image_compare)
##### Windows : 
The utility has been tested on windows 10

[windows](dist/windows/image_compare.exe)
##### macOS :
macOS support has been tested on Mojave and Catalina. 
The distribution has been code-signed using self generated certificates.

[macOS](dirs/../dist/mac/image_compare)

###  Python script setup
The code base folder contains the *image_compare.py* python script 

> To run as a python script, follow the instructions below.

##### Pre-requisites:
1. Python 3.5 or greater
2. imagehash
3. Pillow
###### Check python version:
``` python
        python3 --version
```
###### Install python module dependencies using pip:
Module dependencies are bundled together in [requirments.txt](requirments.txt) and can be installed using 
```Python
       python3 -m pip install -r requirments.txt
```

### Input parameters and Output file
#### Input csv file: 
    Required 
###### Input csv file format

![sample input](./resources/Sample_input.PNG)

##### Output csv file: 
    optional (defaults to *{input-filename}_results.csv*)
    ** In absence of an output filename on CLI, default output file is generated.
###### output csv file sample
![Sample_output](./resources/Sample_output.PNG)

## Usage :
*** *The utility is re-run able.
In the scenario when no output file is specified, a backup of previous default output files in <filename>_YYYY_MM_DD_H_M_S.csv format is created*

##### Linux exe:
###### Display usage help:

```bash
   ./image_compare -h
```
![linux_help](./resources/linux_help.png)
###### Display the version information:
```bash 
    ./image_compare -v
```
![linux_help_version](./resources/linux_version.png)
###### Execute image comparison :
```bash
 ./image_comapre -i <input csv file> -o <output csv file> *(Optional)
```
![linux_execute](./resources/linux_execute.png)


##### Windows exe:
###### Display usage help:
``` dos
image_compare -h
```
![windows_help](./resources/windows_help.png)
###### Display utility version:
```dos
image_compare -v
```
![windows_help_VERSION](./resources/windows_version.png)
###### Process image comparison:
```dos
image_compare -i <input csv file> -o <output csv file> *Optional*
```
![windows_help_exec](./resources/windows_execution.png)


#### Python script (Linux/macOS):
###### Display usage help:
```bash
   python image_compare.py -h
```
![macOShelp](./resources/py_script_macOS_help_.PNG)

###### Display the version information:
```bash 
    python image_compare.py -v
```
![macOSVer](./resources/py_script_macOS_ver_.PNG)
###### Process image comparison :
```bash
 python image_compare.py -i <input csv file> -o <output csv file> *(Optional)
```
![macOShelp](./resources/py_script_macOS_exec.PNG)

#### using python scripts (Windows):
```dos
   python image_compare.py -h
```
Display the version information:
```dos 
    python image_compare.py -v
```
Process image comparison :
```dos
 python image_compare.py -i <input csv file> -o <output csv file> *(Optional)
```
