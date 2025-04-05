import tkinter as tk

root = tk.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"{screenWidth}x{screenHeight}")
root.resizable(0, 0)

colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

for index, color in enumerate(colors):
    tk.Label(root, text=color, relief="groove", width=20).grid(column=0, row=index)
    tk.Label(root, background=color, relief="ridge", width=20).grid(column=1, row=index)
    '''
    color_txt = tk.Label(root, text=color, borderwidth=2, width=10)
    color_lbl = tk.Label(root, background=color, width=10)
    color_txt.grid(column=0, row=index)
    color_lbl.grid(column=1, row=index)
    '''
root.mainloop()

btn = tk.Button()
print(dir(btn))