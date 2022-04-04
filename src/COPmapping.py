# import statements

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr
import time
from matplotlib.patches import Circle, Arc
import random

#---------global variables---------------

centerOfPressureX = np.array([0])
centerOfPressureY = np.array([0])
cond = False
calibrationValues = []

one_leg = False  #CHANGE THIS VARIABLE TO CHANGE STATES

targetX = 0
targetY = 0

timeInCircle = 0
timeOutOfCircle = 0

max_targetX = 15
max_targetY = 10
circleRadius = 3



if one_leg:

    max_targetX = 5
    max_targetY = 5
    circleRadius = 5

    
arc = Arc((targetX, targetY), (2 * circleRadius)+2, (2 * circleRadius)+2, color='white', linewidth='7')
circle = Circle((targetX, targetY), circleRadius, color='black', fill=False)

#----------plot data-------------------

def calibrate():
    counter = 0
    sensOne = 0
    sensTwo = 0
    sensThree = 0
    sensFour = 0
    while (counter < 11):
        a = serialData.readline()
        ar = a.decode("utf-8")
        ar = ar.split('\t')
        ar = ar[0:4]
        #print(ar)

        if(len(ar) < 4):
            pass
        else:
            for i in range(len(ar)):
                if ar[i] == '' or ar[i] == '\r\n':
                    print("passed")
                    pass
                else:
                    ar[i] = float(ar[i])
                    
        calibrationValues.append(ar)

        for i in range(len(self.calibrationValues)):
            sensOne += float(self.calibrationValues[i][0])
            sensTwo += float(self.calibrationValues[i][1])
            sensThree += float(self.calibrationValues[i][2])
            sensFour += float(self.calibrationValues[i][3])

        calibrationValues[sensOne, sensTwo, sensThree, sensFour]

def plot_data():
    global cond, centerOfPressureX, centerOfPressureY, timeInCircle, timeOutOfCircle, arc, circle, targetX, targetY

    COPx = 0
    COPy = 0
    
    if (cond == True):

        try:
            a = serialData.readline()
        except serial.SerialException as e:
            print(e)
            raise e
           
        
        ar = a.decode("utf-8")
        ar = ar.split('\t')
        ar = ar[0:4]
        print(ar)

        if(len(ar) < 4):
            pass
        else:
            for i in range(len(ar)):
                if ar[i] == '' or ar[i] == '\r\n':
                    #print("passed")
                    ar[i] = 0
                else:
                    ar[i] = float(ar[i])

            sensOne = 0.4545*(ar[0]) + 2.7273
            sensTwo = 0.4689*(ar[1]) - 159.67
            sensThree = 0.3058*(ar[2]) - 6.7932
            sensFour = 0.3605*(ar[3]) - 152.51

            if (sensOne + sensTwo + sensThree + sensFour == 0):
                pass
            else:
                # 22, 13
                COPx = 22*((sensTwo + sensThree)-(sensOne + sensFour))/(sensOne + sensTwo + sensThree + sensFour)
                COPy = 13*((sensOne + sensTwo)-(sensThree + sensFour))/(sensOne + sensTwo + sensThree + sensFour)

                centerOfPressureX[0] = COPx
                centerOfPressureY[0] = COPy

                

        #print(centerOfPressureX)
        #print(centerOfPressureY)
        
        points.set_xdata(centerOfPressureX)
        points.set_ydata(centerOfPressureY)

        

        if((targetX - centerOfPressureX[0])**2 + (targetY-centerOfPressureY[0])**2 < circleRadius**2):
            timeInCircle+=1
            if timeInCircle > 10:
                timeInCircle = 0
                timeOutOfCircle = 0
                targetX = random.randint(-1*max_targetX, max_targetX)
                targetY = random.randint(-1*max_targetY, max_targetY)
                try:
                    ax.patches.remove(circle)
                    ax.patches.remove(arc)
                except:
                    pass
                
                circle = Circle((targetX, targetY), circleRadius, color='black', fill=False)
                ax.add_patch(circle)
            else:
                
                try:
                    ax.patches.remove(arc)
                except:
                    pass
                arc = Arc((targetX, targetY), (2 * circleRadius)+2, (2 * circleRadius)+2, theta2 = 0, theta1 = -36*timeInCircle, color='green', linewidth='7')
                ax.add_patch(arc)
        else:
            if timeOutOfCircle > 5:
                timeInCircle = 0
                timeOutOfCircle = 0
                try:
                    ax.patches.remove(arc)
                except:
                    pass
            else:
                timeOutOfCircle +=1
        
        canvas.draw()
        time.sleep(0.1)
       
        serialData.flush()
        serialData.flushInput()
        serialData.flushOutput()
        
    root.after(1, plot_data)
def start_plot():
    global cond
    cond = True
    serialData.reset_input_buffer()

def stop_plot():
    global cond
    cond = False   
            


#-----------Main GUI code---------------

root = tk.Tk()
root.title('Live Force Graphing')
root.configure()
root.geometry("700x500") #this sets the window size

#-----------Create Plot object on GUI---------------
fig = Figure()
ax = fig.add_subplot(111)

ax.set_title('Center of Pressure');
ax.set_xlabel('X (cm)')
ax.set_ylabel('Y (cm)')
ax.set_xlim(-22,22)
ax.set_ylim(-13,13)
ax.set_aspect('equal')
points = ax.plot([],[], 'o', color = 'blue')[0]

ax.add_patch(circle)

canvas = FigureCanvasTkAgg(fig, master=root) #A tk.DrawingArea
canvas.get_tk_widget().place(x = 10,y = 10, width = 600,height = 400)
canvas.draw()

#------------------ make button ------------------------
root.update();
start = tk.Button(root, text = "Start", font = ('calbiri',12), command = lambda: start_plot())
start.place(x = 100, y = 500)

root.update();
stop = tk.Button(root, text = "Stop", font = ('calbiri',12), command = lambda: stop_plot())
stop.place(x = start.winfo_x() + start.winfo_reqwidth() + 20, y = 500)

root.update();
cal = tk.Button(root, text = "Calibrate", font = ('calbiri',12), command = lambda: calibrate())
cal.place(x = stop.winfo_x() + stop.winfo_reqwidth() + 20, y = 500)

#-------------------open the serial port------------------
serialData = sr.Serial('COM13', 115200);
serialData.reset_input_buffer()


root.after(1, plot_data)
root.mainloop()
