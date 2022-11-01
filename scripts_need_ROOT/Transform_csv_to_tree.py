#! /usr/bin/env python
# Author: Zifeng Xu
# email: zifeng.xu@cern.ch
# Usage: Use this scripts to transform different channels with many output to one TTree
# Example: python Transform_csv_to_tree.py this_is_an_example.root input_dir input_file_name this_is_an_example --n_save_waveforms 5 --save_channels CH1,CH2 --n_max_points 2000
# Use pandas to readcsv file, and them use pyroot to write a tree

import argparse

import ROOT as R
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(
    description="Use this script to transform csv files to TTree. Author: Zifeng XU, email: zifeng.xu@cern.ch")

parser.add_argument("output_filename", type=str,
                    help="Output file name")
parser.add_argument("input_dir", type=str,
                    help="Dir to input files, for example: ~/inputfiles/")
parser.add_argument("input_file_name", type=str,
                    help="The begin part of the input file name, For example: suppose you have a set of input files named test-CH1-1.csv, the input_file_name is test")
parser.add_argument("--n_save_waveforms", type=int, default=10,
                    help="N_Waveforms save in the output scripts")
parser.add_argument("--save_channels", type=str, default="CH1,CH2",
                    help="Which channel should we save in the scripts? Example: CH1,CH2")
parser.add_argument("--n_max_points", type=int, default=2000,
                    help="Max save points for one saved waveform")

args = parser.parse_args()
print("All parameters get from commandline are:")
print(args)

output_filename = args.output_filename
input_dir = args.input_dir
input_file_name = args.input_file_name
n_save_waveforms = args.n_save_waveforms
save_channels = args.save_channels
n_max_points = args.n_max_points

# Open a TFile to save TTrees
file_output = R.TFile.Open("{0}".format(output_filename), "RECREATE")
# Open a TFile to save TTree
dic_trees = {}
dic_arrays = {}
for channel in save_channels.split(","):
    dic_trees[channel] = R.TTree(
        "tree_waveform_{0}".format(channel), "A tree save channel {0} wave form data and size of each measurment".format(channel))
    dic_arrays["{0}_size".format(channel)] = np.zeros(1, dtype=int)
    dic_arrays["{0}_time".format(channel)] = np.zeros(
        n_max_points, dtype=float)
    dic_arrays["{0}_voltage".format(channel)] = np.zeros(
        n_max_points, dtype=float)
    dic_trees[channel].Branch("size".format(
        channel), dic_arrays["{0}_size".format(channel)], "size/I".format(channel))
    dic_trees[channel].Branch("time".format(channel), dic_arrays["{0}_time".format(
        channel)], "time[{1}]/D".format(channel, str(n_max_points)))
    dic_trees[channel].Branch("voltage".format(
        channel), dic_arrays["{0}_voltage".format(channel)], "voltage[{1}]/D".format(channel, str(n_max_points)))
for channel in save_channels.split(","):
    dic_trees[channel].Print()
    dic_trees[channel].Show()
# Loop over all inputfiles
for n_waveform in range(0, n_save_waveforms):
    # Loop all channels
    for channel in save_channels.split(","):
        # Use pandas to open the file
        df_inputfile = pd.read_csv("{0}{1}-{2}-{3}.csv".format(
            input_dir, input_file_name, channel, str(n_waveform)), sep=",")
        # print("DEBUG {0}".format(str(df_inputfile)))
        # print(df_inputfile)
        # TODO: check if NaN exist in the file, if exist ,warning and change the Nan to 0.0
        i = 0
        # Save max to n_max_points points, or just the len(df_inputfile[used_colums[0]])points
        if(len(df_inputfile['scaled_time']) <= n_max_points):
            length_to_save = len(df_inputfile['scaled_time'])
        else:
            print("WARNING The lenght of colums in data is larger than the n_max_points, you may miss some data points now!")
            length_to_save = n_max_points
        # print("DEBUG length to save is {0}".format(str(length_to_save)))
        dic_arrays["{0}_size".format(channel)][0] = length_to_save
        # Copy the data one by one to the
        while i < length_to_save:
            dic_arrays["{0}_time".format(
                channel)][i] = df_inputfile['scaled_time'][i]
            dic_arrays["{0}_voltage".format(
                channel)][i] = df_inputfile['scaled_voltage'][i]
            i = i+1
        # print("DEBUG ",end="")
        # print(dic_arrays["{0}_time".format(
        #         channel)])
        # print("DEBUG ",end="")
        # print(dic_arrays["{0}_voltage".format(
        #         channel)])
        dic_trees[channel].Fill()
        print("INFO Fill tree for " + "{0}{1}-{2}-{3}.csv".format(
            input_dir, input_file_name, channel, str(n_waveform)))

file_output.cd()
# Write all the trees into TFile
for channel in save_channels.split(","):
    dic_trees[channel].Write()
    print("INFO Write tree for {0}, totally n_files is {1}".format(
        channel, n_save_waveforms))
file_output.Close()
print("INFO Finish all jobs")
