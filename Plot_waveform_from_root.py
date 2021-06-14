#!/usr/bin/env python
# Author: Zifeng Xu
# Email: zifeng.xu@cern.ch
# Usage: Use this script to draw charge and max voltage in waveform

import matplotlib.pyplot as plt
import ROOT
import numpy as np
import matplotlib
matplotlib.use("TkAgg")


class Waveform_one_channel():
    def __init__(self) -> None:
        self.size = np.zeros(1, dtype=int)
        self.time = np.zeros(5000, dtype=float)
        self.voltage = np.zeros(5000, dtype=float)


class Tree_waveform():

    def __init__(self, input_filename, list_channels) -> None:
        self.entry=0
        self.list_channels = list_channels
        self.__input_filename=input_filename
        self.__input_TFile = ROOT.TFile.Open(input_filename)
        self.dic_tree = {}
        self.dic_waveform_one_channel = {}
        for _channel in self.list_channels.split(','):
            self.dic_tree[_channel] = self.__input_TFile.Get(
                "tree_waveform_{0}".format(_channel))
            self.dic_waveform_one_channel[_channel] = Waveform_one_channel()
            self.dic_tree[_channel].AddBranchAddress(
                "size", self.dic_waveform_one_channel[_channel].size)
            self.dic_tree[_channel].AddBranchAddress(
                "time", self.dic_waveform_one_channel[_channel].time)
            self.dic_tree[_channel].AddBranchAddress(
                "voltage", self.dic_waveform_one_channel[_channel].voltage)

    def my_GetEntry(self, i_entry):
        for _channel in self.list_channels.split(','):
            self.dic_tree[_channel].GetEntry(i_entry)

        self.entry=i_entry

    def Plot_this_entry(self):
        for _channel in self.list_channels.split(','):
            plt.plot(
                self.dic_waveform_one_channel[_channel].time[:
                                                             self.dic_waveform_one_channel[_channel].size],
                self.dic_waveform_one_channel[_channel].voltage[:
                                                                self.dic_waveform_one_channel[_channel].size],
                label=_channel)
        plt.legend()
        # plt.savefig('{0}-{1}.png'.format(str(self.entry), self.__input_filename))
        plt.show()
