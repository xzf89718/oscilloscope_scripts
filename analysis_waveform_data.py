#!/usr/bin/env python
# Author: Zifeng Xu
# Email: zifeng.xu@cern.ch
# Usage: Use this interface to get charge and max voltage in waveform


import argparse
import sys

import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
import ROOT

def RunSelector(input_TFile, channels='CH1,CH2,CH3', output_filename='output_filename'):

    list_channel = channels.split(',')

    for _channel in list_channel:
        try:
            tree=input_TFile.Get("tree_waveform_{0}".format(_channel))
        except:
            print("tree_waveform_{0} is not exist".format(_channel))
        tree.Process("single_channel_selector.C+", "{1}_{0}.root".format(_channel, output_filename))

    return 0

def RunAnalysis(channels='CH1,CH2,CH3', input_filename='output_filename', min_trig_level_cut=0.0):

    dic_TFile = {}
    dic_tree = {}
    list_channels = channels.split(',')
    for _channel in list_channels:

        try:
            ROOT.TFile.Open("{0}_{1}.root".format(input_filename, _channel))
        except:
            print("{0}_{1}.root".format(input_filename, _channel))

    # Check the length of these trees

    return 0

 
input_TFile=ROOT.TFile.Open("./waveform_data_root/channel2_trig_n3p00.root", "READ")
RunSelector(input_TFile, "CH1,CH2,CH3", output_filename='channel2_trig_n3p00_cut_charge_n4400_level_n2p68')
# RunAnalysis(channels='CH1,CH2', input_filename='output_filename')
