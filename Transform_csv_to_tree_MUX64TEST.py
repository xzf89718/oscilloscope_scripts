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

import os
import shutil
from glob import iglob


def char_copier(array, str):
    length = len(array)
    if(len(str) >= (length - 1)):
        return False
    else:
        for index, char in enumerate(str):
            array[index:index+1] = bytes(char, "ascii")
        array[index+1:index+2] = b"\x00"
    return True


def bytearrays_withzero(str):

    c_str = bytearray(len(str) + 1)
    char_copier(c_str, str)

    return c_str


parser = argparse.ArgumentParser(
    description="Use this script to transform csv files to TTree. Author: Zifeng XU, email: zifeng.xu@cern.ch")

parser.add_argument("input_prefix", type=str,
                    help="The begin part of the input file name, For example: suppose you have a set of input files named test-CH1-1.csv, the input_file_name is test")
parser.add_argument("--output_dir", type=str,
                    help="The dir save outputs", default="./")
parser.add_argument("--n_max_points", type=int, default=10*24,
                    help="Max save points for one saved waveform")
parser.add_argument("--measuretimes", type=int, default=10)

args = parser.parse_args()
print("All parameters get from commandline are:")
print(args)

n_max_points = args.n_max_points
input_prefix = args.input_prefix
output_dir = args.output_dir
MEASURETIMES = args.measuretimes

iter_inputfiles = iglob(r"{0}".format(input_prefix))
# for index, input_file in enumerate(iter_inputfiles):
#     print("Inputfile {0}: {1}".format(index, input_file))

# hard coded variables
variables = ["Voltage_in", "Current_in", "Voltage_load", "Current_power"]
for input_file in iter_inputfiles:
    input_basename = os.path.basename(input_file)
    input_filename, postfix = input_basename.split(".")
    nametag, channel, temperature, load = input_filename.split("_")
    # Open an outputfile
    output_file = R.TFile.Open("{0}.root".format(
        os.path.join(output_dir, input_filename)), "RECREATE")
    # Create Branches
    ntuple = R.TTree("ntuple", "ntuple for MUX64 test")
    # Global 
    _measuretimes = np.zeros(1, dtype=int)
    _measuretimes[0] = MEASURETIMES
    # Varies by input files
    _nametag = bytearray(n_max_points + 1)
    _channel = np.zeros(1, dtype=int)
    _temperature = np.zeros(1, dtype=float)
    _load = np.zeros(1, dtype=float)

    char_copier(_nametag, nametag)
    _channel[0] = int(channel[1:])
    _temperature[0] = int(temperature[1:])
    # Unit for load is Ohm
    _load[0] = 10 * 1000

    ntuple.Branch("measuretimes", _measuretimes, "measuretimes/I")
    ntuple.Branch("nametag", _nametag,
                  "nametag[{0}]/C".format(n_max_points + 1))
    ntuple.Branch("channel", _channel, "channel/I")
    ntuple.Branch("temperature", _temperature, "temperature/D")
    ntuple.Branch("load", _load, "load/D")
    # hardcoded now, each points test 10 times
    vectors_store_ntuples = {}
    for var in variables:
        vectors_store_ntuples[var] = R.vector('double')(n_max_points)
        ntuple.Branch("{0}".format(var), vectors_store_ntuples[var])
    # Read data from csv files
    dataframe = pd.read_csv(input_file,
                            sep=',', skiprows=5, names=variables)
    for i in range(0, n_max_points):
        for var in variables:
            vectors_store_ntuples[var][i] = dataframe[var][i]
    ntuple.Fill()
    ntuple.Write()
    output_file.Close()
    del ntuple
    for var in variables:
        del vectors_store_ntuples[var]
    print("Transform_csv_to_tree_MUX64TEST.py Finish transform. Outputfile at: {0}.root".format(
        os.path.join(output_dir, input_filename)))
