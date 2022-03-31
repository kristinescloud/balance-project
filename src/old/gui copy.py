from tkinter import *
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
from drawnow import *

class NextWindow:
   
   def __init__(self, master):
       self.master = master
       master.title("Next")
       self.arduinoData = serial.Serial()
       self.arduinoData.port = '/dev/cu.usbserial-14330'
       self.arduinoData.baudrate = 115200
       self.arduinoData.timeout = 0
       self.arduinoData.open()
       self.calibrationValues = []
 
       self.buttonCal = Button(master, text = 'Calibrate', 
                            command = NextWindow.calibrate(self))
       self.buttonCal.pack()
       self.buttonBegin = Button(master, text = 'Begin Test', 
                            command = master.destroy)
       self.buttonBegin.pack()

   def calibrate(self):
      #get baseline readings from the serial of the ESP, store values in
      #a list of 4-value lists for 10 seconds.
      arduinoString = self.arduinoData.readline()
      print(arduinoString)
      dataArray = arduinoString.split('\t'.encode())
      
##      sensOne = float(dataArray[0])
##      sensTwo = float(dataArray[1])
##      sensThree = float(dataArray[2])
##      sensFour = float(dataArray[3])

      self.calibrationValues.append(dataArray)
      print(self.calibrationValues)

      #take the average for each of the four readings
      sensOne = 0
      sensTwo = 0
      sensThree = 0
      sensFour = 0

      for i in range(len(self.calibrationValues)):
         sensOne += float(self.calibrationValues[i][0])
         sensTwo += float(self.calibrationValues[i][1])
         sensThree += float(self.calibrationValues[i][2])
         sensFour += float(self.calibrationValues[i][3])

      sensOne = sensOne/len(self.calibrationValues)
      sensTwo = sensTwo/len(self.calibrationValues)
      sensThree = sensThree/len(self.calibrationValues)
      sensFour = sensFour/len(self.calibrationValues)

      #store as strain gauge calibration variables
      self.calibrationValues[sensOne, sensTwo, sensThree, sensFour]
      
class StartWindow:
 
   def __init__(self, master):
      self.master = master
      master.title("Welcome to Balance.")
 
      self.buttonOne = Button(master, text = 'Force Time Graphing', 
                           command = self.openNext)
      self.buttonTwo = Button(master, text = 'Center of Pressure Time Graphing', 
                           command = self.openNext)
      self.buttonThree = Button(master, text = 'Center of Pressure', 
                           command = self.openNext)
      self.buttonOne.pack()
      self.buttonTwo.pack()
      self.buttonThree.pack()
      
 
   def openNext(self):
      self.newWindow = Toplevel(self.master)
      self.app = NextWindow(self.newWindow)

# main program #
root = Tk()
app = StartWindow(root)
root.mainloop()
