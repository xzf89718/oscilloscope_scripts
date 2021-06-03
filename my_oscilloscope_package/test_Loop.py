from weakref import WeakValueDictionary
from Oscilloscope import Oscilloscope
import pyvisa
import time

import numpy as np
import matplotlib.pyplot as plt

for i in range(0,10):
    Scope=Oscilloscope()
    wavetime, waveform=Scope.Sampling("CH1,CH2,CH3")
    print("time: {0}\nwaveform: {1}".format(wavetime, waveform))
    # plt.plot(wavetime,waveform)
    # plt.show()
    time.sleep(0.5)