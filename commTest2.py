from numpysocket import NumpySocket
import cv2
import numpy as np

npSocket = NumpySocket()
npSocket.startServer(9999)


#Command Loop Structure

while True:
    matLabCmd = npSocket.receiveCmd()
    print(matLabCmd)
    if matLabCmd == '0':
        #print("SENDING LEFT COMMAND")
        #npSocket.send(np.array(matLabCmd))
        dataImg = npSocket.receive()
        print("GOT Images")
    elif matLabCmd == '1':
        print("SENDING POSITION")
        npSocket.send(np.array([400, 400]))
    elif matLabCmd == '2':
        break
    #End if
npSocket.close()






