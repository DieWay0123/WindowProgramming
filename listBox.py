import tkinter as tk

def click_add():
  item = entry.get()
  if item:
    lb_A.insert(tk.END, item)
    entry.delete(0, tk.END)
def move_A_B():
  indexes = lb_A.curselection()
  for i in reversed(indexes):
    lb_B.insert(tk.END, lb_A.get(i))
    lb_A.delete(i)
def move_B_A():
  indexes = lb_B.curselection()
  for i in reversed(indexes):
    lb_A.insert(tk.END, lb_B.get(i))
    lb_B.delete(i)
root = tk.Tk()

lb_var_A = tk.StringVar()
lb_var_B = tk.StringVar()

entry = tk.Entry(root)
add_btn = tk.Button(root, text="Add", command=click_add)
move_A_B_btn = tk.Button(root, text="Move A to B", command=move_A_B)
move_B_A_btn = tk.Button(root, text="Move B to A", command=move_B_A)
lb_A = tk.Listbox(root, listvariable=lb_var_A, selectmode="extended")
lb_B = tk.Listbox(root, listvariable=lb_var_B, selectmode="extended")

entry.grid(row=0, column=0)
add_btn.grid(row=0, column=1, padx=20)
lb_A.grid(row=1, column=0, pady=10)
lb_B.grid(row=1, column=2, pady=10)
move_A_B_btn.grid(row=2, column=1, pady=10, padx=5)
move_B_A_btn.grid(row=2, column=3, pady=10, padx=5)

#event

root.mainloop()

"""
def move_item(lb_from, lb_to):
  indexes = lb_from.curseselection()
  for i in indexes[::-1]:
    lb_to.insert(tk.END, lb_from.get(i))
    lb_from.delete(i)

lambda: move_item(listboxA, listboxB)
"""