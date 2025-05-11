import tkinter as tk

class test(tk.Tk):
    def __init__(self):
        self.creat_gui()
        
    def creat_gui(self):
        ARTICLE_FG = "#ffffff"
        ARTICLE_BG = "#2c3e50"
        ENTRY_BG = "ecf0f1"
        BUTTON_COLOR = "#3498db"
        BUTTON_TEXT = "#ffffff"
        FONT = ("Arial", 14)
        
        # frame版面管理
        self.race_car_frame = tk.Frame(self)
        self.text_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        
        self.race_car_frame.grid(column=0, row=0, sticky="ew")
        self.text_frame.grid(column=0, row=1, sticky="nsew")
        self.bottom_frame.grid(column=0, row=2, sticky="nsew")
        self.configure(bg="#ecf0f1")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        # 設定 Canvas 作為賽道進度條底圖
        self.track_canvas = tk.Canvas(self.race_car_frame, height=80, bg="#eeeae7", highlightthickness=0, border=1, relief=GROOVE)
        self.track_canvas.grid(row=0, column=0, sticky="ew", pady=0, padx=5)
        self.race_car_frame.columnconfigure(0, weight=1)
        # 調整視窗時，動態更新終點與起點位置
        self.track_canvas.bind("<Configure>", self.resize_progress_bar)
        
if __name__ == 'main':
    app = tk.Tk()
    root = test()
    root.mainloop()
    