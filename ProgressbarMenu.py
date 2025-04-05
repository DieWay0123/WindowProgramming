import tkinter as tk
from tkinter import ttk

root = tk.Tk()

progress_bar = ttk.Progressbar(root, length=300, mode='determinate', orient='horizontal')
progress_bar.pack(pady=10)

def start_progress():
  progress_bar.start()
def stop_progress():
  progress_bar.stop()
def change_color(color):
  print(color)
  progress_bar.config(style=f"{color}.Horizontal.TProgressbar")
def change_mode(mode):
  progress_bar.config(mode=mode)

style = ttk.Style()
style.configure("Red.Horizontal.TProgressbar", troughcolor='red', background='red')
style.configure("Green.Horizontal.TProgressbar", troughcolor='green', background='green')
style.configure("Blue.Horizontal.TProgressbar", troughcolor='blue', background='blue')
menu_bar = tk.Menu(root)

function_menu = tk.Menu(menu_bar, tearoff=0)
function_menu.add_command(label="Start Progress", command=start_progress)
function_menu.add_command(label="Stop Progress", command=stop_progress)
function_menu.add_separator()
function_menu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="Function", menu=function_menu)

appearance_menu = tk.Menu(menu_bar, tearoff=0)
appearance_menu.add_command(label="Red", command=lambda: change_color("Red"))
appearance_menu.add_command(label="Green", command=lambda: change_color("Green"))
appearance_menu.add_command(label="Blue", command=lambda: change_color("Blue"))
menu_bar.add_cascade(label="Appearance", menu=appearance_menu)

Mode_menu = tk.Menu(menu_bar, tearoff=0)
Mode_menu.add_command(label="Normal", command=lambda: change_mode("determinate"))
Mode_menu.add_command(label="Indeterminate", command=lambda: change_mode("indeterminate"))
menu_bar.add_cascade(label="Mode", menu=Mode_menu)

root.config(menu=menu_bar)

root.mainloop()