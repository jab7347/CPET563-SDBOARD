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
        stereoImage = np.reshape(data, (720, 1280, 2))
        print "converted image"
    elif cmd == '2':
        print "sending processed frames to matlab"
        leftGray = stereoImage[:, :, 1]
        leftGray = np.ascontiguousarray(leftGray, dtype=np.uint8)
        rightGray = stereoImage[:, :, 2]
        rightGray = np.ascontiguousarray(rightGray, dtype=np.uint8)
        npSocket.send(np.array(['400','400']))
    else:
        print "received unknown command"
        break
npSocket.close()