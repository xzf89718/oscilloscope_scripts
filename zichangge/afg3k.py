#!/usr/bin/python
# This is afg3k.py file
# author: zicg@ihep.ac.cn
# 2021-05-24 created
import pyvisa

class afg3k():
    def __init__(self, tcpip = '192.168.10.10'):
        self.rm = pyvisa.ResourceManager()      #打开visa的资源管理器实例化
        self.afg = self.rm.open_resource('TCPIP0::192.168.10.10::inst0::INSTR')
        #print(self.afg.query("*IDN?")) #Who are you?
        self.afg.write("*CLS")         #clear the AFG status

    def setShape(self, shape, ch = 1):
        self.afg.write('SOURce'+str(ch)+':FUNCtion:SHAPe '+str(shape) )

    def setHighVoltage(self, highvoltage, ch = 1):
        self.afg.write('SOURce'+str(ch)+':VOLTage:LEVel:IMMediate:HIGH '+str(highvoltage)+'mV')

    def setLowVoltage(self, lowvoltage, ch = 1):
        self.afg.write('SOURce'+str(ch)+':VOLTage:LEVel:IMMediate:LOW '+str(lowvoltage)+'mV')

    def setOffsetVoltage(self, offset, ch = 1):
        self.afg.write('SOURce'+str(ch)+':VOlTage:LEVel:IMMediate:OFFSet '+str(offset)+'mV')

    def setAmplitude(self, amplitude, ch = 1):
        self.afg.write('SOURce'+str(ch)+':VOlTage:LEVel:IMMediate:AMPLitude '+str(amplitude)+'mV')

    def setOutput(self, on = 1, ch = 1):
        if on:
            self.afg.write('OUTPut'+str(ch)+':STATe on')
        else:
            self.afg.write('OUTPut'+str(ch)+':STATe off')

    def setFrequency(self, frequency, ch = 1):
        self.afg.write('SOURce'+str(ch)+':FREQuency:FIXed '+str(frequency)+'Hz')

    def close(self):
        self.rm.close()

'''myafg = afg3k()
myafg.setShape('DC')
myafg.setOffsetVoltage(200)
myafg.setOutput(1)
myafg.close()'''