import time
import matplotlib.pyplot as plt
import numpy as np

from afg3k import afg3k
from mso4k import mso4k

myafg = afg3k()
myafg.setShape('DC')
myafg.setOffsetVoltage(0)
myafg.setOutput(1)
myafg.close()

step = 100
M = int(1200/step +1)
vin=np.linspace(0,1200,M)

vout = np.arange(M)
i = 0
while i < M:
    myafg = afg3k()
    myafg.setOffsetVoltage(vin[i])
    myafg.close()
    time.sleep(2)

    myosp = mso4k()
    myosp.Autoset()
    time.sleep(2)
    low = myosp.MeasureLow()
    high = myosp.MeasureHigh()
    myosp.close()
    vout[i]= (float(low)+float(high))*250       #250 = 1/2*1000/2
    i = i + 1

vout_step = np.arange(M-1)
j = 0
while j < M - 1:
    vout_step[j] =  vout[j+1] - vout[j]
    j = j + 1

step_mean = np.mean(vout_step)
step_diff = vout_step - step_mean
step_diff_abs = np.abs(step_diff)
DNL = max(step_diff_abs)/step_mean

print('vin: {} mv'.format(vin))
print('vout: {} mv'.format(vout))
print("--------------------------------")

print('vout step: {} mv'.format(vout_step))
print('vout step mean: {} mv'.format(step_mean))
print('step diff: {} mv'.format(step_diff))
print('abs of step diff: {} mv'.format(step_diff_abs))
print('DNL: {} '.format(DNL))
print("--------------------------------")

diff = vout - vin
diff_abs = np.abs(diff)
INL = max(diff_abs)/1200

print('diff between vout with vin: {} mv'.format(diff))
print('abs of diff between vout with vin: {} mv'.format(diff_abs))
print('INL: {} '.format(INL))