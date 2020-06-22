import time
import socket
import numpy as np
from bbb_pru_adc import capture

gainOfClamp = (1/0.0497)
ADCnoiseCorrectioninW = 4
sampleCount = 26
bufferCount = 500
channelSelect = [0,1,2,3,4,5,6]
sampleCount = sampleCount * len(channelSelect)
mybufferseries = np.zeros((bufferCount*sampleCount), dtype=np.float32)
power = np.zeros(len(channelSelect), dtype=object)
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

    def PowerCalculation(self, FilteredValue, Samples, channel):
        Samples = np.delete(Samples, len(Samples)-1)
        Wattsec =((np.sqrt(np.mean(np.square(Samples - FilteredValue)))) * gainOfClamp) * mainsVoltage
        Wattsec = Wattsec - ADCnoiseCorrectioninW
        #Wattsec = Wattsec * (((sampleCount * bufferCount) / (300 * 50 * len(channelSelect)))) Should not be needed~
        Wattsec = f'CH{channel}:'+(str(round(Wattsec, 2)))+':'
        return Wattsec

    def WriteToDatabase(self, Wattsec):
        try:
            self.s.send(Wattsec.encode())
            print(''.join(power))
        except BrokenPipeError:
            print('Server Lit On Fire, reconnecting...')
            self.s = socket.socket()
            self.ConnectToServer()
        except ConnectionResetError:
            time.sleep(1)
            self.s = socket.socket()
            self.ConnectToServer()
            print('Connection To Server Failed, retrying...')

    def ConnectToServer(self):
        try:
            time.sleep(1)
            self.s.connect(('10.10.32.252', 12348))
            print('Connected Successfully')
        except ConnectionRefusedError:
            time.sleep(1)
            print('Connection To Server Failed, retrying...')
        except BrokenPipeError:
            time.sleep(1)
            print('Connection To Server Failed, retrying...')
        except ConnectionResetError:
            time.sleep(1)
            print('Connection To Server Failed, retrying...')


CoolClass = MyCoolClass()
CoolClass.ConnectToServer()

def measure():
    with capture.capture(clk_div=0, step_avg=0, channels=[0,1,2,3,4,5,6],
                         max_num=int((sampleCount/len(channelSelect))),
                         auto_install=False) as adcValues:
        for index, (numberDropped, timestamps, values) in enumerate(adcValues):
            mybufferseries[index*sampleCount:index*sampleCount + sampleCount] = (np.frombuffer(values, dtype='float32'))
            if index == bufferCount - 1:
                break
    for i in range(len(channelSelect)):
        filteredSamples = CoolClass.LowpassFiltering(mybufferseries[i::len(channelSelect)])
        power[i] = CoolClass.PowerCalculation(filteredSamples, mybufferseries[i::len(channelSelect)], i)
    CoolClass.WriteToDatabase(''.join(power))

while 1:
    measure()
