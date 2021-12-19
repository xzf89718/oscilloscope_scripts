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
import os

import numpy as np
import matplotlib.pyplot as plt
import pyvisa

from Oscilloscope import Oscilloscope, WriteToCsv

def SampleOnce(inst, list_channels='CH1,CH2'):
    try:
        wavetime, waveform = inst.Sampling(list_channels)
        wavetime, waveform = inst.Sampling(list_channels)
    except pyvisa.VisaIOError as error:
        print("The oscilloscope is not triggered more than 10s. VI_ERROR_TMO\n\033[33mA kindly remind: Check TRIGGER on oscilloscope, make sure you got a signal on the screen when press Single\033[0m")
        print("The information below is prepared for experts:\n\033[31mVisaIOError\033[0m, meassage:{0}".format(error.args))
        return False
    for channel in list_channels.split(","):
        plt.plot(wavetime[channel], waveform[channel])
        print(len(waveform[channel]))
    plt.xlabel('time')
    plt.ylabel('voltage')
    plt.savefig('sample_once_{channels}'.format(
        channels=list_channels.replace(',', '_')))
    plt.show()


def Software_trigger(dic_scaled_time, dic_scaled_voltage):
    """
    User software trigger
    """

    # Pass tirgger
    return True


print("Here are instruments' name you have:")
resource_manager = pyvisa.ResourceManager()
inst_name = resource_manager.list_resources()
print("{0}".format(inst_name))

if not(__name__ == "__main__"):
    print("Interactive mode")
    print("Use command RunMeasurement.SampleOnce(RunMeasurement.Scope,\"CH1,CH2,CH3\")")
    try:
        # Interactive mode
        scope_name = input(
            "Enter your scope_name, also provide \"default\" and \"auto\" for quick setup\n")
        if (scope_name == "default"):
            Scope = Oscilloscope()
        elif (scope_name == "auto"):
            Scope = Oscilloscope(inst_name[0])
        else:
            Scope = Oscilloscope(scope_name)
    except pyvisa.VisaIOError:
        print("Fail to create a Osilloscope object.\n1, Check connection between oscilloscope and computer\n2, Check the name of Scope and the inst_name")

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
    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    output_filename = args.output_filename
    n_save_waveforms = args.n_save_waveforms
    save_channels = args.save_channels
    output_dir = args.output_dir
    scope_name = args.scope_name
    # oscilloscope_setup_scripts = args.oscilloscope_setup_scripts

    print("****************************************************************************************")
    print("****************************************************************************************")
    print("****************************************************************************************")
    print("*                Please check the channel option here very carefully                   *")
    print("****************************************************************************************")
    print("****************************************************************************************")
    print("****************************************************************************************")
    begin_time = time.time()
    # Initialize Oscilloscope
    if(scope_name == "default"):
        Scope = Oscilloscope()
    elif(scope_name == "auto"):
        Scope = Oscilloscope(inst_name[0])
    else:
        Scope = Oscilloscope(scope_name)
    # Loop from 0 to n_save_waveforms, save all wave form
    t_list = []
    for i_waveform in range(0, n_save_waveforms):
        t1 = time.time()
        # Autoset, you wont want this in our measurement!
        # Scope.Autoset()
        wavetime, waveform = Scope.Sampling(save_channels)
        while (not Software_trigger(wavetime, waveform)):
            wavetime, waveform = Scope.Sampling(save_channels)
        for _channel in save_channels.split(","):
            WriteToCsv("{3}/{0}-{1}-{2}.csv".format(output_filename, _channel,
                       str(i_waveform), output_dir), wavetime[_channel], waveform[_channel])
        t2 = time.time()

        t_list.append(t2-t1)
        t_mean = np.mean(t_list)

        percentage_of_job = float(i_waveform) / float(n_save_waveforms)
        # clear screen
        os.system("cls")
        print( "**************{0:.1f}% job is processed.***************".format(percentage_of_job*100))
        time_left = t_mean*(n_save_waveforms-i_waveform) # (s)
        print(time.strftime("%Mmin %Ss", time.gmtime(time_left)), "left")
    
    Scope.Close()
    os.system("cls")
    end_time = time.time()
    event_rate = float(n_save_waveforms) / (end_time - begin_time)

    print("****************************")
    print("****************************")
    print("**  Event rate: {0:.2f}Hz **".format(event_rate))
    print("****************************")
    print("****************************")
