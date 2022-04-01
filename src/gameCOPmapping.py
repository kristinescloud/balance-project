# import statements

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Arc
import tkinter as tk
import numpy as np
import serial as sr
import random
import time

#---------global variables---------------

cond = False
calibrationValues = []

targetX = random.randint(-15, 15)
targetY = random.randint(-15, 15)
targetX = 0
targetY = 0

centerOfPressureX = np.array([0])
centerOfPressureY = np.array([0])

timeInCircle = 0
arc = Arc((targetX, targetY), 12, 12, color='white', linewidth='7')
circle = Circle((targetX, targetY), 5, color='black', fill=False)

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
        print(ar)

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
    global cond, centerOfPressureX, centerOfPressureY, circle, timeInCircle, targetX, targetY, arc

    if (cond == True):

        a = serialData.readline()
        ar = a.decode("utf-8")
        ar = ar.split('\t')
        ar = ar[0:4]
        

        if(len(ar) < 4):
            pass
        else:
            for i in range(len(ar)):
                if ar[i] == '' or ar[i] == '\r\n':
                    print("passed")
                    pass
                else:
                    ar[i] = float(ar[i])

       
                    sensOne = float(ar[0]) 
                    sensTwo = float(ar[1]) - 400
                    sensThree = float(ar[2]) - 20
                    sensFour = float(ar[3]) - 330

                    COPx = 22*((sensTwo + sensFour)-(sensOne + sensThree))/(sensOne + sensTwo + sensThree + sensFour)
                    COPy = 13*((sensOne + sensTwo)-(sensThree + sensFour))/(sensOne + sensTwo + sensThree + sensFour)

                    
                    centerOfPressureX[0] = COPx
                    centerOfPressureY[0] = COPy

                    print(COPx, COPy)
        points.set_xdata(centerOfPressureX)
        points.set_ydata(centerOfPressureY)

        #ax.plot(targetX, targetY, 'o', color='red')[0]
        ax.add_patch(circle)

        if((targetX - centerOfPressureX[0])**2 + (targetY-centerOfPressureY[0])**2 < 5**2):
            timeInCircle+=1
            if timeInCircle > 10:
                targetX = random.randint(-15, 15)
                targetY = random.randint(-15, 15)
                ax.patches.remove(circle)
                circle = Circle((targetX, targetY), 5, color='black', fill=False)
                ax.add_patch(circle)
            else:
                try:
                    ax.patches.remove(arc)
                except:
                    pass
                arc = Arc((targetX, targetY), 12, 12, theta2 = 0, theta1 = -36*timeInCircle, color='green', linewidth='7')
                ax.add_patch(arc)
        else:
            try:
                ax.patches.remove(circle)
            except:
                pass

            timeInCircle = 0
            try:
                ax.patches.remove(arc)
            except:
                pass

        
        canvas.draw()

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

ax.set_title('Serial Data');
ax.set_xlabel('Center X')
ax.set_ylabel('Center Y')
ax.set_xlim(-100,100)
ax.set_ylim(-200,200)
ax.set_aspect('equal')


points = ax.plot([],[], 'o', color = 'blue')[0]
#target_points = ax.plot(targetX, targetY, 'o', color='red')[0]

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
serialData = sr.Serial('/dev/cu.Team_3_ESP-ESP32SPP', 115200);
serialData.reset_input_buffer()


root.after(1, plot_data)
root.mainloop()
