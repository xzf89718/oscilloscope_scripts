#!/usr/bin/env python

# Author: Zifeng XU
# Email: zifeng.xu@cern.ch
# Proposal: save oscilloscope
# Usage: Use it to generate scripts for OpenChoice Talker Listener
# TODO
# Add oscilloscope setup for SiPM and PMT
# Example: python RunMeasurement.py this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --output_dir output_dir
import argparse
import time

import numpy as np
import matplotlib.pyplot as plt
import pyvisa

from Oscilloscope import Oscilloscope, WriteToCsv


def SampleOnce(inst, list_channels='CH1,CH2'):
    wavetime, waveform = inst.Sampling(list_channels)
    for channel in list_channels.split(","):
        plt.plot(wavetime[channel], waveform[channel])
    plt.xlabel('time')
    plt.ylabel('voltage')
    plt.show()

if not(__name__ == "__main__"):
    try:
        # Interactive mode
        Scope = Oscilloscope()
        print("Interactive mode")
        print("Use command SampleOnce(Scope,\"CH1,CH2\")")
    except:
        print("Check connection between oscilloscope and computer")

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
    parser.add_argument("--output_dir", type=str, default="",
                        help="Which directory to save waveform data, please make sure you have this directory in you USB. For examle: /usb0/waveform_data")
    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    output_filename = args.output_filename
    n_save_waveforms = args.n_save_waveforms
    save_channels = args.save_channels.split(',')
    output_dir = args.output_dir
    # oscilloscope_setup_scripts = args.oscilloscope_setup_scripts

    print("****************************************************************************************")
    print("****************************************************************************************")
    print("****************************************************************************************")
    print("*                Please check the channel option here very carefully                   *")
    print("****************************************************************************************")
    print("****************************************************************************************")
    print("****************************************************************************************")

    # Initialize Oscilloscope
    Scope = Oscilloscope()
    # Loop from 0 to n_save_waveforms, save all wave form
    for i_waveform in range(0, n_save_waveforms):

        for _channel in save_channels:
            # print('Hello, wolrd!')
            # Autoset, you wont want this in our measurement!
            # Scope.Autoset()
            wavetime, waveform = Scope.Sampling("CH1,CH2")
            print("time: {0}\nwaveform: {1}".format(wavetime, waveform))
            WriteToCsv("{3}/{0}-{1}-{2}.csv".format(output_filename, _channel,
                       str(i_waveform), output_dir), wavetime[_channel], waveform[_channel])
            # plt.plot(wavetime,waveform)
            # plt.show()
            time.sleep(0.5)

    Scope.Close()
