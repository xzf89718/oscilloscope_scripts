#!/usr/bin/env python

# Author: Zifeng XU
# Email: zifeng.xu@cern.ch
# Proposal: save oscilloscope
# Usage: Use it to generate scripts for OpenChoice Talker Listener
# TODO
# Add oscilloscope setup for SiPM and PMT
# Example: python Tektronix_continuous_savewaveform.py output_filename output_scripts_name --n_save_waveforms 100 --save_channels CH1,CH2 --output_dir  output_dir
# Example: python .\Tektronix_continuous_savewaveform.py test save_100_waveforms.txt --save_channels CH1,CH2 --n_save_waveforms 100
# Example: python  Tektronix_continuous_savewaveform --help
import argparse


def AddLineBreak(line):
    return line + "\n"


parser = argparse.ArgumentParser(
    description="Use this script to generate scripts for osilloscope Author: Zifeng XU, email: zifeng.xu@cern.ch")

parser.add_argument("output_filename", type=str,
                    help="Output file name for waveforms")
parser.add_argument("output_scripts_name", type=str,
                    help="Output scripts name for oscilloscope scripts")
parser.add_argument("--n_save_waveforms", type=int, default=10,
                    help="N_Waveforms save in the output scripts")
parser.add_argument("--save_channels", type=str, default="CH1,CH2",
                    help="Which channel should we save in the scripts? Example: CH1,CH2")
parser.add_argument("--output_dir", type=str, default="/usb0",
                    help="Which directory to save waveform data, please make sure you have this directory in you USB. For examle: /usb0/waveform_data")

args = parser.parse_args()
print("All parameters get from commandline are:")
print(args)

output_filename = args.output_filename
output_scripts_name = args.output_scripts_name
n_save_waveforms = args.n_save_waveforms
save_channels = args.save_channels
output_dir = args.output_dir

print(output_filename)
print(output_scripts_name)
print(n_save_waveforms)
print(save_channels)
print(output_dir)

cm_begin_of_scripts = "Talker Listener Script: <<Script1>>"
# Add command here in the future to setup oscilloscope
cm_setup_oscillosocpe = ""
cm_stop_oscilloscope = "ACQUIRE:STOPAFTER SEQUENCE"
cm_single = "ACQUIRE:STATE ON"
cm_wait_response = "*OPC?"
cm_synchronize = "*WAI"
cm_save_waveform = "SAVe:WAVEfrom"

if __name__ == "__main__":
    with open(output_scripts_name, "w") as file_object:
        # Write headers into output_scripts_file
        file_object.write(AddLineBreak(cm_begin_of_scripts))
        # setup oscillopscope
        file_object.write(AddLineBreak(cm_setup_oscillosocpe))
        # stop oscilloscope, prepare to save waveform
        file_object.write(AddLineBreak(cm_stop_oscilloscope))

        # begin to get single waveform
        for i in range(0, n_save_waveforms):
            for channel in save_channels.split(","):
                save_command = "{0} {1}, {2}/{3} ".format(
                    cm_save_waveform, channel, output_dir, output_filename+"-" + channel+"-"+str(i)+".csv")
                # print(save_command)
                file_object.write("{0}{1}{2}{3}".format(AddLineBreak(cm_single), AddLineBreak(
                    cm_wait_response), AddLineBreak(save_command), AddLineBreak(cm_wait_response)))
