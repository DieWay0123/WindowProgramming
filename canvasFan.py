import tkinter as tk
import math

class RotatingSectorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("旋轉的扇形")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.center = (200, 200)
        self.radius = 100
        self.angle = 0  # 初始角度
        self.sector_count = 3
        self.sector_angle = 60
        self.gap = 60
        self.colors = ["red", "green", "blue"]

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        for i in range(self.sector_count):
            start = self.angle + i*(self.sector_angle+self.gap)
            self.draw_sector(self.center[0], self.center[1], self.radius, start, self.sector_angle, self.colors[i])
        self.angle = (self.angle + 2) % 360
        self.root.after(2, self.update_canvas)

    def draw_sector(self, x, y, r, start, extent, color):
        # 扇形是用 canvas.arc 的方式畫出
        self.canvas.create_arc(
            x - r, y - r, x + r, y + r,
            start=start, extent=extent,
            fill=color, outline='black'
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RotatingSectorsApp(root)
    root.mainloop()
