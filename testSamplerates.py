import time
import numpy as np
import rrdtool
from bbb_pru_adc import capture
import matplotlib.pyplot as plt

Combinations=[(3,2,73,3),#AVG,DIV,SAMPLE,BUFFER
              (0,0,75,12),
              (3,0,41,15),
              (0,2,38,9),
              (3,3,54,3),
              (2,3,69,3),
              (3,4,43,3),
              (3,5,36,3)]

AmountOfMeasurments = len(Combinations)

for i in range(AmountOfMeasurments):
    mybufferseries = np.zeros((Combinations[i][2] * Combinations[i][3]), dtype=np.float32)
    with capture.capture(clk_div=Combinations[i][1], step_avg = Combinations[i][0], channels=[0],max_num = Combinations[i][2], auto_install=False) as adcValues:
        for index, (numberDropped, timestamps, values) in enumerate(adcValues):
            mybufferseries[index*Combinations[i][2]:index*Combinations[i][2] + Combinations[i][2]] = (np.frombuffer(values, dtype='float32'))
            if index == Combinations[i][3] - 1:
                FilteredValue = np.zeros(Combinations[i][2] * Combinations[i][3])
                FilteredValue[0] = 0.8345
                LastFiltered = 0.8345
                Samples = mybufferseries
                FilteredValue = (LastFiltered) + np.cumsum(np.diff(Samples) * 0.0004)
                LastFiltered = FilteredValue[-1]
                Samples = np.delete(Samples, len(Samples)-1)
                Samples = Samples - FilteredValue
                plt.plot(Samples, '-o', label='Signal')
                plt.title(f'AVG_{Combinations[i][0]}_DIV_{Combinations[i][1]} ({Combinations[i][2] * Combinations[i][3]} Samples), RMSvalue={((np.sqrt(np.mean(np.square(Samples)))))}')
                plt.savefig(f'AVG_{Combinations[i][0]}_DIV_{Combinations[i][1]}')
                plt.close()
                np.delete(mybufferseries,np.arange(len(mybufferseries)))
                print(f'Done with {i}')
                break
