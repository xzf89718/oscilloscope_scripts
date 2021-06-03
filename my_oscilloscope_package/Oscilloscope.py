#!/usr/bin/env python
# Author: Zifeng Xu, Changge Zi.
# Email: zifeng.xu@cern.ch
# Note:1, How to detect muon decay events in our lab?
#      2, Only sample the channel you already setup
import pyvisa
import time

import numpy as np
import matplotlib.pyplot as plt
from pyvisa.constants import DataWidth


class Oscilloscope():

    """
    This class include method of initialize and setup the oscilloscope via usb.
    And some methods to measure the waveform and get the data.
  
    """

    def __init__(self, resource_name='USB0::0x0699::0x03C7::C011248::INSTR'):
        # enable libvisa support. Only available on Mac and Windows
        self.resource_manager = pyvisa.ResourceManager()
        # enable full python pyvisa
        # self.resource_manager=pyvisa.ResourceManager("@py")
        self.inst = self.resource_manager.open_resource(
            resource_name=resource_name)
        self.inst.timeout = 10000  # ms
        self.inst.encoding = 'latin_1'
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self._channel='DEFAULT'
        self.inst.write('*cls')  # clear ESR
        self.inst.write('header OFF')  # disable attribute echo in replies
        print(self.inst.query('*idn?')) 
        # autoset
        # self.Autoset()

       
    def Sampling(self, sammple_channels="CH1", M=2000):  # M is the number of sampling points
        list_channels=sammple_channels.split(',')
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
        self.inst.write('data:stop {0}'.format(acq_record))
        self.inst.write('wfmoutpre:byt_nr 1')  # 1 byte per sample

        dic_waveforms={}
        for channel in list_channels:
            self.SetChannel(channel)
            self.inst.write('data:source {0}'.format(self._channel))
            # data query
            # send message in binary form
            bin_wave = self.inst.query_binary_values('curve?', datatype='b', container=np.array)
            print(bin_wave)
            
            # retrieve scaling factors
            wfm_record = int(self.inst.query('wfmoutpre:nr_pt?'))
            pre_trig_record = int(self.inst.query('wfmoutpre:pt_off?'))
            t_scale = float(self.inst.query('wfmoutpre:xincr?'))
            # sub-sample trigger correction
            t_sub = float(self.inst.query('wfmoutpre:xzero?'))
            v_scale = float(self.inst.query('wfmoutpre:ymult?'))  # volts / level
            v_off = float(self.inst.query('wfmoutpre:yzero?'))  # reference voltage
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

        return scaled_time, scaled_wave

    def MeasureFreq(self):  # MEASUre Frequency
        self.inst.write(':MEASUrement:IMMed:SOUrce1 {0}'.format(self._channel))
        self.inst.write(':MEASUrement:IMMed:TYPe FREQuency')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def MeasureAmpl(self):  # MEASUre Amplitude
        self.inst.write(':MEASUrement:IMMed:SOUrce1 {0}'.format(self._channel))
        self.inst.write(':MEASUrement:IMMed:TYPe AMPlitude')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def MeasureHigh(self):  # MEASUre Low
        self.inst.write(':MEASUrement:IMMed:SOUrce1 {0}'.format(self._channel))
        self.inst.write(':MEASUrement:IMMed:TYPe HIGH')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def MeasureLow(self):  # MEASUre Low
        self.inst.write(':MEASUrement:IMMed:SOUrce1 {0}}'.format(self._channel))
        self.inst.write(':MEASUrement:IMMed:TYPe LOW')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def SetChannel(self, channel):
        """
        Set channel for Measure and Sampling
        example, "CH1" "CH2"
        """

        # Check if channel is legal
        if(channel == 'DEFAULT'):
            print("Oscilloscop::WARNING the channel is set to DEFAULT now, no measure of data-save is proceeded")
        if(channel == 'CH1'):
            self._channel=channel       
            print("Set CH1")
        elif(channel == 'CH2'):
            self._channel=channel
            print("Set CH2")
        elif(channel =='CH3'):
            self._channel=channel
            print("Set CH3")
        elif(channel=='CH4'):
            self._channel=channel
            print("Set CH4")
        else:
            self._channel="DEFAULT"
            print("The select channel should be one of CH1, CH2, CH3, CH4\nSet DEFUALT")



    def Autoset(self):
        self.inst.write('autoset EXECUTE')

    # disconnect
    def close(self):
        self.inst.close()
        self.resource_manager.close()

