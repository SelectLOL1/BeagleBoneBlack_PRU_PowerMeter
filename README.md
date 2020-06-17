# Espros Power Consumption Visualization
#### ![Logo](https://www.espros.com/wp-content/uploads/2016/11/epc_logo_250x125.jpg")

**Using a BeagleBoneBlack and Non-Invasive current calmps to monitor the power consumption of different parts of the Building.**

# Usage

## Client Side

The Client in this context is the BeagleBone. The BeagleBone is sampling, filtering and calculationg for every channel. In the end it will send a string containing the Channel number and its Value in Watts over a socket. (allChannelSampling/sevenChannelSampler.py for all channels)

## Server Side

The Server Side keeps the RRD Files and evaluetes the string from the client and writes the values into the corresponding RRD File. (allChannelSampling/rrdServerReadAndWrite.py for all channels)

## Imports

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

## License

[Terms](https://de-de.facebook.com/terms)

#BCA was here#