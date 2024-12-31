import tkinter as tk# import tkinter
from pynput.mouse import Listener
from pynput import keyboard, mouse
import pygetwindow as gw
from pywinauto import Application
import win32gui
import win32con
import time
import struct
import win32api
import autoit
import ast

root = tk.Tk() # create a window
root.title("Ghost Mouse")
root.geometry("900x700") # set the window size
root.configure(bg="#333333")
entry = tk.Entry(root)
#color controles
buttonGrey = '#444444'
lableGrey = '#333333'
dataBoxbg = lableGrey

lightBlue = '#B0C4DE'
green = '#66CD00'
pink = '#EE1289'
file = "ghost_data.txt"

def getLst(file):
    dictLst = []
    with open(file) as f: 
        data = f.read()
    dictLst = ast.literal_eval(data)
    return dictLst

data = getLst(file)
recorded_actions = data[1]
window = data[0]
user_poses = []
time_stamps = data[2]
timer = 0.0
start_time = 0.0
ctrl_pressed = False

def updateFile(Lst, file):
    with open(file, "w") as f:
        f.write(str(Lst))

def on_click(x, y, button, pressed):
    if pressed:
        recorded_actions.append(('click', (x, y)))
        capture_click_time()

def capture_click_time():
    global start_time
    click_time = time.perf_counter()
    delta_time = click_time - start_time
    start_time = click_time
    print(f"Click at {click_time}, Delta Time: {delta_time}")
    time_stamps.append(delta_time)

stop = False
def play_back(actions, window_title, repetitions):
    focus_window(window_title)
    key_listener2.start()
    for t in range(repetitions):
        if stop:
            break
        print(t)
        i = 0
        for action, pos in actions:
            time.sleep(time_stamps[i])
            mouse_pos = autoit.mouse_get_pos() # back to user position
            if stop == False:
                if action == 'click':
                    autoit.mouse_move(pos[0], pos[1], speed=0)
                    time.sleep(0.08)
                    autoit.mouse_click('left', pos[0], pos[1])
                    print(f"Clicked at {pos}")
                autoit.mouse_move(mouse_pos[0], mouse_pos[1], speed=0) # back to user position
                i += 1
        time.sleep(time_stamps[i])
    forget_all(root)
    main()

mouse_listener = mouse.Listener(on_click=on_click)

def record(window):
    global recorded_actions
    recorded_actions = []
    global start_time
    start_time = time.perf_counter()
    focus_window(window)
    mouse_listener.start()
    key_listener.start()
    forget_all(root)
    main()

def selectWindow():#print and select from open windows
    forget_all(root)
    windows = gw.getAllTitles()#makes list of window names
    windows = [win for win in windows if win] #need to research this weird code
    def getName(name):
        lst = [name, recorded_actions, time_stamps]
        updateFile(lst, file)
        forget_all(root)
        main()
    makeLable(f"\n\nOpen windows.", 18)
    for window in windows:
        makeButton(window, lambda w = window: getName(w), hi=1, wi=70)

def focus_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    time.sleep(0.25)
    window[0].activate()

def on_press(key):
    if key == keyboard.KeyCode.from_char('f'):
        mouse_listener.stop() # Stop mouse recording
        capture_click_time()
        key_listener.stop()
        lst = [window, recorded_actions, time_stamps]
        updateFile(lst, file)
        print(recorded_actions)
        print(time_stamps)
        focus_window("Ghost Mouse")

def on_press2(key):
    global stop
    if key == keyboard.KeyCode.from_char('u'):
        stop = True
        key_listener2.stop()
        print("stopped")
        focus_window("Ghost Mouse")

key_listener2 = keyboard.Listener(on_press=on_press2)
key_listener = keyboard.Listener(on_press=on_press)

def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False

def main():
    user_data = getLst(file)
    print("main function")
    window = user_data[0]
    recorded_actions = user_data[1]
    def play():
        repetitions = 1000
        focus_window(window)
        play_back(recorded_actions, window, repetitions)
    
    makeLable(f"\n\nWindow: {window}\n", 18)
    makeButton("Select Window", selectWindow, wi=20)
    makeButton("Record", lambda w = window: record(w), wi=20)
    makeButton("Play", play, wi=20)
    tk.Label(root, text='\n\n\nDeveloped By Thomas Gomez @https://github.com/BruzaTom', fg=lablelc, bg="#333333", font=("Arial", 10, "bold")).pack()
    root.mainloop()

#entrys bg color change on focus
def on_focus_in(event):
    event.widget.config(bg=green)

def on_focus_out(event):
    event.widget.config(bg='white')

def on_return_next(event):
    event.widget.tk_focusNext().focus()

def entrys_focus_color(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.bind("<FocusIn>", on_focus_in)
            widget.bind("<FocusOut>", on_focus_out)
            widget.bind("<Return>", on_return_next)

def forget_all(parent):
    for widget in parent.winfo_children():
        widget.forget()

def makeLable(string, size):
    return tk.Label(root, text=string, fg=lablelc, bg=lablebg, font=("Arial", size, "bold")).pack()

def makeButton(name, func, hi=3, wi=8):
    return tk.Button(
        root,
        text=name,
        command=func,
        fg=buttonlc, bg=buttonbg,
        height=hi, width=wi,
        font=("Arial", 12, "bold")
        ).pack()

font_style = ("Helvetica", 12, "bold")
colorsFile = 'pldata/colors.txt'
#userColors = getLst(colorsFile)
buttonbg = buttonGrey
buttonlc = lightBlue
lablebg = lableGrey
lablelc = lightBlue

main()