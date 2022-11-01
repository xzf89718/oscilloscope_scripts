from Tektronix_TBS2000B_control.oscilloscope_control import Oscilloscope, WriteToCsv
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import pyvisa


def Software_trigger(dic_scaled_time, dic_scaled_voltage):
    """
    User software trigger
    """

    # Pass tirgger
    return True


def sampleOnce(inst, save_channels='CH1,CH2'):
    try:
        wavetime, waveform = inst.Sampling(save_channels)
        wavetime, waveform = inst.Sampling(save_channels)
    except pyvisa.VisaIOError as error:
        print(
            "The oscilloscope is not triggered more than 10s. VI_ERROR_TMO\n\033[33mA kindly remind: Check TRIGGER on oscilloscope, make sure you got a signal on the screen when press Single\033[0m")
        print("The information below is prepared for experts:\n\033[31mVisaIOError\033[0m, meassage:{0}".format(
            error.args))
        return False
    for channel in save_channels.split(","):
        plt.plot(wavetime[channel], waveform[channel])
        print(len(waveform[channel]))
    plt.xlabel('time')
    plt.ylabel('voltage')
    plt.savefig('sample_once_{channels}'.format(
        channels=save_channels.replace(',', '_')))
    plt.show()


def interactiveDataTaking(inst_name, save_channels="CH1,CH2"):
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
        sampleOnce(inst=Scope, save_channels=save_channels)
    except pyvisa.VisaIOError:
        print("Fail to create a Osilloscope object.\n1, Check connection between oscilloscope and computer\n2, Check the name of Scope and the inst_name")


def batchDataTaking(output_filename,
                    n_save_waveforms,
                    save_channels,
                    output_dir,
                    scope_name, inst_name):
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
        print(
            "**************{0:.1f}% job is processed.***************".format(percentage_of_job*100))
        time_left = t_mean*(n_save_waveforms-i_waveform)  # (s)
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
