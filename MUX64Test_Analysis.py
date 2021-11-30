import atlasplots as aplt
import ROOT as R

import numpy as np

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


aplt.set_atlas_style()
goodchannels = R.TChain("goodchannels")
goodchannels.Add("output.root")
good_entries = goodchannels.GetEntries()
good_entry = 0

badchannels = R.TChain("badchannels")
badchannels.Add("output.root")
bad_entries = badchannels.GetEntries()
bad_entry = 0

while (good_entry < good_entries):
    goodchannels.GetEntry(good_entry)
    # Fill your cut here
    # if (goodchannels.nametag == "B1C30"):
    #     print(goodchannels.max_resistance_error)
    #     print("channel is:")
    #     print(goodchannels.channel)
    good_entry = good_entry + 1


print("Here're bad channels:")
while (bad_entry < bad_entries):
    badchannels.GetEntry(bad_entry)
    # Fill your cut here
    # if (badchannels.max_resistance_error > 0.1 or badchannels.max_resistance > 1000 or badchannels.min_resistance < 0):
    print("nametag: {0} channel: {1} error: {2} max_resistance: {3} min_resistance: {4}".format(badchannels.nametag, badchannels.channel, badchannels.max_resistance_error, badchannels.max_resistance, badchannels.min_resistance))
    bad_entry = bad_entry + 1


