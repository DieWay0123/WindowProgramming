import tkinter as tk

def show_coordinates(event):
    coord_label.config(text=f"X: {event.x}, Y: {event.y}")
def enter_coordinates(event):
    enter_coord_label.config(text=f"Enter X: {event.x}, Y: {event.y}")
def leave_coordinates(event):
    leave_coord_label.config(text=f"Leave X: {event.x}, Y: {event.y}")

root = tk.Tk()
root.geometry("400x300")

coord_label = tk.Label(root, text="x: -, y: -", font=("Arial", 12))
coord_label.pack(pady=5)

enter_coord_label = tk.Label(root, text="Enter X: , Y: ")
enter_coord_label.pack()

leave_coord_label = tk.Label(root, text="Leave X: , Y: ")
leave_coord_label.pack()

# Bind mouse motion event to update coordinates
root.bind('<Motion>', show_coordinates)
root.bind('<Enter>', enter_coordinates)
root.bind('<Leave>', leave_coordinates)

root.mainloop()
