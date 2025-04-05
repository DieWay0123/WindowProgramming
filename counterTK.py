from tkinter import *
import time

root = Tk()
screenWidth = root.winfo_screenmmwidth()
screenHeight = root.winfo_screenheight()
print(f"{screenWidth},{screenHeight}")
root.geometry(f"{screenWidth}x{screenHeight}+0+0")
lb = Label(root, text="test123", height=3, width=15, background='yellow', foreground='black', anchor='s')
lb.pack()

count = 0
def count_time():
  global count
  count += 1
  if count > 10:
    count = 0
  lb.config(text=str(count))
  lb.after(1000, count_time)
# root.attributes('-fullscreen', True)
count_time()
root.mainloop()