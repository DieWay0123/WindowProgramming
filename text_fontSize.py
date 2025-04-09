import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

def changeFontSize(event):
    text_selected = text_block.tag_ranges("sel")
    if "sel_block" in text_block.tag_names():
        text_block.tag_delete("sel_block")
    if text_selected:
        f = Font(size=sizeVar.get())
        st, end = text_selected
        text_block.tag_add("sel_block", st, end)
        text_block.tag_configure("sel_block", font=f)
    else:
        f = Font(size=sizeVar.get())
        text_block.configure(font=f)


root = tk.Tk()

sizeVar = tk.IntVar()
cbBox = ttk.Combobox(root, textvariable=sizeVar)
sizeFamily = [x for x in range(8, 31)]
cbBox['value'] = sizeFamily
cbBox.bind("<<ComboboxSelected>>", changeFontSize)
cbBox.pack()

text_block = tk.Text(root, width=10, height=10)
text_block.insert(1.0, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
text_block.pack()
root.mainloop()