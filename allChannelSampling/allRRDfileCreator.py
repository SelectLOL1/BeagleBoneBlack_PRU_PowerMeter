import rrdtool

for i in range(7):
    rrdtool.create(
        f"powerCapture{i}.rrd",
        "--start", "NOW",
        "--step", "1s",
        "DS:PowerCapture:GAUGE:60:-100000:3000000",
        "RRA:AVERAGE:0.5:1s:10d",
        "RRA:AVERAGE:0.5:30s:90d",
        "RRA:AVERAGE:0.5:5m:1y",
        "RRA:AVERAGE:0.5:30m:3y",
        "RRA:AVERAGE:0.5:1h:5y",
        "RRA:AVERAGE:0.5:3h:10y")
