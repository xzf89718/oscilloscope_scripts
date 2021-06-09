#!/usr/bin/env python
# Author: Zifeng Xu
# Email: zifeng.xu@cern.ch
# Usage: Use this interface to get charge and max voltage in waveform

import numpy as np
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

    dic_tree = {}
    try:
        ROOT.TFile.Open("".format())
    except:
        print("hello")
    # Check the length of these trees

    return 0

input_TFile=ROOT.TFile.Open("channel1_trig_n4p00.root", "READ")

RunSelector(input_TFile, "CH1,CH2,CH3", output_filename='channel1_trig_n4p00')
# RunAnalysis(channels='CH1,CH2', input_filename='output_filename')