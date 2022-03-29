import serial
import matplotlib.pyplot as plt
import numpy
from drawnow import *

centerOfPressureX = []
centerOfPressureY = []

arduinoData = serial.Serial('/dev/cu.Team_3_ESP-ESP32SPP', 115200)
ser_bytes = arduinoData.readline()
plt.ion()

def makeFig(): #Creating the function that will make ourdesired plot
    plt.plot(centerOfPressureX,'r' )
    plt.plot(centerOfPressureY, 'b')
    
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

        COPx = 21*((sensTwo + sensFour)-(sensOne + sensThree))/(sensOne + sensTwo + sensThree + sensFour)
        COPy = 12*((sensOne + sensTwo)-(sensThree + sensFour))/(sensOne + sensTwo + sensThree + sensFour)

        centerOfPressureX.append(COPx)
        centerOfPressureY.append(COPy)

        drawnow(makeFig)

        plt.pause(.000001)
