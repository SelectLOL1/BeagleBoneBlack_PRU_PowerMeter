import math
import time
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy.polynomial.polynomial as poly
import numpy as np
import rrdtool

os.system('clear')
select = input('#Which Channel should be analyzed? \nOptions:0, 1, 2, 3, 4, 5, 6. Please enter only the Number: ')

start = input('\n#Start of capture, amount of time to look in to the past. \n' +
              'Options:1h, 5h, 1d, 5d, 2w, 1M, 3M, 8M, 1y, 2y, 4y, 8y \n' +
              'Or any given amount of seconds. Written like XXXXs: ')

end = input('\n#End of capture, amount of time to look from the past to present or past. \n' +
            'Options:2s, 1h, 5h, 1d, 5d, 2w, 1M, 3M, 8M, 1y, 2y, 4y, 8y \n' +
            'Or any given amount of seconds. Written like XXXXs: ')


if 's' in start:
    if int(start[0:len(start)-1]) <= 1:
        start = '2s'
if start == '0':
    start = '86400s'

if 's' in end:
    if int(end[0:len(end)-1]) <= 1:
        end = '86400s'
if end == '0':
    end = '2s'

epochTimeNow = int(time.time()-1)
data = rrdtool.fetch(f'powerCapture{select}.rrd','AVERAGE',
                     '--start', f'-{start}',
                     '--end',f'-{end}')

factors = {'s': 1,
           'h': 3600,
           'd': 86400,
           'w': 604800,
           'M': 2592000,
           'y': 31536000}

for name, factor in factors.items():
    if name in start:
        startInSecond = int(start[:len(start)-1]) * factor
    if name in end:
        endInSecond = int(end[:len(end)-1]) * factor

values = np.array(data[2])
values[values == None] = 0
values = values.flatten()

integValues = np.cumsum(values)
integValues = ((integValues/1000)/3600)

epochEndTime = epochTimeNow - endInSecond
epochStartTime = epochTimeNow - startInSecond
timeseries = np.zeros(shape=((epochEndTime-epochStartTime + 1),1))

for i in range (epochEndTime - epochStartTime + 1):
    timeseries[i] = epochStartTime + 7200  + i

fig, axes = plt.subplots(2, sharex=True, figsize =(11.65, 8.25))
ax0, ax1 = axes.ravel()
timeseries = mdate.epoch2num(timeseries)

ax0.plot_date(timeseries,integValues, linestyle = '-', marker = '')
timeseriesFormatted = mdate.DateFormatter('%Y:%m:%d %h:%m:%s')
ax0.xaxis.set_major_formatter(timeseriesFormatted)
ax0.set_ylabel('kW/h')

StartTime = time.strftime('%Y-%m-%d [%H:%M:%S]', time.localtime(epochStartTime))
EndTime = time.strftime('%Y-%m-%d [%H:%M:%S]', time.localtime(epochEndTime))
ax0.set_title(f'Time range: {StartTime}    -    {EndTime}')

StartTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(epochStartTime))
EndTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(epochEndTime))
ax1.plot_date(timeseries,values, linestyle = '-', marker = '',label=f'Label')
ax1.set_ylabel('Watt')

ax1.set_ylim(bottom = 0)
ax0.set_ylim(bottom = 0)
fig.autofmt_xdate()
fig.tight_layout()


plt.savefig(f'Channel_{select}_{StartTime}_{EndTime}')
plt.legend()
plt.show()
plt.close()
