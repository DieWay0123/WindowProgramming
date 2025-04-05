import tkinter as tk
from tkinter import font
from tkinter import ttk

def change_fontsize(event):
  print("123")
  size = combo_var.get()
  f = ("Arial", size)
  #ft = font(size=size)
  #f = tk.font(size=size)
  lb.config(font=f)
def change_color(*args):
  lb.config(background=op_var.get())
def add_lb():
  if entry.get():
    lb.insert(tk.END, entry.get())
    entry.delete(0, tk.END)
  return
def delete_lb():
  for i in lb.curselection()[::-1]:
    lb.delete(i)
  return
root = tk.Tk()

combo_var = tk.StringVar()
op_var = tk.StringVar()
op_value = ["Red", "Green", "Blue"]

entry = tk.Entry(root)
add_btn = tk.Button(root, text="ADD", command=add_lb)
del_btn = tk.Button(root, text="DEL", command=delete_lb)
lb = tk.Listbox(root)
option = tk.OptionMenu(root, op_var, *op_value)
comboBox = ttk.Combobox(root, textvariable=combo_var, state="readonly")

comboBox["value"] = (8, 12, 16, 20, 24, 32)

entry.grid(row=0, column=0)
add_btn.grid(row=0, column=1)
del_btn.grid(row=0, column=2)
lb.grid(row=1, column=0)
option.grid(row=2, column=0)
comboBox.grid(row=3, column=0)

op_var.trace_add(mode="write", callback=change_color)
comboBox.bind("<<ComboboxSelected>>", change_fontsize)
root.mainloop()