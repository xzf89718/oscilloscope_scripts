# Usage
This projects aim to generate scripts for TBS2000B osilloscope. In order to save many waveforms for multiple channels. In the next step,
I will write scripts to transform those data in to TTree.
# Contact me
Author: Zifeng XU
Email: zifeng.xu@cern.ch
# Why
Proposal: save oscilloscope
Usage: Use it to generate scripts for OpenChoice Talker Listener
# TODO
Add oscilloscope setup for SiPM and PMT
# How to
## Example
Example: python Tektronix_continuous_savewaveform.py output_filename output_scripts_name --n_save_waveforms 100 --save_channels CH1,CH2 --output_dir  output_dir
Example: python .\Tektronix_continuous_savewaveform.py test save_100_waveforms.txt --save_channels CH1,CH2,CH3 --n_save_waveforms 100
Try it, simply, this command generate a script names output_scripts_names, which save 100 waveforms, and divide them into three channels.
## Get some help
Example: python  Tektronix_continuous_savewaveform --help