from Oscilloscope import Oscilloscope, WriteToCsv
import pyvisa
import time

import numpy as np
import matplotlib.pyplot as plt

for i in range(0,10):
    Scope=Oscilloscope()
    wavetime, waveform=Scope.Sampling("CH1,CH2")
    print("time: {0}\nwaveform: {1}".format(wavetime, waveform))
    WriteToCsv("test-CH1-{0}.csv".format(str(i)), wavetime['CH1'], waveform['CH1'])
    # plt.plot(wavetime,waveform)
    # plt.show()
    time.sleep(0.5)