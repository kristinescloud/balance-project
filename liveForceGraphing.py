import serial
import matplotlib.pyplot as plt
import numpy
from drawnow import *

sensorOne = []
sensorTwo = []
sensorThree = []
sensorFour = []
arduinoData = serial.Serial('/dev/cu.Team_3_ESP-ESP32SPP', 115200)
ser_bytes = arduinoData.readline()
plt.ion()

def makeFig(): #Creating the function that will make ourdesired plot
    plt.plot(sensorOne,'r' )
    plt.plot(sensorTwo, 'g')
    plt.plot(sensorThree, 'b')
    plt.plot(sensorFour, 'c')
    
def liveForce():
    
    while True:
        while(arduinoData.in_waiting == 0):
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



