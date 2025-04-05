import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

def msg():
  messagebox.showinfo("HI", "HI!HI!HI!")

root = tk.Tk()

notebook = ttk.Notebook(root)
f1 = tk.Frame()
f2 = tk.Frame()

l = tk.Label(f1, text="Hello")
l.pack(padx=10, pady=10)

b = tk.Button(f2, text="Hi", command=msg)
b.pack(padx=10, pady=10)

notebook.add(f1, text="page 1")
notebook.add(f2, text="page 2")
notebook.pack(padx=10, pady=10, expand=True, fill="both")

root.mainloop()