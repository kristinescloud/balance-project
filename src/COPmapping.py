# import statements

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr
import time

#---------global variables---------------

centerOfPressureX = np.array([])
centerOfPressureY = np.array([])
cond = False
calibrationValues = []

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
    global cond, centerOfPressureX, centerOfPressureY

    COPx = 0
    COPy = 0
    
    if (cond == True):

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
                COPx = 22*((sensTwo + sensFour)-(sensOne + sensThree))/(sensOne + sensTwo + sensThree + sensFour)
                COPy = 13*((sensOne + sensTwo)-(sensThree + sensFour))/(sensOne + sensTwo + sensThree + sensFour)

                centerOfPressureX = np.append(centerOfPressureX, COPx)
                centerOfPressureY = np.append(centerOfPressureY, COPy)

        print(centerOfPressureX)
        print(centerOfPressureY)
        
        points.set_xdata(centerOfPressureX)
        points.set_ydata(centerOfPressureY)
        
        canvas.draw()

##--------------- if she's running slow, uncomment the below

##        serialData.flush()
##        serialData.flushInput()
##        serialData.flushOutput()

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
ax.set_xlabel('Time')
ax.set_ylabel('Force')
ax.set_xlim(0,30)
ax.set_ylim(0,30)
points = ax.plot([],[], 'o', color = 'blue')[0]

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
