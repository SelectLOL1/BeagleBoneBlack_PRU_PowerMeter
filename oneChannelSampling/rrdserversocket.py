import socket
import rrdtool
import time
import os
#server#

s = socket.socket()
port = 12348
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
def mySocket():
    s.listen(1)
    c, addr = s.accept()
    print ("Socket Up and running with a connection from",addr)
    while True:
        rcvdData = c.recv(1024).decode()
        if not 'N:' in rcvdData:
            c.close()
            time.sleep(0.2)
            break
        rrdtool.update("powerCapturenew.rrd", rcvdData)
        rrdtool.graph("mypicreon.png",
                      "--title",f"Power Consumption = {rcvdData}",
                      "--vertical-label", "Wattseconds",
                      "--start", "NOW-24h", "--end", "NOW",
                      "--color","BACK#007733AB",
                      "--color","CANVAS#002F00",
                      "--color","SHADEA#001F00",
                      "--color","SHADEB#00001F",
                      "--lower-limit", "0",
                      "DEF:ds1a=powerCapturenew.rrd:PowerCapture:AVERAGE",
                      "AREA:ds1a#05FF0B99:'Power Consumption'",
                      "--width", "1900", "--height", "1000")
        os.system('clear')
        rcvdData = float(rcvdData[2:])
        power = rcvdData
        amountToBeFilled = int(float((80*rcvdData)/3680))
        amountToBeNotFilled = 80 - amountToBeFilled
        print('')
        print('[', end='')
        for i in range(amountToBeFilled):
            print('#', end='')
        for i in range(amountToBeNotFilled):
            print(' ', end = '')
        print(f'] {power} in Ws')
while 1:
    mySocket()
