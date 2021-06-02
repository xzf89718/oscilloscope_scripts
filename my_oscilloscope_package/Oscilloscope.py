#!/usr/bin/env python
# Author: Zifeng Xu, Changge Zi.
# Email: zifeng.xu@cern.ch
import pyvisa
import time

import numpy as np
import matplotlib.pyplot as plt


class Oscilloscope():

    """
    This class include method of initialize and setup the oscilloscope via usb.
    And some methods to measure the waveform and get the data.
    list_channels should like CH1,CH2,CH3
    """

    def __init__(self, list_channels='CH1', resource_name='USB0::0x0699::0x03C7::C011248::INSTR'):
        # enable libvisa support. Only available on Mac and Windows
        self.resource_manager = pyvisa.ResourceManager()
        # enable full python pyvisa
        # self.resource_manager=pyvisa.ResourceManager("@py")
        self.list_channels= list_channels.split(',')
        self.inst= self.resource_manager.open_resource(
            resource_name=resource_name)
        self.inst.timeout = 10000  # ms
        self.inst.encoding = 'latin_1'
        self.inst.read_termination = '\n'
        self.inst.write_termination = '\n'
        self.inst.write('*cls') # clear ESR
        self.inst.write('header OFF') # disable attribute echo in replies
        print(self.inst.query('*idn?'))
        # Create dictionary for 
        self.dic_waveform={}
        for channel in self.list_channels:
            self.dic_waveform[channel]=[]
            print("Create list for {0}".format(channel))


    def Sampling(self, M = 8192):     #M is the number of sampling points
        # default setup
        self.inst.write('*rst')
        #t1 = time.perf_counter()
        r = self.inst.query('*opc?') # sync
        #t2 = time.perf_counter()
        #print('reset time: {} s'.format(t2 - t1))

        # autoset
        self.inst.write('autoset EXECUTE')
        #t3 = time.perf_counter()
        r = self.inst.query('*opc?')
        #t4 = time.perf_counter()
        #print('autoset time: {} s'.format(t4 - t3))

        # acquisition
        self.inst.write('acquire:state OFF') # stop
        self.inst.write('acquire:stopafter SEQUENCE;state ON') # single
        #t5 = time.perf_counter()
        r = self.inst.query('*opc?')
        #t6 = time.perf_counter()
        #print('acquire time: {} s'.format(t6 - t5))

        # curve configuration
        self.inst.write('data:encdg SRIBINARY') # signed integer
        self.inst.write('data:source CH1')
        self.inst.write('data:start 1')
        acq_record = int(M)      #self.inst.query('horizontal:recordlength?')
        self.inst.write('data:stop {}'.format(acq_record))
        self.inst.write('wfmoutpre:byt_nr 1') # 1 byte per sample

        # data query
        #t7 = time.perf_counter()
        bin_wave = self.inst.query_binary_values('curve?', datatype='b', container=np.array)
        #t8 = time.perf_counter()
        #print('transfer time: {} s'.format(t8 - t7))

        # retrieve scaling factors
        wfm_record = int(self.inst.query('wfmoutpre:nr_pt?'))
        pre_trig_record = int(self.inst.query('wfmoutpre:pt_off?'))
        t_scale = float(self.inst.query('wfmoutpre:xincr?'))
        t_sub = float(self.inst.query('wfmoutpre:xzero?')) # sub-sample trigger correction
        v_scale = float(self.inst.query('wfmoutpre:ymult?')) # volts / level
        v_off = float(self.inst.query('wfmoutpre:yzero?')) # reference voltage
        v_pos = float(self.inst.query('wfmoutpre:yoff?')) # reference position (level)

        # error checking
        r = int(self.inst.query('*esr?'))
        #print('event status register: 0b{:08b}'.format(r))
        r = self.inst.query('allev?').strip()
        #print('all event messages: {}'.format(r))

        # create scaled vectors
        # horizontal (time)
        total_time = t_scale * wfm_record
        t_start = (-pre_trig_record * t_scale) + t_sub
        t_stop = t_start + total_time
        scaled_time = np.linspace(t_start, t_stop, num=wfm_record, endpoint=False)

        # vertical (voltage)
        unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
        scaled_wave = (unscaled_wave - v_pos) * v_scale + v_off
        return scaled_time, scaled_wave

    def MeasureFreq(self):    #MEASUre Frequency
        self.inst.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.inst.write(':MEASUrement:IMMed:TYPe FREQuency')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def MeasureAmpl(self):    #MEASUre Amplitude
        self.inst.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.inst.write(':MEASUrement:IMMed:TYPe AMPlitude')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def MeasureHigh(self):    #MEASUre Low
        self.inst.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.inst.write(':MEASUrement:IMMed:TYPe HIGH')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def MeasureLow(self):    #MEASUre Low
        self.inst.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.inst.write(':MEASUrement:IMMed:TYPe LOW')
        return (self.inst.query(':MEASUrement:IMMed:VALue?'))

    def Autoset(self):
        self.inst.write('autoset EXECUTE')

    # disconnect
    def close(self):
        self.inst.close()
        self.rm.close()
