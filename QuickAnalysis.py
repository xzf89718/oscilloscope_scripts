# Author: Zifeng Xu
# Usage: Provide a full python analysis skeleton to analyze the data which taken from the cosmic ray muon detection experiment
# Dependencies: python 3.6+, numpy matplotlib pandas

import argparse

# In order to use ndarray
import numpy as np 
# In order to read data from csv
import pandas as pd
# In order to make simple histograms
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# Analysis Base class
class QuickAnalysisBase(object):

    def __init__(self):
        pass
    
    def Initialize(self):
        pass

    def Begin(self):
        pass

    def Process(self):
        pass

    def Terminate(self):

        self.QuickResult()
        self.QuickHist()

        return True

    def RunAnalysis(self):
        self.Initialize()
        self.Begin()
        self.Process()
        self.Terminate()

        return True
    def QuickHist(self):
        pass

    def QuickResult(self):
        pass

    def BookAnalysis(self):
        pass

    def DoOneAnalysis(self):
        pass

class QuickAnalysis_Zifeng(object):

    pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

