import os
import tkinter as tk# import tkinter
from pynput.mouse import Listener, Button
from pynput import keyboard, mouse
import pygetwindow as gw
from pywinauto import Application
import time
import autoit
import ast
import ctypes

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

def getLst(file):
    dictLst = []
    with open(file) as f: 
        data = f.read()
    dictLst = ast.literal_eval(data)
    return dictLst

#files
file = "ghost_data.txt"#primary actions
if not os.path.exists(file):
    with open(file, "w") as f:
        f.write("[ '', [], []]")  # Write default content
    print(f"'{file}' created with default data.")
else:
    print(f"'{file}' already exists.")
file2 = "new_step.txt"#for new step
if not os.path.exists(file2):
    with open(file2, "w") as f:
        f.write(f"['{getLst(file)[0]}', [], []]")  # Write default content
    print(f"'{file2}' created with default data.")
else:
    print(f"'{file2}' already exists.")
file3 = "options.txt"#for new step
if not os.path.exists(file3):
    with open(file3, "w") as f:
        f.write("[False, 0]")  # Write default content
    print(f"'{file3}' created with default data.")
else:
    print(f"'{file3}' already exists.")

#options
options = getLst(file3)
new_step = options[0]
lap = options[1]
print(f'new step: {new_step}')
print(f'lap: {lap}')

class app2:
    def __init__(self):
        self.file = file2
        self.data = getLst(file2)
        self.recorded_actions = self.data[1]
        self.time_stamps = self.data[2]
        self.window = self.data[0]

    def record(self):
        #forget_all(root)
        #makeLable("\n\n\n\nRecording\nPress f to stop.", 16)
        self.mouse_listener = mouse.Listener(on_click=self.on_click) #need to implement on recording
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.recorded_actions = []
        self.time_stamps = []
        self.start_time = time.perf_counter()
        self.focus_window(self.window)
        self.mouse_listener.start()
        self.key_listener.start()

    def focus_window(self, window_title):
        window = gw.getWindowsWithTitle(window_title)
        time.sleep(0.25)
        window[0].activate()

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('f'):
            self.capture_click_time()
            self.mouse_listener.stop() # Stop mouse recording
            self.key_listener.stop()
            lst = [self.window, self.recorded_actions, self.time_stamps]
            updateFile(lst, file2)
            print(self.recorded_actions)
            print(self.time_stamps)
            self.focus_window("Ghost Mouse")

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == Button.left:
                self.recorded_actions.append(('left_click', (x, y)))
            elif button == Button.right:
                self.recorded_actions.append(('right_click', (x, y)))
            self.capture_click_time()

    def capture_click_time(self):
        click_time = time.perf_counter()
        delta_time = click_time - self.start_time
        self.start_time = click_time
        print(f"Click at {click_time}, Delta Time: {delta_time}")
        self.time_stamps.append(delta_time)

class app:
    def __init__(self):
        self.file = file
        self.data = getLst(file)
        self.data2 = getLst(file2)#for new step
        self.recorded_actions = self.data[1]
        self.time_stamps = self.data[2]
        #print(f"recorded actions: {self.recorded_actions}")
        self.window = self.data[0]
        #print(f"window: {self.window}")
        self.user_poses = []
        #print(f"time stamps: {self.time_stamps}")
        self.timer = 0.0
        self.start_time = 0.0
        self.ctrl_pressed = False
        self.stop = False
        self.mouse_listener = None
        self.key_listener = None
        self.key_listener2 = None

    def insert_step(self, lap, trigger_lap, data, init_actions, init_timestamps):
        self.recorded_actions2 = self.data2[1]#for new step
        self.time_stamps2 = self.data2[2]#for new step
        if lap >= trigger_lap:#for new step
            print("new step activated")
            return self.recorded_actions2, self.time_stamps2, -1
        else:
            return init_actions, init_timestamps, lap

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == Button.left:
                self.recorded_actions.append(('left_click', (x, y)))
            elif button == Button.right:
                self.recorded_actions.append(('right_click', (x, y)))
            self.capture_click_time()

    def capture_click_time(self):
        click_time = time.perf_counter()
        delta_time = click_time - self.start_time
        self.start_time = click_time
        print(f"Click at {click_time}, Delta Time: {delta_time}")
        self.time_stamps.append(delta_time)

    def play_back(self, init_actions, init_timestamps, window_title, repetitions):
        self.focus_window(window_title)
        #transperant = terminal()
        self.key_listener2 = keyboard.Listener(on_press=self.on_press2)
        self.key_listener2.start()
        count = 0
        t = 0
        while t < repetitions:
            if new_step == True:
                print(f"new step: on\nwill activate in {lap-t} laps")
                actions, timestamps, t = self.insert_step(t, int(lap), self.data2, init_actions, init_timestamps)
            else:
                count -= 1
                actions = init_actions
                timestamps = init_timestamps
            #transperant.lift()
            if self.stop:
                forget_all(root)
                main()
            print(f"laps completed: {count}")
            i = 0
            for action, pos in actions:
                time.sleep(timestamps[i])
                #mouse_pos = autoit.mouse_get_pos() # back to user position
                if self.stop == False:
                    time.sleep(0.08)
                    if action == 'left_click':
                        autoit.mouse_move(pos[0], pos[1], speed=0)
                        time.sleep(0.08)
                        autoit.mouse_click('left', pos[0], pos[1])
                        #print(f"left Clicked at {pos}")
                    if action == 'right_click':
                        autoit.mouse_move(pos[0], pos[1], speed=0)
                        time.sleep(0.08)
                        autoit.mouse_click('right', pos[0], pos[1])
                        #print(f"right Clicked at {pos}")
                    #autoit.mouse_move(mouse_pos[0], mouse_pos[1], speed=0) # back to user position
                    i += 1
                else:
                    forget_all(root)
                    main()
            t += 1
            count += 1
            time.sleep(self.time_stamps[i])

    def play(self):
        repetitions = 1000
        self.focus_window(self.window)
        self.play_back(self.recorded_actions, self.time_stamps, self.window, repetitions)
        

    def record(self):
        #forget_all(root)
        #makeLable("\n\n\n\nRecording\nPress f to stop.", 16)
        self.mouse_listener = mouse.Listener(on_click=self.on_click) #need to implement on recording
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.recorded_actions = []
        self.time_stamps = []
        self.start_time = time.perf_counter()
        self.focus_window(self.window)
        self.mouse_listener.start()
        self.key_listener.start()

    def selectWindow(self):#print and select from open windows
        forget_all(root)
        windows = gw.getAllTitles()#makes list of window names
        windows = [win for win in windows if win] #need to research this weird code
        def getName(name):
            lst = [name, self.recorded_actions, self.time_stamps]
            updateFile(lst, file)
            with open(file2, "w") as f:
                f.write(f"['{getLst(file)[0]}', [], []]")
            forget_all(root)
            main()
        makeLable(f"\n\nOpen windows.", 18)
        for window in windows:
            makeButton(window, lambda w = window: getName(w), hi=1, wi=70)

    def focus_window(self, window_title):
        window = gw.getWindowsWithTitle(window_title)
        time.sleep(0.25)
        window[0].activate()

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('f'):
            self.capture_click_time()
            self.mouse_listener.stop() # Stop mouse recording
            self.key_listener.stop()
            lst = [self.window, self.recorded_actions, self.time_stamps]
            updateFile(lst, file)
            print(self.recorded_actions)
            print(self.time_stamps)
            self.focus_window("Ghost Mouse")

    def on_press2(self, key):
        if key == keyboard.KeyCode.from_char('u'):
            self.stop = True
            self.key_listener2.stop()
            print("stopped")
            self.focus_window("Ghost Mouse")

