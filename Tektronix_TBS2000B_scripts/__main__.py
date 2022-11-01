#!/usr/bin/env python

# Author: Zifeng XU
# Email: zifeng.xu@cern.ch
# Usage: provide interafate to save waveform data from Tek TBS2000B oscilloscope
# Make sure you have output_dir, make sure the save_channels is enable in oscilloscope
# Example: python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir
# Use auto scope_name, the first name
# Example: python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name auto
# Example: python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir --scope_name USB0::0x0699::0x03C7::C011248::INSTR
# Output filename for example will be this_is_an_example-CH1.csv in output_dir
import argparse
import time

import pyvisa

from Tektronix_TBS2000B_scripts.helper_function import batchDataTaking, interactiveDataTaking

# Batch mode
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Save multiple waveform into csv files. You can even make measure. Author: Zifeng XU, email: zifeng.xu@cern.ch")
    parser.add_argument("output_filename", type=str,
                        help="Output file name for waveforms")
    parser.add_argument("--n_save_waveforms", type=int, default=10,
                        help="N_Waveforms save in the output scripts")
    parser.add_argument("--save_channels", type=str, default="CH1",
                        help="Which channel should we save in the scripts? Example: CH1,CH2. Becarful, if you add wrong Channel here, often cause this program break down")
    parser.add_argument("--output_dir", type=str, default="./",
                        help="Which directory to save waveform data, please make sure you have this directory in you USB. For examle: /usb0/waveform_data")
    parser.add_argument("--scope_name", type=str, default="default",
                        help="scope_name, every oscilloscope has its own name, which is needed when instantiate the Scope, default, auto, and specify the name you like is supported")
    parser.add_argument("--mode", type=str, choices=["batch", "inter"], required=True, help="Supported options: inter batch")
    parser.add_argument("--backen", type=str, default="NIVISA", choices=["NIVISA", "pyvisa-py"], help="Supported options: NIVISA, pyvisa-py")
    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    output_filename = args.output_filename
    n_save_waveforms = args.n_save_waveforms
    save_channels = args.save_channels
    output_dir = args.output_dir
    scope_name = args.scope_name
    mode = args.mode
    backen = args.backen

    print("Here are instruments' name you have:")
    if (backen == "NIVISA"):
        resource_manager = pyvisa.ResourceManager()
    elif (backen == "pyvisa-py"):
        resource_manager = pyvisa.ResourceManager("@py")
    inst_name = resource_manager.list_resources()
    print("{0}".format(inst_name))
    time.sleep(3)
    if (mode == "batch"):
        batchDataTaking(output_filename, n_save_waveforms,
                        save_channels, output_dir, scope_name, inst_name)
    elif (mode == "inter"):
        interactiveDataTaking(inst_name, save_channels)
