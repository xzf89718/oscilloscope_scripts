# Oscilloscope scripts
This project contains interface to help you collect waveform data from osilloscope and transform them into root file. If you prefer old version follow the slides. Please check here: https://github.com/xzf89718/oscilloscope_scripts/tree/v7.2 and https://github.com/xzf89718/oscilloscope_scripts/releases/tag/v7.2
## Getting started  
### Setup python and NI-VISA  
#### For Windows   
Python 3.8:   
https://www.python.org/downloads/release/python-383/   
NI-VISA:   
https://www.ni.com/zh-cn/support/downloads/drivers/download.ni-visa.html  
#### For Linux/Mac OS 
Please install libserial or other lib as backen  
### Install   
#### Install package with pip     
```bash
pip install oscilloscope-scripts-xzf8971  
```
```bash
pip install git+
Get source code from github:  
```bash
git clone git@github.com:xzf89718/oscilloscope_scripts.git
```   

### The commands here aim to setup package for python  
```bash
pip install -U virtualenv  
virtualenv -p 3.8 ~/pyvisa_3d8  
~/pyvisa_3d8/Scripts/activate  
```

## How to use this package
### Every Login
```bash
cd ~/pyvisa_3d8/Scripts     
.\activate  
```
### Use Tektronix_TBS2000B_scripts for TBS2000B DAQ
#### Batch mode  
```bash
python -m Tektronix_TBS2000B_scripts this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name auto --mode batch
# On macOS or linux
# python -m Tektronix_TBS2000B_scripts this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name auto --mode batch --backen pyvisa-py
```
#### Interactive mode (for debug)
```bash
python -m Tektronix_TBS2000B_scripts this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name auto --mode inter
# On macOS or linux
# python -m Tektronix_TBS2000B_scripts this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name auto --mode inter --backen pyvisa-py
Enter your scope_name, also provide "default" and "auto" for quick setup  
auto  
```
If the setup is correct, you will got a plot contain waveforms from CH1 and CH2  


## Get some help
Example: $python  xxx.py --help  
Read the comments on the begin of each scripts  

## Other materials
In order to use the root scripts, you need ROOT and pyroot setup. Get Ubuntu20.04 VM with ROOT here: https://box.nju.edu.cn/d/045506afb0f347b78806/   
How to build your own ROOT release on Ubuntu20.04: https://blog.csdn.net/weixin_44121665/article/details/102637844?spm=1001.2014.3001.5502  
Data collected by me, without proper Impedance matching: https://box.nju.edu.cn/d/8c35131d91e846c4ada6/     
## Contact me
Author: Zifeng XU  
Email:  
zifeng.xu@foxmail.com  
mg20220214@smail.nju.edu.cn  
zifeng.xu@cern.ch  
