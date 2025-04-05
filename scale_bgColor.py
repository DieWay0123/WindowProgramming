import tkinter as tk

def update_color(*args):
    r = red_scale.get()
    g = green_scale.get()
    b = blue_scale.get()
    color = f'#{r:02x}{g:02x}{b:02x}'  # Convert to hex color
    root.config(bg=color)

root = tk.Tk()
root.title("Color Changer")
root.geometry("400x300")

scale_frame = tk.LabelFrame(root, width=10, height=10, text="Color Change")
scale_frame.pack(padx=10, pady=10, expand=True, anchor='n')
# Create scales for Red, Green, and Blue
red_scale = tk.Scale(scale_frame, from_=0, to=255, orient=tk.VERTICAL, label='Red', command=update_color)
red_scale.grid(row=0, column=0)

green_scale = tk.Scale(scale_frame, from_=0, to=255, orient=tk.VERTICAL, label='Green', command=update_color)
green_scale.grid(row=0, column=1)

blue_scale = tk.Scale(scale_frame, from_=0, to=255, orient=tk.VERTICAL, label='Blue', command=update_color)
blue_scale.grid(row=0, column=2)

# Set initial background color
update_color()

root.mainloop()