from numpysocket import NumpySocket
import cv2
import numpy as np

npSocket = NumpySocket()
npSocket.startServer(9999)

#Command Loop Structure

while(1):
    matLabCmd = npSocket.receiveCmd()
    print(matLabCmd)
    if matLabCmd == '0':
        print "reciving images"
        dataImg = npSocket.receive()
        stereoImage = np.reshape(dataImg, (720, 1280, 2))
        print "GOT Images"
    elif matLabCmd == '2':
        print "SENDING POSITION"
        npSocket.send(np.array([400, 400]))
    elif matLabCmd == '3':
        break
    #End if
npSocket.close()






