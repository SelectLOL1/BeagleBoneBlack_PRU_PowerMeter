import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import time
import numpy.polynomial.polynomial as poly
import numpy as np
import math
import rrdtool

start = input('Start of capture,(can be x(seconds)) x is a number.\nEntered number will be subtracted from the now time.\nEnter number:')
end = input('End of capture,(can be x(seconds)) x is a number.\nEntered number will be subtracted from the now time.\nEnter number:')
if int(end) <= 0:
    end = 2
if int(start) <= 0:
    start = 600

epochTimeNow = int(time.time()-1)
data = rrdtool.fetch('powerCapturenew.rrd','AVERAGE',
                     '--start', f'-{start}',
                     '--end',f'-{end}')

values = np.array(data[2])
values[values == None] = 0
epochEndTime = epochTimeNow - int(end)
epochStartTime = epochTimeNow - int(start)
timeseries = np.zeros(shape=((epochEndTime-epochStartTime + 1),1))

for i in range (epochEndTime - epochStartTime + 1):
    timeseries[i] = epochStartTime + i

fig, ax = plt.subplots()
timeseries = mdate.epoch2num(timeseries)
ax.plot_date(timeseries,values, linestyle = '-', marker = '',label=f'AllThePower')
timeseriesFormat = '%d-%m-%y %H:%M:%S'
timeseriesFormatted = mdate.DateFormatter(timeseriesFormat)
ax.xaxis.set_major_formatter(timeseriesFormatted)
fig.autofmt_xdate()
plt.ylim(bottom = 0)
StartTime = time.strftime('%Y-%m-%d [%H:%M:%S]', time.localtime(epochStartTime))
EndTime = time.strftime('%Y-%m-%d [%H:%M:%S]', time.localtime(epochEndTime))

plt.title(f'Time range: {StartTime}    -    {EndTime}')
plt.tight_layout()
plt.legend()
plt.show()
plt.close()


####Fill Bettweeeeennnn?#####
