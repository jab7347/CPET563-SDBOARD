from numpysocket import NumpySocket
import cv2
import numpy as np

npSocket = NumpySocket()
npSocket.startServer(9999)


#Command Loop Structure

while True:
    matLabCmd = npSocket.receiveCmd()
    print(matLabCmd)
    if matLabCmd == "ImageReady":
        npSocket.send("Left")
        leftImg = npSocket.receive()
        npSocket.send("Right")
        rightImg = npSocket.receive()
        npSocket.send(np.array([400,400]))
    elif matLabCmd == "Quit":
        break
    #End if
npSocket.close()






