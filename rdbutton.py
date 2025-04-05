import tkinter as tk
from PIL import Image, ImageTk

cities = {0:"美國", 1:"德國", 2:"香港"}

root = tk.Tk()
img_us = ImageTk.PhotoImage(Image.open('./united-states.png').resize((50, 50)))
img_gz = ImageTk.PhotoImage(Image.open('./germany.png').resize((50, 50)))
img_hk = ImageTk.PhotoImage(Image.open('./hong-kong.png').resize((50, 50)))

result = tk.StringVar()
selecetd_country_label = tk.Label(textvariable=result, bg='lightyellow', fg='blue').grid(row=0, column=0, padx=10, pady=5)
rd_button1 = tk.Radiobutton(root, text="美國", image=img_us, variable=result, compound=tk.RIGHT, indicatoron=0, value="美國").grid(row=1, column=0, padx=10, pady=5, sticky='ew')
rd_button2 = tk.Radiobutton(root, text="德國", image=img_gz, variable=result, compound=tk.RIGHT, indicatoron=0, value="德國").grid(row=2, column=0, padx=10, pady=5, sticky='ew')
rd_button3 = tk.Radiobutton(root, text="香港", image=img_hk, variable=result, compound=tk.RIGHT, indicatoron=0, value="香港").grid(row=3, column=0, padx=10, pady=5, sticky='ew')

root.grid_columnconfigure(0, weight=1)  # Column 0 will expand

root.mainloop()