import tkinter as tk

root = tk.Tk()

frame_bg = {0:"pink", 1:"green", 2:"brown"}
radio_frame = tk.Frame(root, bg='pink')
radio_frame.pack()
radio_selected = tk.StringVar()
for i, k in frame_bg.items():
  btn = tk.Radiobutton(radio_frame, text=k, variable=radio_selected, value=k)
  btn.grid(row=0, column=i)
change_frame=tk.Frame()

root.mainloop()