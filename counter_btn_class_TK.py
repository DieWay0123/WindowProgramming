import tkinter as tk

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("200x150")
        self.root.title("計時器")

        self.is_running = False
        self.counter = 0

        self.label = tk.Label(root, text="0", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Counter", command=self.toggle_timer)
        self.button.pack()

        self.update_timer()
        self.root.mainloop()

    def update_timer(self):
        if self.is_running:
            self.counter += 1
            self.label.config(text=str(self.counter))
        self.root.after(1000, self.update_timer)  # 每隔一秒更新一次計時器

    def toggle_timer(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.button.config(text="Stop")
        else:
            self.button.config(text="Counter")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    