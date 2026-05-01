from numpysocket import NumpySocket
import cv2
import numpy as np
import time

npSocket = NumpySocket()
npSocket.startServer(9999)

print "entering main loop"

while (1):
    cmd = npSocket.receiveCmd()
    print(cmd)
    if cmd == '0':
        print "received frame from matlab"
        data = npSocket.receive()
        print "converted image"
    elif cmd == '2':
        print "sending processed frames to matlab"
        time.sleep(1)
        npSocket.send(np.array([400,400]))
    else:
        print "received unknown command"
        break
npSocket.close()