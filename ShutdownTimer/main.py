__author__ = "Enrico Ferraiolo"
__copyright__ = "Copyright 2022, Enrico Ferraiolo"
__credits__ = ["Enrico Ferraiolo"]
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Enrico Ferraiolo"
__email__ = "enricofe300@gmail.com"
__status__ = "Production"


import tkinter.messagebox
from datetime import datetime, timedelta
import os
import re
import tkinter as tk

# Constants
FONTDEFAULT_LB = 'calibre', 12, 'normal'
FONTDEFAULT_ENTRY = 'calibre', 12, 'normal'
FONTDEFAULT_BTN = 'calibre', 10, 'normal'
FONTCLOCK = "calibre", 16, "bold"
FONTCLOCK_BTN = "calibre", 12, "bold"
FONTDEFAULT_LBTIME = "calibre", 12, "bold"
FONTBTN_ABORT = "calibre", 12, "bold"
ENTRY_PLACEHOLDER = "HH:MM:SS"
SB_INC = "1"
SB_HOURS_MAX = "23"
SB_MIN_MAX = "59"
SB_SEC_MAX = "59"
SB_MIN = "0"
TIME = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
windowWidth = 470
windowHeight = 150
widgetWidth = 250
widgetHeight = 80

# Create window object
root = tk.Tk()


# Events
def entryKbdReturn(events):
    # print("You hit return")
    # print("focus is: ", root.focus_get())
    btn_Submit.invoke()


def entryClearBoxHandler(events, input):
    # print("Focus in")
    if input == ENTRY_PLACEHOLDER:
        entry_Time.delete(0, tk.END)


def entryClearBox():
    entry_Time.delete(0, tk.END)


def entryFillPlaceholder(events, input):
    # print("Focus out")
    if input == "":
        entry_Time.insert(0, ENTRY_PLACEHOLDER)


def entryClicked(events):
    # print("Clicked")
    pickTimeWidget()


def sbScrollListener(event, self, value, thisMax, thisMin, inc):
    time = int(value)
    if event.num == 4 or event.delta == 120:
        # print("Scroll up")
        time += int(inc)
        # print("Time: ",time,"max: ", thisMax,"min: ",thisMin)
        if time <= int(thisMax):
            self.delete('0', 'end')
            if time < 10:
                self.insert('0', TIME[time])
            else:
                self.insert('0', time)
    if event.num == 5 or event.delta == -120:
        # print("Scroll down")
        time -= int(inc)
        # print("Time: ", time, "max: ", thisMax, "min: ", thisMin)
        if time >= int(thisMin):
            self.delete('0', 'end')
            if time < 10:
                self.insert('0', TIME[time])
            else:
                self.insert('0', time)


def checkSB(event, self, time):
    if int(time) < 10:
        self.delete('0', 'end')
        self.insert('0', TIME[int(time)])


def checkStringTime(stringTime):
    pattern = "\d{2}[:]\d{2}[:]\d{2}"
    regex = re.match(pattern, stringTime)
    return regex


# Functions
def submitBtn(stringTime):
    # Check parameter
    if not (checkStringTime(stringTime)):
        lb_Output.config(text="Invalid input")
        return
    lb_Output.config(text=stringTime)
    splitString = stringTime.split(':')
    hours = splitString[0]
    minutes = splitString[1]
    seconds = splitString[2]
    total = int(hours) * 3600 + int(minutes) * 60 + int(seconds)

    # Set shutdown
    shutdown(str(total))

    # Output
    lb_Output.config(text="Timer set in:")
    lb_OutputTime.config(text=str(total) + " seconds")
    lb_final.config(text="Your PC will shut down at:")
    now = datetime.now()
    finalTime = now + timedelta(seconds=total)
    # print(now)
    # print(finalTime)
    lb_finalTime.config(text=finalTime.strftime("%H:%M:%S"))


