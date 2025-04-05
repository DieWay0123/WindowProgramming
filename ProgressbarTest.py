import tkinter as tk
import tkinter.ttk as ttk
import time

"""
pb_val = 0
pb_flag = False
def running():
  global pb_val
  global pb_flag

  pb_flag = True
  for val in range(pb_val, 100, 1):
    if pb_flag == False:
      break
    print(pb_val)
    pb_val = val
    pb['value'] = val
    root.update()
    time.sleep(0.1)
  
def stop():
  global pb_flag
  pb_flag = False
"""
def running():
  pb.start()
def stop():
  pb.stop()

root = tk.Tk()

pb = ttk.Progressbar(root, length=200, orient='horizontal')
pb.pack(padx=10, pady=10)

run_btn = tk.Button(root, text="start", command=running)
stop_btn = tk.Button(root, text="stop", command=stop)

run_btn.pack(padx=10, pady=10)
stop_btn.pack(padx=10, pady=10)

def ctrlF(self):
  print("ctrl+f pressed")
  
root.bind('<Control-f>', ctrlF)

root.mainloop()