from numpysocket import NumpySocket
#import cv2
import numpy as np
import mmap
import struct
from frameGrabber import ImageProcessing
from frameGrabber import ImageFeedthrough
from frameGrabber import ImageWriter

camProcessed = ImageProcessing()
camFeedthrough = ImageFeedthrough()
camWriter = ImageWriter()

npSocket = NumpySocket()
npSocket.startServer(9999)

# only set this flag to true if you have generated your bit file with a
# Vivado reference design for Simulink

print "entering main loop"

# feel free to modify this command structue as you wish.  It might match the
# command structure that is setup in the Matlab side of things on the host PC.
while(1):
    cmd = npSocket.receiveCmd()
    #print(cmd)
    if cmd == '0':
        data = npSocket.receive()
        camWriter.setFrame(data)
        npSocket.send(np.array(2))
    elif cmd == '1':
        frameLeft,frameRight = camFeedthrough.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8)
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8)
        npSocket.send(tempImageLeft)
        npSocket.send(tempImageRight)
    elif cmd == '2':
        frameLeft,frameRight = camProcessed.getStereoGray()
        tempImageLeft = np.ascontiguousarray(frameLeft, dtype=np.uint8)
        tempImageRight = np.ascontiguousarray(frameRight, dtype=np.uint8)
        npSocket.send(tempImageLeft)
        npSocket.send(tempImageRight)
    else:
        break
npSocket.close()
