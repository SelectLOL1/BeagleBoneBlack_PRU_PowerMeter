import time
import numpy as np
import rrdtool
from bbb_pru_adc import capture
import socket

gainOfClamp = (1/0.0497)
ADCnoiseCorrectioninW = 4
sampleCount = 75
bufferCount = 45
mybufferseries = np.zeros((bufferCount*sampleCount), dtype=np.float32)
mainsVoltage = 230

class MyCoolClass:
    def __init__(self):
        self.FilteredValue = np.zeros(bufferCount*sampleCount)
        self.FilteredValue[0] = 0.8345
        self.LastFiltered = 0.8345
        self.s = socket.socket()

    def LowpassFiltering(self, Samples):
        self.FilteredValue = (self.LastFiltered) + np.cumsum(np.diff(Samples) * 0.0004)
        self.LastFiltered = self.FilteredValue[-1]
        return self.FilteredValue

    def PowerCalculation(self, FilteredValue, Samples):
        Samples = np.delete(Samples, len(Samples)-1)
        Wattsec =((np.sqrt(np.mean(np.square(Samples - FilteredValue)))) * gainOfClamp) * mainsVoltage
        Wattsec = Wattsec - ADCnoiseCorrectioninW
        Wattsec = Wattsec * (1/(50/bufferCount))
        return Wattsec

    def WriteToDatabase(self, Wattsec):
        #rrdtool.update("powerCapturenew.rrd", 'N:' + (str(round(Wattsec, 2))))
        Wattsec = 'N:'+(str(round(Wattsec, 2)))
        try:
            self.s.send(Wattsec.encode())
        except BrokenPipeError:
            print('Server Lit On Fire, reconnecting...')
            self.s = socket.socket()
            self.ConnectToServer()
    def ConnectToServer(self):
        try:
            time.sleep(1)
            self.s.connect(('10.10.32.252', 12348))
            print('Connected Successfully')
        except ConnectionRefusedError:
            time.sleep(1)
            print('Connection To Server Failed')


CoolClass = MyCoolClass()

CoolClass.ConnectToServer()

def measure():
    with capture.capture(clk_div=2, step_avg = 3, channels=[0],
                         max_num = sampleCount, auto_install=False) as adcValues:
        for index, (numberDropped, timestamps, values) in enumerate(adcValues):
            mybufferseries[index*sampleCount:index*sampleCount + sampleCount] = (np.frombuffer(values, dtype='float32'))
            if index == bufferCount - 1:
                break
    filteredSamples = CoolClass.LowpassFiltering(mybufferseries)
    power = CoolClass.PowerCalculation(filteredSamples, mybufferseries)
    CoolClass.WriteToDatabase(power)

while 1:
    measure()
