from tkinter import *
import time

root = Tk()
screenWidth = root.winfo_screenmmwidth()
screenHeight = root.winfo_screenheight()
print(f"{screenWidth},{screenHeight}")
root.geometry("500x500")
lb = Label(root, text="test123", height=10, width=10, background='yellow', foreground='black')
lb.pack()

count = 0

def is_count():
  if btn_counter['text']=='Counter':
    btn_counter['text'] = 'Stop' #btn.config(text='Stop')
  elif btn_counter['text']=='Stop':
    btn_counter['text'] = 'Counter'

def count_time():
  global count
  if btn_counter['text']=='Counter':
    lb.after(1000, count_time)
    return
  count += 1
  lb.config(text=str(count))
  lb.after(1000, count_time)

btn_counter = Button(text='Counter', command=is_count)
btn_close = Button(text='Close Window', command=root.destroy)
count_time()
# root.attributes('-fullscreen', True)

lb.grid(row=0, column=0, columnspan=2, sticky=N+S+W+E)
btn_counter.grid(row=1, column=0, sticky=W+E)
btn_close.grid(row=1, column=1, sticky=W+E)
root.mainloop()