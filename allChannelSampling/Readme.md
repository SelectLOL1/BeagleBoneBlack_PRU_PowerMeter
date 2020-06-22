The file `allChannelGraph` lets you choose a channel and a timeframe thats should be analyzed.
It will plot the values and save a plot with the timeframe and channel as the name to the
same directory as the script.

The file `allRRDfileCreator.py` creates 7 RRDdatabases for each Channel one.
This file has ONLY to be excuted once, or all existing information will be overwritten.

The file `sevenChannelSampler.py` samples all the channels for close to a second,
calculates many things, filters values, removes offsets and finnely sends the values
to the server over sockets.

The file `rrdServerReadAndWrite.py` gets values from the Client over sockets
and then parses and writes the values to the corresponding RRDfile.

