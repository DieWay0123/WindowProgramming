import tkinter as tk
import time

def Run():
  print(f"{color.get()} Set")
  if cbox_check1.get() == 1:
    print("Bold Set")
  if cbox_check2.get() == 1:
    print("Italics Set")
  print(f"Name: {name.get()}")

root = tk.Tk()

color = tk.StringVar(None, "Lightblue")
rd_btn1 = tk.Radiobutton(root, text="Lightblue", variable=color, value="Lightblue").grid(row=0, column=0)
rd_btn2 = tk.Radiobutton(root, text="Lightgreen", variable=color, value="Lightgreen").grid(row=0, column=1)

cbox_check1 = tk.IntVar()
cbox_check2 = tk.IntVar() 
checkbox1 = tk.Checkbutton(root, text="Bold", variable=cbox_check1).grid(row=1, column=0)
checkbox2 = tk.Checkbutton(root, text="Italics", variable=cbox_check2).grid(row=1, column=1)

name = tk.StringVar()
label = tk.Label(root, text="Input").grid(row=2, column=0)
name_entry = tk.Entry(root, textvariable=name).grid(row=2, column=1)
btn = tk.Button(root, text="Run", command=Run).grid(row=2, column=2)

root.mainloop()