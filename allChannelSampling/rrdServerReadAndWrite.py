import socket
import rrdtool
import time
import os
import re
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
        rcvdData = c.recv(120).decode()
        if not 'C' in rcvdData:
            c.close()
            time.sleep(0.2)
            break
        power = rcvdData
        time.sleep(0.3)
        os.system('clear')
        print(power)
        entry = re.split(':',power)
        entry = entry[1::2]
        for i in range(len(entry)):
            rrdtool.update(f"powerCapture{i}.rrd", f'N:{entry[i]}')
            print(f'Wrote N:{entry[i]} to powerCapture{i}.rrd')
        print(entry)
        entry = list(map(float, entry))
        for i in range(len(entry)):
            amountToBeFilled = int(float((80*entry[i])/3680))
            amountToBeNotFilled = 80 - amountToBeFilled
            print('')
            print('[', end='')
            for f in range(amountToBeFilled):
                print('#', end='')
            for d in range(amountToBeNotFilled):
                print(' ', end = '')
            print(f'] {entry[i]} in W (CH{i})')
while 1:
    mySocket()
