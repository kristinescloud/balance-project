import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
from drawnow import *


arduinoData = serial.Serial('/dev/cu.usbserial-14330', 115200)
ser_bytes = arduinoData.readline()
plt.ion()

sensorOne = []
sensorTwo = []
sensorThree = []
sensorFour = []

def makeFig(): #Creating the function that will make ourdesired plot
    plt.plot(sensorOne,'r' )
    plt.plot(sensorTwo, 'g')
    plt.plot(sensorThree, 'b')
    #plt.plot(sensorFour, 'c')
    
def liveForce():
    
    while True:
        while(arduinoData.inWaiting == 0):
            pass
        arduinoString = arduinoData.readline() #read line of text from the serial port
        dataArray = arduinoString.split('\t'.encode())
        
        sensOne = float(dataArray[0])
        sensTwo = float(dataArray[1])
        sensThree = float(dataArray[2])
        sensFour = float(dataArray[3])

        sensorOne.append(sensOne)
        sensorTwo.append(sensTwo)
        sensorThree.append(sensThree)
        sensorFour.append(sensFour)

        drawnow(makeFig)

        plt.pause(.000001)



