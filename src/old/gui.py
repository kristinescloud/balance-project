from tkinter import *

class NextWindow:
   
   def __init__(self, master):
       self.master = master
       master.title("Next") 
 
       self.buttonCal = Button(master, text = 'Calibrate', 
                            command = NextWindow.calibrate(self))
       self.buttonCal.pack()
       self.buttonBegin = Button(master, text = 'Begin Test', 
                            command = master.destroy)
       self.buttonBegin.pack()
       self.arduinoData = serial.Serial()
       self.arduinoData.port = '/dev/cu.Team_3_ESP-ESP32SPP'
       self.arduinoData.baudrate = 115200
       self.arduinoData.timeout = 0
       self.calibrationValues = []

   def calibrate(self):
      #get baseline readings from the serial of the ESP, store values in
      #a list of 4-value lists for 10 seconds.
      arduinoString = self.arduinoData.readline()      #ascii
      dataArray = line.split(b'\t')
      
##      sensOne = float(dataArray[0])
##      sensTwo = float(dataArray[1])
##      sensThree = float(dataArray[2])
##      sensFour = float(dataArray[3])

      calibrationValues.append(dataArray)

      #take the average for each of the four readings
      sensOne = 0
      sensTwo = 0
      sensThree = 0
      sensFour = 0

      for i in len(calibrationValues):
         sensOne += calibrationValues[i][0]
         sensTwo += calibrationValues[i][1]
         sensThree += calibrationValues[i][2]
         sensFour += calibrationValues[i][3]

      sensOne = sensOne/len(calibrationValues)
      sensTwo = sensTwo/len(calibrationValues)
      sensThree = sensThree/len(calibrationValues)
      sensFour = sensFour/len(calibrationValues)

      #store as strain gauge calibration variables
      calibrationValues[sensOne, sensTwo, sensThree, sensFour]
      
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
