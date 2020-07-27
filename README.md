# Power Consumption Visualization

**Using a BeagleBoneBlack and Non-Invasive current calmps to monitor the power consumption.**

# Usage

Only the files in the `allChannelSampling` folder will be needed for the final usage case.

## Client Side

The Client in this context is the BeagleBone. The BeagleBone is sampling, filtering and calculationg for every channel. In the end it will send a string containing the Channel number and its Value in Watts over a socket. (allChannelSampling/sevenChannelSampler.py for all channels)

## Server Side

The Server Side keeps the RRD Files and evaluetes the string from the client and writes the values into the corresponding RRD File. (allChannelSampling/rrdServerReadAndWrite.py for all channels)

## Imports

Besides Python3, this must be installed for the usage of the scripts.

[RRDtool](https://pypi.org/project/rrdtool/)


```python
#########################CLIENT#########################
import time #Standard import
import socket #Socket for data exchange
import numpy as np #Standard import
import from bbb_pru_adc import capture #PRU Control for ADC
#########################SERVER#########################
import socket #Socket for data exchange
import rrdtool #RRDtool for the Database
import time #Standard import
import os #To clear STDOUT
import re #Regexp for filtering incoming data
```

## Visualization

To visulize the data Matplotlib.pyplot can be used. Examples in /RRDGraphs/*

## Measurment Reports
--
## License

[Terms](https://de-de.facebook.com/terms)

#BCA was here#