# import statements

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr
import time

#---------global variables---------------

data1 = np.array([])
data2 = np.array([])
data3 = np.array([])
data4 = np.array([])
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
    global cond, data1, data2, data3, data4

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
                    print("passed")
                    pass
                else:
                    ar[i] = float(ar[i])


            if(len(data1) < 100):
                data1 = np.append(data1, ar[0])
                data2 = np.append(data2, ar[1])
                data3 = np.append(data3, ar[2])
                data4 = np.append(data4, ar[3])
            else:
                data1[0:99] = data1[1:100]
                data1[99] = ar[0]
                data2[0:99] = data2[1:100]
                data2[99] = ar[1]
                data3[0:99] = data3[1:100]
                data3[99] = ar[2]
                data4[0:99] = data4[1:100]
                data4[99] = ar[3]
            
        line1.set_xdata(np.arange(0, len(data1)))
        line2.set_xdata(np.arange(0, len(data1)))
        line3.set_xdata(np.arange(0, len(data1)))
        line4.set_xdata(np.arange(0, len(data1)))
        line1.set_ydata(data1)
        line2.set_ydata(data2)
        line3.set_ydata(data3)
        line4.set_ydata(data4)

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
ax.set_xlabel('Time')
ax.set_ylabel('Force')
ax.set_xlim(0,100)
ax.set_ylim(-0.5,800)
line1 = ax.plot([],[], color = 'green')[0]
line2 = ax.plot([],[], color = 'blue')[0]
line3 = ax.plot([],[], color = 'cyan')[0]
line4 = ax.plot([],[], color = 'red')[0]


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
