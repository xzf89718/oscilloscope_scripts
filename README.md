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
cd ~/pyvisa_3d8/Scripts  
.\activate   
pip install pyvisa scipy matplotlib numpy pandas  
4. Congratulations, you have already installed this package. If you want to run analysis and packup scipts, you need ROOT, search CERN ROOT for more details.    
# Usage
This project contains interface to help you collect waveform data from osilloscope and transform them into root file.
# Contact me
Author: Zifeng XU  
Email: zifeng.xu@cern.ch
# Why
Proposal:     
Usage:   
# TODO
Add oscilloscope setup for SiPM and PMT  
# How to
## Every Login
cd ~/pyvisa_3d8/Scripts/activate    
.\activate  
## Example
### RunMeasurement.py 
Example: python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --outputdir output_dir    
Output filename for example will be this_is_an_example-CH1.csv in output_dir. This command save 5 waveforms in output_dir  
### Transform_csv_to_tree.py
Example: python Transform_csv_to_tree.py this_is_an_example.root input_dir input_file_name this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --n_max_points 2000  
### Plot_waveform_from_root.py  
Example: python Plot_waveform_from_root.py this_is_an_example.root --n_plot_waveforms 10 --plot_channels CH1,CH2,CH3 --save_names this_is_an_example
## Get some help
Example: python  xxx.py --help  
Read the comments on the begin of each scripts  