def popUpWindow(boxType, title, message):
    # type can be "error", "warning", "info"
    if boxType == "error":
        tkinter.messagebox.showerror(title=title, message=message)
    if boxType == "warning":
        tkinter.messagebox.showwarning(title=title, message=message)
    if boxType == "info":
        tkinter.messagebox.showinfo(title=title, message=message)


def shutdown(time):
    # /f arresto forzato
    # /t <xxx>	Imposta il periodo di timeout prima dell'arresto su xxx secondi.
    # L'intervallo valido è 0-315360000 (10 anni), con un valore predefinito di 30.
    # Se il periodo di timeout è maggiore di 0, il /f parametro è implicito.
    # shutdown /f /t 20 spegne il PC dopo 20 secondi
    timer = "shutdown -s -t " + time
    # print(timer)
    feedback = os.system(timer)
    # (0) OK.
    # (1190) Arresto del sistema già pianificato.
    # print(feedback)
    if feedback == 1190:
        # Timer already set
        popUpWindow("error", "Error", "Shutdown already scheduled.")


def abortShutdown():
    # shutdown /a
    # (0) OK,
    # (1116) Impossibile interrompere l'arresto del sistema, perchè la chiusura non è in corso.
    abort = "shutdown /a"
    feedback = os.system("shutdown /a")
    # print(feedback)
    if feedback == 1116:
        # Timer already set
        popUpWindow("warning", "Warning", "There is no scheduled shutdown.")
    if feedback == 0:
        popUpWindow("info", "Info", "Shutdown aborted.")


def updateTime(hours, minutes, seconds, window):
    # print(hours,":",minutes,":",seconds)
    if int(hours) < 10:
        hours = TIME[int(hours)]
    if int(minutes) < 10:
        minutes = TIME[int(minutes)]
    if int(seconds) < 10:
        seconds = TIME[int(seconds)]
    time = hours + ":" + minutes + ":" + seconds
    entryClearBox()
    entry_Time.insert(0, time)
    window.destroy()


def checkCredits():
    popUpWindow("info", "Credits",
                "Made by Enrico Ferraiolo.\nTimer icons created by Freepik - Flaticon flaticon.com/free-icons/timer")


def centerWindow(self, width, height, wConst, hConst):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)
    self.geometry('%dx%d+%d+%d' % (width, height, x + wConst, y + hConst))


def pickTimeWidget():
    flyingWidget = tk.Toplevel(root)
    geometry = str(widgetWidth) + "x" + str(widgetHeight)
    centerWindow(flyingWidget, widgetWidth, widgetHeight, 0, -windowHeight)
    flyingWidget.geometry(geometry)
    flyingWidget.resizable(False, False)

    # Clock UI
    sb_Hours = tk.Spinbox(flyingWidget)
    sb_Hours.configure(from_=SB_MIN, increment=SB_INC,
                       justify='center', to=SB_HOURS_MAX, width='3', font=FONTCLOCK)
    sb_Hours.delete('0', 'end')
    sb_Hours.insert('0', "00")
    sb_Minutes = tk.Spinbox(flyingWidget)
    sb_Minutes.configure(from_=SB_MIN, increment=SB_INC,
                         justify='center', to=SB_MIN_MAX, width='3', font=FONTCLOCK)
    sb_Minutes.delete('0', 'end')
    sb_Minutes.insert('0', "00")
    sb_Seconds = tk.Spinbox(flyingWidget)
    sb_Seconds.configure(from_=SB_MIN, increment=SB_INC,
                         justify='center', to=SB_SEC_MAX, width='3', font=FONTCLOCK)
    sb_Seconds.delete('0', 'end')
    sb_Seconds.insert('0', "00")

    # Placing
    btn_SetTime = tk.Button(flyingWidget, text="Change time", font=FONTCLOCK_BTN,
                            command=lambda: updateTime(sb_Hours.get(), sb_Minutes.get(), sb_Seconds.get(),
                                                       flyingWidget))
    btn_SetTime.grid(row=1, column=1)
    sb_Hours.grid(row='0', column='0')
    sb_Minutes.grid(row='0', column='1')
    sb_Seconds.grid(row='0', column='2')

    # Event listener
    sb_Hours.bind("<MouseWheel>",
                  lambda event: sbScrollListener(event, sb_Hours, sb_Hours.get(), SB_HOURS_MAX, SB_MIN, SB_INC))
    sb_Minutes.bind("<MouseWheel>",
                    lambda event: sbScrollListener(event, sb_Minutes, sb_Minutes.get(), SB_MIN_MAX, SB_MIN, SB_INC))
    sb_Seconds.bind("<MouseWheel>",
                    lambda event: sbScrollListener(event, sb_Seconds, sb_Seconds.get(), SB_SEC_MAX, SB_MIN, SB_INC))
    #  sb_Hours.bind('<FocusOut>', lambda event: checkSB(event, sb_Hours, sb_Hours.get()))
    # sb_Minutes.bind('<FocusOut>', lambda event: checkSB(event, sb_Minutes, sb_Hours.get()))
    # sb_Seconds.bind('<FocusOut>', lambda event: checkSB(event, sb_Seconds, sb_Hours.get()))


