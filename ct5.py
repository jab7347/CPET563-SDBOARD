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
        leftGray = stereoImage[:, :, 0]
        leftGray = np.ascontiguousarray(leftGray, dtype=np.uint8)
        rightGray = stereoImage[:, :, 1]
        rightGray = np.ascontiguousarray(rightGray, dtype=np.uint8)

        leftEdge = cv2.Sobel(leftGray, cv2.CV_8U, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        rightEdge = cv2.Sobel(rightGray, cv2.CV_8U, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(leftEdge, connectivity=8, ltype=cv2.CV_32S)
        resPos= np.array(['1','1'],dtype=np.uint8)
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            if (abs(w-h) < 25 ) and 100 < area < 200:
                resPos = np.array([x,y], dtype=np.uint8)
            #End if
        #End for
        npSocket.send(resPos)
    else:
        print "received unknown command"
        break
npSocket.close()