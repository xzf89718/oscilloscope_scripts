#!/usr/bin/env python
# Author: Zifeng Xu
# This is a container class for a .root file derive from single_channel_selector.C

import ROOT
import numpy as np
# import matplotlib.pyplot as plt


class Event():

    def __init__(self, input_TFile) -> None:

        self.__input_TFile = ROOT.TFile.Open(input_TFile, "READ")
        self.m_tree_event = self.__input_TFile.Get("event")
        self.entries = self.m_tree_event.GetEntries()

        self.max_voltage = np.zeros(1, dtype=float)
        self.width = np.zeros(1, dtype=int)
        self.charge = np.zeros(1, dtype=float)
        self.trig_charge = np.zeros(1, dtype=int)
        self.pass_width = np.zeros(1, dtype=int)
        self.trig_level = np.zeros(1, dtype=int)
        self.__m_dic_branches= {}
        # Add branch address here
        self.SetBranchAddress()

    def SetBranchAddress(self):
        """
        Add Branch Address for all branch
        """
        self.__m_dic_branches['max_voltage']=self.m_tree_event.SetBranchAddress("max_voltage", self.max_voltage)
        self.__m_dic_branches['width']=self.m_tree_event.SetBranchAddress('width',self.width)
        self.__m_dic_branches['charge']=self.m_tree_event.SetBranchAddress('charge',self.charge)
        self.__m_dic_branches['trig_charge']=self.m_tree_event.SetBranchAddress('trig_charge',self.trig_charge)
        self.__m_dic_branches['pass_width']=self.m_tree_event.SetBranchAddress('pass_width',self.pass_width)
        self.__m_dic_branches['trig_level']=self.m_tree_event.SetBranchAddress('trig_level',self.trig_level)