# setting the window
geometry = str(windowWidth) + "x" + str(windowHeight)
root.geometry("470x150")
root.resizable(False, False)
centerWindow(root, windowWidth, windowHeight, 0, 0)
root.iconbitmap("./stopwatch.ico")
root.title("Shutdown Timer")

# Variables
input_Time = tk.StringVar()

# PARTS
# Parts -- Time
lb_Time = tk.Label(root, text='Insert time', anchor="w", font=FONTDEFAULT_LB)
entry_Time = tk.Entry(root, textvariable=input_Time,
                      width=15, font=FONTDEFAULT_ENTRY)
entry_Time.insert(0, ENTRY_PLACEHOLDER)
btn_Submit = tk.Button(root, text='Set', width=7, font=FONTDEFAULT_BTN,
                       command=lambda: submitBtn(input_Time.get()))

# Parts -- Abort shutdown
btn_abortShutdown = tk.Button(root, text="Abort shutdown", font=FONTBTN_ABORT, bg="#FFBD33", activebackground="#FF5733",
                              command=lambda: abortShutdown())

# Parts -- Output
lb_Output = tk.Label(root, text="", width=12, anchor="w", font=FONTDEFAULT_LB)
lb_OutputTime = tk.Label(root, text="", width=12,
                         anchor="w", font=FONTDEFAULT_LBTIME)
lb_final = tk.Label(root, text="", width=19, anchor="w", font=FONTDEFAULT_LB)
lb_finalTime = tk.Label(root, text="", width=14,
                        anchor="w", font=FONTDEFAULT_LBTIME)

# Parts -- Credits
btn_Credits = tk.Button(root, text="Credits", font=FONTDEFAULT_BTN, command=lambda: checkCredits())

# Placing parts
# Placing -- Time
root.columnconfigure(0, weight=0)  # avoid overgrowth
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=0)
lb_Time.grid(row=0, column=0, sticky="W")
entry_Time.grid(row=0, column=1, sticky="N")
btn_Submit.grid(row=0, column=2, sticky="W")
# Placing -- Abort shutdown
btn_abortShutdown.grid(row=3, column=2, sticky="W")
# Placing -- Output
lb_Output.grid(row=1, column=0, sticky="W", pady=15)
lb_OutputTime.grid(row=1, column=1, sticky="W", pady=15)
lb_final.grid(row=2, column=0, sticky="W")
lb_finalTime.grid(row=2, column=1, sticky="W")
# Placing -- Credits
btn_Credits.grid(row=3, column=0, sticky="W")

# Event listener
entry_Time.bind('<Return>', entryKbdReturn)
entry_Time.bind('<FocusIn>', lambda event: entryClearBoxHandler(
    event, input_Time.get()))
entry_Time.bind('<FocusOut>', lambda event: entryFillPlaceholder(
    event, input_Time.get()))
entry_Time.bind('<1>', lambda event: entryClicked(event))

# Display window
root.mainloop()
