import tkinter as tk
from tkinter import *

class Tk_Container:
    def __init__(self, window=None):
        if window is None:
            self.window = tk.Tk()
        else:
            self.window = window
    
    def start(self):
        self.window.mainloop()
