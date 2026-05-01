from numpysocket import NumpySocket
import cv2
import numpy as np

npSocket = NumpySocket()
npSocket.startServer(9999)


#Command Loop Structure

while True:
    matLabCmd = npSocket.receiveCmd()
    print(matLabCmd)
    if matLabCmd == 0:
        npSocket.send(1)
        leftImg = npSocket.receive()
        npSocket.send(2)
        rightImg = npSocket.receive()
        npSocket.send(np.array([400,400]))
    elif matLabCmd == 99:
        break
    #End if
npSocket.close()






