import tkinter as tk

def sel():
  entry.selection_range(0, tk.END)
def cancel_sel():
  entry.selection_clear()
def del_sel():
  entry.delete(0, tk.END)
def sel_readonly():
  if read_only.get() == True:
    entry.config(state=tk.DISABLED)
  else:
    entry.config(state=tk.NORMAL)

root = tk.Tk()
entry = tk.Entry(root)
entry.grid(row=0, column=0, columnspan=4)
button1 = tk.Button(root, text="選取全部", command=sel).grid(row=1, column=0)
button2 = tk.Button(root, text="刪除選取", command=cancel_sel).grid(row=1, column=1)
button3 = tk.Button(root, text="取消選取", command=del_sel).grid(row=1, column=2)
button4 = tk.Button(root, text="結束", command=root.destroy).grid(row=1, column=3)

read_only = tk.BooleanVar()
checkbox1 = tk.Checkbutton(text="readonly", variable=read_only, command=sel_readonly)
checkbox1.grid(row=2, column=0)



root.mainloop()
