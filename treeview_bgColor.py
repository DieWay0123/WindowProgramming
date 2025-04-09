import tkinter as tk
from tkinter import ttk

root = tk.Tk()
tree = ttk.Treeview(root, columns=("States", "Cities"))
tree.heading("#0", text="State")
tree.heading("#1", text="City")

tree.column("#0", anchor='center')
tree.column("#1", anchor='center')

tree_dict = {
    "Taipei": "Shilin",
    "Taichung": "Tanzi",
    "Taoyuan": "AAA"
}

idx = 0
for k, val in tree_dict.items():
    if idx&1:
        tree.insert("", index=tk.END, text=k, values=val, tag="color")
    else:
        tree.insert("", index=tk.END, text=k, values=val)
    idx += 1

tree.tag_configure("color", background="lightgreen")
tree.pack()
root.mainloop()