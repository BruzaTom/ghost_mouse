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
file = "ghost_data.txt"

def getLst(file):
    dictLst = []
    with open(file) as f: 
        data = f.read()
    dictLst = ast.literal_eval(data)
    return dictLst

class terminal:
    def __init__(self):
        self.root2 = tk.Tk()
        self.root2.title("ghost_terminal")
        self.root2.geometry("300x400+100+100")
        self.root2.overrideredirect(True) #make borderless and click-through
        self.root2.attributes("-transparentcolor", "white")
        self.root2.wm_attributes("-topmost", True)
        self.root2.attributes("-alpha", 0.7)
        self.row = 0
        self.hwnd = ctypes.windll.user32.GetParent(self.root2.winfo_id())
        exstyle = ctypes.windll.user32.GetWindowLongW(self.hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(self.hwnd, -20, exstyle | 0x00080000 | 0x00000020)

    def term_lable(self, string):
        label = tk.Label(self.root2, text=string, font=("Arial", 10), fg = green)
        label.grid(row=self.row, column=0, padx=10, pady=10)
        self.row += 1

    def lift(self):
        self.root2.lift()

class app:
    def __init__(self, file):
        self.file = file
        self.data = getLst(file)
        self.recorded_actions = self.data[1]
        print(f"recorded actions: {self.recorded_actions}")
        self.window = self.data[0]
        print(f"window: {self.window}")
        self.user_poses = []
        self.time_stamps = self.data[2]
        print(f"time stamps: {self.time_stamps}")
        self.timer = 0.0
        self.start_time = 0.0
        self.ctrl_pressed = False
        self.stop = False
        self.mouse_listener = None
        self.key_listener = None
        self.key_listener2 = None

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

    def play_back(self, actions, window_title, repetitions):
        self.focus_window(window_title)
        #transperant = terminal()
        self.key_listener2 = keyboard.Listener(on_press=self.on_press2)
        self.key_listener2.start()
        for t in range(repetitions):
            #transperant.lift()
            if self.stop:
                forget_all(root)
                main()
            print(t)
            i = 0
            for action, pos in actions:
                time.sleep(self.time_stamps[i])
                #mouse_pos = autoit.mouse_get_pos() # back to user position
                if self.stop == False:
                    time.sleep(0.08)
                    if action == 'left_click':
                        autoit.mouse_move(pos[0], pos[1], speed=0)
                        time.sleep(0.08)
                        autoit.mouse_click('left', pos[0], pos[1])
                        print(f"left Clicked at {pos}")
                    if action == 'right_click':
                        autoit.mouse_move(pos[0], pos[1], speed=0)
                        time.sleep(0.08)
                        autoit.mouse_click('right', pos[0], pos[1])
                        print(f"right Clicked at {pos}")
                    #autoit.mouse_move(mouse_pos[0], mouse_pos[1], speed=0) # back to user position
                    i += 1
                else:
                    forget_all(root)
                    main()
            time.sleep(self.time_stamps[i])

    def play(self):
        repetitions = 1000
        self.focus_window(self.window)
        self.play_back(self.recorded_actions, self.window, repetitions)
        

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
    user = app("ghost_data.txt")
    print("main function")
    makeLable(f"\n\nWindow: {user.window}\n", 18)
    makeButton("Select Window", user.selectWindow, wi=20)
    makeButton("Record", user.record, wi=20)
    makeButton("Play", user.play, wi=20)
    tk.Label(root, text='\n\n\nDeveloped By Thomas Gomez @https://github.com/BruzaTom', fg=lablelc, bg="#333333", font=("Arial", 10, "bold")).pack()
    root.mainloop()
    

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