def main():
    forget_all(root)
    user = app()
    print("main function")
    makeLable(f"\n\nWindow: {user.window}\n", 18)
    makeButton("Select Window", user.selectWindow, wi=20)
    makeButton("Record", user.record, wi=20)
    makeButton("Play", user.play, wi=20)
    makeButton("Opions", options, hi= 1, wi=20)
    tk.Label(root, text='\n\n\nDeveloped By Thomas Gomez @https://github.com/BruzaTom', fg=lablelc, bg="#333333", font=("Arial", 10, "bold")).pack()
    root.mainloop()

def options():
    forget_all(root)
    makeLable(f"\n\nOptions\n", 18)
    
    if new_step == False:
        makeButton(f"New step: OFF\nTurn ON?", new_step_on, wi=20)
    if new_step == True:
        makeButton(f"New step: ON\nTurn Off?", new_step_off, wi=20)
        makeButton(f"Choose lap", choose_lap, wi=20)
    makeButton(f"Home", main, wi=20)

def choose_lap():
    forget_all(root)
    global lap
    makeLable(f"\n\nWhich lap would you\nlike to activate on?\n", 18)
    answer = tk.Entry(root, insertwidth=6, font=font_style)
    answer.pack()
    def submit_lap():
        global lap
        lap = answer.get().strip()  # Get user input when they click Submit
        if lap.isdigit():
            lap = int(lap)  # Convert to an integer if valid
            print(f"Lap selected: {lap}")  # Debugging step
        else:
            print("Error: Invalid lap entry!")
        options()
        with open(file3, "w") as f:
            f.write(f"[True, {lap}]")  # Write default content
        print(f"updated '{file3}' - [True, {lap}]")
    makeButton(f"Submit", submit_lap, wi=20)

def new_step_on():
    forget_all(root)
    user = app2()
    global new_step
    global lap
    if [] in getLst(file2):
        makeLable(f"\n\nThe new actions file is empty..\n", 18)
        makeButton(f"Record new actions for step", user.record, wi=20)
        makeButton(f"Options", options, wi=20)
        makeButton(f"Home", main, wi=20)
        new_step = True
    else:
        makeLable(f"\n\nFound actions for a new step.\n", 18)
        makeButton(f"Use existing", choose_lap, wi=20)
        makeButton(f"Record new actions", user.record, wi=20)
        makeButton(f"Options", options, wi=20)
        makeButton(f"Home", main, wi=20)
        new_step = True

def new_step_off():
    forget_all(root)
    global new_step
    new_step = False
    with open(file3, "w") as f:
        f.write(f"[False, 0]")  # Write default content
    print(f"updated '{file3}' - [False, 0]")
    makeLable(f"\n\nAdditional step\nturned Off.\n", 18)
    makeButton(f"Options", options, wi=20)
    makeButton(f"Home", main, wi=20)

def updateFile(Lst, file):
    with open(file, "w") as f:
        f.write(str(Lst))

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