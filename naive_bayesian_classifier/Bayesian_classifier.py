#!/usr/bin/env python
# Author: Zifeng Xu
# This scripts aim to train the classifier use 7000 data, and use the classifier to predict.
# Also, the confusion matrix.

import ROOT
import numpy as np
# import matplotlib.pyplot as plt
from Event import Event as ev
import os

train_set = 7000
test_set = 3000
# Init all event we need
event_CH1 = ev('../channel2_trig_n3p00_cut_charge_n4400_level_n2p68_CH1.root')
event_CH2 = ev('../channel2_trig_n3p00_cut_charge_n4400_level_n2p68_CH2.root')
event_CH3 = ev('../channel2_trig_n3p00_cut_charge_n4400_level_n2p68_CH3.root')

# Use 0-6999 to learn, use 7000-9999 to test


charge_bin_x = np.array([-4950., -4860., -4845., -4800])
width_binx = np.array([274., 294., 300., 303.])
max_voltage_binx = np.array([-5.5, -2.6, -2.3])
dic_hist = {}
# Train
h_charge_sig = ROOT.TH1F("charge_sig", "charge_sig",
                         len(charge_bin_x) - 1, charge_bin_x)
h_charge_bkg = ROOT.TH1F("charge_bkg", "charge_bkg",
                         len(charge_bin_x) - 1, charge_bin_x)
h_width_sig = ROOT.TH1I("width_sig", "width_sig",
                        len(width_binx)-1, width_binx)
h_width_bkg = ROOT.TH1I("width_bkg", "width_bkg",
                        len(width_binx)-1, width_binx)
h_max_voltage_sig = ROOT.TH1F("max_voltage_sig", "max_voltage_sig", len(
    max_voltage_binx)-1, max_voltage_binx)
h_max_voltage_bkg = ROOT.TH1F("max_voltage_bkg", "max_voltage_bkg", len(
    max_voltage_binx)-1, max_voltage_binx)
dic_hist['bkg'] = {'charge': h_charge_bkg,
                   'width': h_width_bkg, 'max_voltage': h_max_voltage_bkg}
dic_hist['sig'] = {'charge': h_charge_sig,
                   'width': h_width_sig, 'max_voltage': h_max_voltage_sig}
# Use Maximum Likelihood estimate parameters
# Just fill the histogram first
for i in range(0, train_set):
    # GetEntry
    event_CH3.m_tree_event.GetEntry(i)

    # If sig
    if(event_CH3.trig_level[0] == 0):
        h_charge_sig.Fill(event_CH3.charge[0])
        h_width_sig.Fill(event_CH3.width[0])
        h_max_voltage_sig.Fill(event_CH3.max_voltage[0])
    # If bkg
    elif (event_CH3.trig_level[0] == 1):
        h_charge_bkg.Fill(event_CH3.charge[0])
        h_width_bkg.Fill(event_CH3.width[0])
        h_max_voltage_bkg.Fill(event_CH3.max_voltage[0])

dic_canvas = {'bkg': ['charge', 'width', 'max_voltage'],
              'sig': ['charge', 'width', 'max_voltage']}
for key in dic_canvas.keys():
    for variable in dic_canvas[key]:
<<<<<<< HEAD
        _canvas = ROOT.TCanvas("{0}_{1}".format(
            key, variable), "{0}_{1}".format(key, variable).format, 800, 600)
        dic_hist[key][variable].Draw("hist e")
=======
        _canvas=ROOT.TCanvas("{0}_{1}".format(key,variable),"{0}_{1}".format(key,variable),800,600)
        dic_hist[key][variable].Draw("hist e")
        ROOT.gPad.Update()
        _canvas.SaveAs("{0}_{1}.png".format(key,variable))
>>>>>>> 85052588ce911b8a62b1b679376ded6bfac47507
