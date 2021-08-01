#!/usr/bin/env python
# Author: Zifeng Xu
# Email: zifeng.xu@cern.ch
# Usage: Use this script to draw charge and max voltage in waveform
# Example: python Plot_waveform_from_root.py this_is_an_example.root --n_plot_waveforms 10 --plot_channels CH1,CH2,CH3 --save_names this_is_an_example
import argparse
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
        self.entry = 0
        self.list_channels = list_channels
        self.__input_filename = input_filename
        self.__input_TFile = ROOT.TFile.Open(input_filename)
        self.dic_tree = {}
        self.dic_waveform_one_channel = {}
        for _channel in self.list_channels.split(','):
            self.dic_tree[_channel] = self.__input_TFile.Get(
                "tree_waveform_{0}".format(_channel))
            self.dic_waveform_one_channel[_channel] = Waveform_one_channel()
            self.dic_tree[_channel].SetBranchAddress(
                "size", self.dic_waveform_one_channel[_channel].size)
            self.dic_tree[_channel].SetBranchAddress(
                "time", self.dic_waveform_one_channel[_channel].time)
            self.dic_tree[_channel].SetBranchAddress(
                "voltage", self.dic_waveform_one_channel[_channel].voltage)

    def my_GetEntry(self, i_entry):
        for _channel in self.list_channels.split(','):
            self.dic_tree[_channel].GetEntry(i_entry)

        self.entry = i_entry

    def Plot_this_entry(self, save_name):
        for _channel in self.list_channels.split(','):
            plt.plot(
                self.dic_waveform_one_channel[_channel].time[:
                                                             self.dic_waveform_one_channel[_channel].size[0]],
                self.dic_waveform_one_channel[_channel].voltage[:
                                                                self.dic_waveform_one_channel[_channel].size[0]],
                label=_channel)
        plt.legend()
        plt.savefig(save_name)
        plt.close()
        # plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Use this script to plot some waveform figure. Author: Zifeng XU, email: zifeng.xu@cern.ch")

    parser.add_argument("input_rootfile", type=str,
                        help="Input root file. Please include full path to the file")
    parser.add_argument("index_you_want_to_plot", type=int,
                        help="Which one you want to plot")
    parser.add_argument("--n_plot_waveforms", type=int, default=10,
                        help="N_Waveforms save in the output scripts")
    parser.add_argument("--plot_channels", type=str, default="CH1,CH2,CH3",
                        help="Which channel should we save in the scripts? Example: CH1,CH2,CH3")
    parser.add_argument("--save_name", type=str, default='waveform_plot',
                        help="header of saved figures")

    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    input_rootfile = args.input_rootfile
    index_you_want_to_plot = args.index_you_want_to_plot
    n_plot_waveforms = args.n_plot_waveforms
    plot_channels = args.plot_channels
    save_name = args.save_name

    # Init
    my_tree_waveforms = Tree_waveform(
        input_filename=input_rootfile, list_channels=plot_channels)
    for i in range(index_you_want_to_plot, index_you_want_to_plot+n_plot_waveforms):
        my_tree_waveforms.my_GetEntry(i)
        my_tree_waveforms.Plot_this_entry(
            save_name='{0}-{1}.png'.format(save_name, str(i)))
