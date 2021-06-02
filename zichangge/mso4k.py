#!/usr/bin/python
# This is mso4k.py file
# author: zicg@ihep.ac.cn
# 2021-05-24 created

import time
import pyvisa
import matplotlib.pyplot as plt
import numpy as np

class mso4k():
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.scope = self.rm.open_resource('TCPIP0::192.168.10.20::inst0::INSTR')
        self.scope.timeout = 10000 # ms
        self.scope.encoding = 'latin_1'
        self.scope.read_termination = '\n'
        self.scope.write_termination = None
        self.scope.write('*cls') # clear ESR
        self.scope.write('header OFF') # disable attribute echo in replies
        #print(self.scope.query('*idn?'))

    def Sampling(self, M = 8192):     #M is the number of sampling points
        # default setup
        self.scope.write('*rst')
        #t1 = time.perf_counter()
        r = self.scope.query('*opc?') # sync
        #t2 = time.perf_counter()
        #print('reset time: {} s'.format(t2 - t1))

        # autoset
        self.scope.write('autoset EXECUTE')
        #t3 = time.perf_counter()
        r = self.scope.query('*opc?')
        #t4 = time.perf_counter()
        #print('autoset time: {} s'.format(t4 - t3))

        # acquisition
        self.scope.write('acquire:state OFF') # stop
        self.scope.write('acquire:stopafter SEQUENCE;state ON') # single
        #t5 = time.perf_counter()
        r = self.scope.query('*opc?')
        #t6 = time.perf_counter()
        #print('acquire time: {} s'.format(t6 - t5))

        # curve configuration
        self.scope.write('data:encdg SRIBINARY') # signed integer
        self.scope.write('data:source CH1')
        self.scope.write('data:start 1')
        acq_record = int(M)      #self.scope.query('horizontal:recordlength?')
        self.scope.write('data:stop {}'.format(acq_record))
        self.scope.write('wfmoutpre:byt_nr 1') # 1 byte per sample

        # data query
        #t7 = time.perf_counter()
        bin_wave = self.scope.query_binary_values('curve?', datatype='b', container=np.array)
        #t8 = time.perf_counter()
        #print('transfer time: {} s'.format(t8 - t7))

        # retrieve scaling factors
        wfm_record = int(self.scope.query('wfmoutpre:nr_pt?'))
        pre_trig_record = int(self.scope.query('wfmoutpre:pt_off?'))
        t_scale = float(self.scope.query('wfmoutpre:xincr?'))
        t_sub = float(self.scope.query('wfmoutpre:xzero?')) # sub-sample trigger correction
        v_scale = float(self.scope.query('wfmoutpre:ymult?')) # volts / level
        v_off = float(self.scope.query('wfmoutpre:yzero?')) # reference voltage
        v_pos = float(self.scope.query('wfmoutpre:yoff?')) # reference position (level)

        # error checking
        r = int(self.scope.query('*esr?'))
        #print('event status register: 0b{:08b}'.format(r))
        r = self.scope.query('allev?').strip()
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
        self.scope.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.scope.write(':MEASUrement:IMMed:TYPe FREQuency')
        return (self.scope.query(':MEASUrement:IMMed:VALue?'))

    def MeasureAmpl(self):    #MEASUre Amplitude
        self.scope.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.scope.write(':MEASUrement:IMMed:TYPe AMPlitude')
        return (self.scope.query(':MEASUrement:IMMed:VALue?'))

    def MeasureHigh(self):    #MEASUre Low
        self.scope.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.scope.write(':MEASUrement:IMMed:TYPe HIGH')
        return (self.scope.query(':MEASUrement:IMMed:VALue?'))

    def MeasureLow(self):    #MEASUre Low
        self.scope.write(':MEASUrement:IMMed:SOUrce1 CH1')
        self.scope.write(':MEASUrement:IMMed:TYPe LOW')
        return (self.scope.query(':MEASUrement:IMMed:VALue?'))

    def Autoset(self):
        self.scope.write('autoset EXECUTE')

    # disconnect
    def close(self):
        self.scope.close()
        self.rm.close()
