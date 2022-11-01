#!/usr/bin/env python
# Author: Zifeng Xu, Changge Zi.
# Email: zifeng.xu@cern.ch
# Note:1, How to detect muon decay events in our lab?
#      2, Only sample the channel you already setup
import pyvisa
import time
import sys

import numpy as np
import matplotlib.pyplot as plt


class Oscilloscope():

    """
    This class include method of initialize and setup the oscilloscope via usb.
    And some methods to measure the waveform and get the data.

    """

    def __init__(self, resource_name='USB0::0x0699::0x03C7::C011248::INSTR'):
        print("Osilloscope::INFO instrumente name: {0}".format(resource_name))
        # enable libvisa support. Only available on Mac and Windows
        self.resource_manager = pyvisa.ResourceManager()
        # enable full python pyvisa
        # self.resource_manager=pyvisa.ResourceManager("@py")
        self.inst = self.resource_manager.open_resource(
            resource_name=resource_name)
        self.inst.timeout = 10000  # ms
        self.inst.encoding = 'latin_1'
        self.inst.read_termination = '\n'
        self.inst.write_termination = None
        self._channel = 'DEFAULT'
        self.inst.write('*cls')  # clear ESR
        self.inst.write('header OFF')  # disable attribute echo in replies
        print(self.inst.query('*idn?'))
        # autoset
        # self.Autoset()

    def Sampling(self, sammple_channels="CH1", M=2000):  # M is the number of sampling points
        list_channels = sammple_channels.split(',')
        # Prepare sampling
        # default setup
        # self.inst.write('*rst')
        r = self.inst.query('*opc?')  # sync

        # acquisition
        self.inst.write('acquire:state OFF')  # stop
        self.inst.write('acquire:stopafter SEQUENCE;state ON')  # single
        r = self.inst.query('*opc?')

        # curve configuration
        self.inst.write('data:encdg SRIBINARY')  # signed integer
        acq_record = int(M)  # self.inst.query('horizontal:recordlength?')
        # 2021/06/14 Zifeng edit, This is a very importrant bug! You must specified the start point of the query!
        # For TBS2000B, 1 to 2500 means a full waveform!
        # If you dont specified, a random start will applied, what is not you want exactly.
        self.inst.write('data:start 1')
        self.inst.write('data:stop {0}'.format(acq_record))
        self.inst.write('wfmoutpre:byt_nr 1')  # 1 byte per sample

        dic_waveforms = {}
        dic_scaledtime = {}
        for channel in list_channels:
            self.SetChannel(channel)
            self.inst.write('data:source {0}'.format(self._channel))
            # data query
            # send message in binary form
            bin_wave = self.inst.query_binary_values(
                'curve?', datatype='b', container=np.array)
            # retrieve scaling factors
            wfm_record = int(self.inst.query('wfmoutpre:nr_pt?'))
            pre_trig_record = int(self.inst.query('wfmoutpre:pt_off?'))
            t_scale = float(self.inst.query('wfmoutpre:xincr?'))
            # sub-sample trigger correction
            t_sub = float(self.inst.query('wfmoutpre:xzero?'))
            v_scale = float(self.inst.query(
                'wfmoutpre:ymult?'))  # volts / level
            # reference voltage
            v_off = float(self.inst.query('wfmoutpre:yzero?'))
            # reference position (level)
            v_pos = float(self.inst.query('wfmoutpre:yoff?'))

            # error checking
            r = int(self.inst.query('*esr?'))
            r = self.inst.query('allev?').strip()

            # create scaled vectors
            # horizontal (time)
            total_time = t_scale * wfm_record
            t_start = (-pre_trig_record * t_scale) + t_sub
            t_stop = t_start + total_time
            scaled_time = np.linspace(
                t_start, t_stop, num=wfm_record, endpoint=False)

            # vertical (voltage)
            # data type conversion
            unscaled_wave = np.array(bin_wave, dtype='double')
            scaled_wave = (unscaled_wave - v_pos) * v_scale + v_off
            dic_scaledtime[channel] = scaled_time
            dic_waveforms[channel] = scaled_wave
        # return scaled_time, scaled_wave
        return dic_scaledtime, dic_waveforms

    def MeasureFreq(self, measure_channels="CH1"):  # MEASUre Frequency
        dic_freq = {}
        for _channel in measure_channels.split(','):
            self.SetChannel(_channel)
            self.inst.write(
                ':MEASUrement:IMMed:SOUrce1 {0}'.format(self._channel))
            self.inst.write(':MEASUrement:IMMed:TYPe FREQuency')
            dic_freq[_channel] = self.inst.query(':MEASUrement:IMMed:VALue?')
        return dic_freq

    def MeasureAmpl(self, measure_channels="CH1"):  # MEASUre Amplitude
        dic_ampl = {}
        for _channel in measure_channels.split(','):
            self.SetChannel(_channel)
            self.inst.write(
                ':MEASUrement:IMMed:SOUrce1 {0}'.format(self._channel))
            self.inst.write(':MEASUrement:IMMed:TYPe AMPlitude')
            dic_ampl[_channel] = self.inst.query(':MEASUrement:IMMed:VALue?')
        return dic_ampl

    def MeasureHigh(self, measure_channels="CH1"):  # MEASUre Low
        dic_high = {}
        for _channel in measure_channels.split(','):
            self.SetChannel(_channel)
            self.inst.write(
                ':MEASUrement:IMMed:SOUrce1 {0}'.format(self._channel))
            self.inst.write(':MEASUrement:IMMed:TYPe HIGH')
            dic_high[_channel] = self.inst.query(':MEASUrement:IMMed:VALue?')
        return dic_high

    def MeasureLow(self, measure_channels="CH1"):  # MEASUre Low
        dic_low = {}
        for _channel in measure_channels:
            self.SetChannel(_channel)
            self.inst.write(
                ':MEASUrement:IMMed:SOUrce1 {0}}'.format(self._channel))
            self.inst.write(':MEASUrement:IMMed:TYPe LOW')
            dic_low[_channel] = self.inst.query(':MEASUrement:IMMed:VALue?')
        return dic_low

    def SetChannel(self, channel):
        """
        Set channel for Measure and Sampling
        example, "CH1" "CH2"
        """

        # Check if channel is legal
        if(channel == 'DEFAULT'):
            print(
                "Oscilloscop::WARNING the channel is set to DEFAULT now, no measure of data-save is proceeded")
        if(channel == 'CH1'):
            self._channel = channel
            print("Set CH1")
        elif(channel == 'CH2'):
            self._channel = channel
            print("Set CH2")
        elif(channel == 'CH3'):
            self._channel = channel
            print("Set CH3")
        elif(channel == 'CH4'):
            self._channel = channel
            print("Set CH4")
        else:
            # self._channel = "DEFAULT"
            # print("The select channel should be one of CH1, CH2, CH3, CH4\nSet DEFUALT")
            ex = Exception("Oscilloscope::ERROR Sampling channl not exist. Example:CH1,CH2,CH3,CH4")
            raise ex

    def Autoset(self):
        self.inst.write('autoset EXECUTE')

    # disconnect
    def Close(self):
        self.inst.close()
        self.resource_manager.close()


def WriteToCsv(output_filename, array_time, array_voltage, sep=','):
    # Check the len of time and voltage
    length_of_time = len(array_time)
    length_of_voltage = len(array_voltage)
    if(not(length_of_time == length_of_voltage)):
        ex = Exception("The size of time and voltage is not equal")
        raise ex
    # Write header
    try:
        with open(output_filename, 'w') as file_object:
            file_object.write("scaled_time{0}scaled_voltage\n".format(sep))
            i = 0
            while (i < length_of_voltage):
                file_object.write("{0}{1}{2}{3}".format(
                    str(array_time[i]), sep, str(array_voltage[i]),  "\n"))
                i = i + 1
    except FileNotFoundError:
        print("Oscilloscope WriteToCsv ERROR: {0} not exist. Create this dir first. like $mkdir {0} or just create this in Windows GUI. This scripts has been terminated.".format(output_filename.split("/")[0]))
        sys.exit()