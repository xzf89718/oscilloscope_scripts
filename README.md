# Setup this packate and dependencies
1. get this package:  
git clone git@github.com:xzf89718/oscilloscope_scripts.git   
2. check out to newest release  
// For example, checkout to v2.1 realease  
git checkout v2.1  
3. setup python, NI-VISA, PYVISA, numpy, scipy, matplotlib, pandas  
// For Ubuntu/Debian  
// Make sure you have python3, if not  
// sudo apt install python3  
 sudo apt install libvisa-dev   
// For Debian, sudo apt install libvisa0-dev    
WARNING: It is not recommended to connect oscilloscope on Ubuntu, or other distrution. Since NI-VISA is only available on Mac and Windwos. But it is still possible to use some lib on Debian and Ubuntu

// For Windows  
NI-VISA:  
https://www.ni.com/zh-cn/support/downloads/drivers/download.ni-visa.html  
Python 3.8:  
https://www.python.org/downloads/release/python-383/  

// The commands here aim to setup package for python  
pip install -U virtualenv  
virtualenv -p 3.8 ~/pyvisa_3d8  
// On Ubuntu  
// source ~/pyvisa_3d8/bin/activate  
cd ~/pyvisa_3d8/Scripts/activate  
.\activate   
pip install pyvisa scipy matplotlib numpy pandas  
4. Congratulations, you have already installed this package. If you want ROOT, bing CERN ROOT for more details.    
# Usage
This projects aim to generate scripts for TBS2000B osilloscope. In order to save many waveforms for multiple channels. Also, you will find scripts to help you analyze the waveform data. i.e. analysis_waveform_data.py or single_channel_selector.C, which required ROOT installed. A raspberry pi 4 is already setup python and root on it. Please contact me to get the ip address and accout.
# Contact me
Author: Zifeng XU  
Email: zifeng.xu@cern.ch
# Why
Proposal: save oscilloscope  
Usage: Use it to generate scripts for OpenChoice Talker Listener  
# TODO
Add oscilloscope setup for SiPM and PMT  
# How to
## Every Login
cd ~/pyvisa_3d8/Scripts/activate    
.\activate  
## Example
Try it, simply, this command generate a script names output_scripts_names, which save 100 waveforms, and divide them into three channels.  
Example: python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --outputdir output_dir  
## Get some help
Example: python  xxx.py --help  
Read the comments on the begin of each scripts  
