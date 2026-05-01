from numpysocket import NumpySocket
import cv2
import numpy as np
import time
import math

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
        maxCirc = 0
        for i in range(1, num_labels):
            component_mask = np.uint8(labels == i) * 255
            # Find contours for the component
            _, contours, hierarchy = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # Calculate perimeter (arc length) for each contour
            perimeter = 0.0
            for cnt in contours:
                perimeter += cv2.arcLength(cnt, True)  # True = closed contour
            x, y, w, h, area = stats[i]
            circularity = (4 * math.pi * area / math.pow(perimeter,2))
            if (circularity > maxCirc) and 50 < area < 100:
                resPos = np.array([x,y], dtype=np.uint8)
            #End if
        #End for
        npSocket.send(resPos)
    else:
        print "received unknown command"
        break
npSocket.close()