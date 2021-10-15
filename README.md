# Setup this packate and dependencies
1. get this package:  
$git clone git@github.com:xzf89718/oscilloscope_scripts.git   
2. check out to newest release   
// For example, checkout to v2.1 realease   
$git checkout v2.1   
3. setup python, NI-VISA, PYVISA 
// For Windows   
NI-VISA:   
https://www.ni.com/zh-cn/support/downloads/drivers/download.ni-visa.html   
Python 3.8:   
https://www.python.org/downloads/release/python-383/   

## The commands here aim to setup package for python  
$pip install -U virtualenv  
$virtualenv -p 3.8 ~/pyvisa_3d8  
$~/pyvisa_3d8/Scripts/activate  
Now you're able to collect data via the RunMeasurement.py scripts!  
These for analysis:  
(pyvisa_3d8)$pip install pyvisa scipy matplotlib numpy pandas ipython  

4. Congratulations, you have already installed this package. If you want to run analysis and packup scipts, you need ROOT, search CERN ROOT for more details.   
5. In order to use the root scripts, you need ROOT and pyroot setup. Get Ubuntu20.04 VM with ROOT here: https://box.nju.edu.cn/d/045506afb0f347b78806/   
6. How to build your own ROOT release on Ubuntu20.04: https://blog.csdn.net/weixin_44121665/article/details/102637844?spm=1001.2014.3001.5502  
# Usage
This project contains interface to help you collect waveform data from osilloscope and transform them into root file.
# Contact me
Author: Zifeng XU  
Email: zifeng.xu@foxmail.com  
mg20220214@smail.nju.edu.cn  
zifeng.xu@cern.ch  
# How to
## Every Login
$cd ~/pyvisa_3d8/Scripts     
$.\activate  
## Example
### RunMeasurement.py 
Batch mode:  
Example: $python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir      
Run with auto mode scope name  
Example: $python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name auto
Interactive mode:  
$ipython  
[0] import RunMeasurement  
[1] RunMeasurement.SampleOnce(RunMeasurement.Scope, "CH1,CH2")  
[2] Enter your scope_name, also provide "default" and "auto" for quick setup  
[3] auto  
If the setup is correct, you will got a plot contain waveforms from CH1 and CH2  

### Transform_csv_to_tree.py
Example: $python Transform_csv_to_tree.py this_is_an_example.root input_dir input_file_name this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --n_max_points 2000  
### Plot_waveform_from_root.py  
Example: $python Plot_waveform_from_root.py this_is_an_example.root --n_plot_waveforms 10 --plot_channels CH1,CH2,CH3 --save_names this_is_an_example
### Do cut on waveform data and do fit
At the very begining, make the workspace, contains pdf you need  
$root MakeWorkspaceForGain.C  
$root some_waveform_data.root  
$tree_waveform_CH1->Process("single_channel_selector.C", "test_tree.root")  
$.q  
$root test_tree.root  
$event->Process("OutputCharge.C")  
$.q  
$root UseWorkspaceForFit.C  
### Data collected by me, without proper Impedance matching
https://box.nju.edu.cn/d/8c35131d91e846c4ada6/   
## Get some help
Example: $python  xxx.py --help  
Read the comments on the begin of each scripts  
