#! /usr/bin/env python
# Author: Zifeng Xu
# email: zifeng.xu@cern.ch
# Usage: Use this scripts to transform different channels with many output to one TTree
# Use pandas to readcsv file, and them use pyroot to write a tree

import argparse
import ROOT as R
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(
    description="Use this script to transform csv files to TTree. Author: Zifeng XU, email: zifeng.xu@cern.ch")

parser.add_argument("output_filename", type=str,
                    help="Output file name")
parser.add_argument("input_dir", type=str,
                help="dir to input files, for example: ~/inputfiles")
parser.add_argument("--n_save_waveforms", type=int, default=10,
                    help="N_Waveforms save in the output scripts")
parser.add_argument("--save_channels", type=str, default="CH1,CH2",
                    help="Which channel should we save in the scripts? Example: CH1,CH2")
args = parser.parse_args()
print("All parameters get from commandline are:")
print(args)

output_filename = args.output_filename
n_save_waveforms = args.n_save_waveforms
save_channels = args.save_channels
input_dir= args.input_dir


