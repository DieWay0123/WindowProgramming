import tkinter as tk
from tkinter import messagebox
import random

class TypeBeatTrainerWindow():
    def __init__(self, root: tk.Tk):
        self.root = root
        self.original_menu = self.root["menu"]
        self.root.config(menu="")
        
        self.root.title("TypeBeat Rhythm!")
        self.root.geometry("1400x400")
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill="both")
        
        self.bpm = 60
        self.miss_count = 0
        self.score = 0
        self.max_miss = 3
        self.running = False
        self.beats = []
        self.mode = tk.StringVar(value="symbols")
        
        self.symbol_sets = {
            "symbols": list(".,?!:;\"'@#$&*()[]{}\\/-=+"),
            "alphabet": list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
            "mixed": list(".,?!:;\"'@#$&*()[]{}\\/-=+" + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        }
        self.create_widgets()
        self.root.bind("<Key>", self.keypress_input)
        
    def create_widgets(self):
        self.control_frame = tk.LabelFrame(self.frame, text="🎮 Controls", bg="#dbe9f4", fg="#1f3b4d", font=("Helvetica", 14, "bold"), bd=3, relief="ridge")
        self.control_frame.pack(side="left", padx=10, pady=10, fill="y")
        
        tk.Label(self.control_frame, text="Generating Speed:", font=("Arial", 12), bg="#dbe9f4", fg="#333").pack(pady=(10, 0))
        self.bpm_scale = tk.Scale(self.control_frame, from_=60, to=100, orient="horizontal", command=self.set_bpm)
        self.bpm_scale.set(self.bpm)
        self.bpm_scale.pack()
        
        tk.Label(self.control_frame, text="Training Mode:", font=("Arial", 12), bg="#dbe9f4", fg="#333").pack(pady=(10, 0))
        modes = [("Symbols", "symbols"), ("Alphabet", "alphabet"), ("Mixed", "mixed")]
        for label, value in modes:
            tk.Radiobutton(self.control_frame, text=label, variable=self.mode, value=value, bg="#dbe9f4", fg="#1f3b4d", selectcolor="#ffffff").pack(anchor="w", padx=10)
        
        self.start_button = tk.Button(self.control_frame, text="▶ Start", command=lambda: self.start_game(n=3), bg="#4caf50", fg="white", font=("Arial", 12, "bold"), relief="raised")
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(self.control_frame, text="⏪ Back to Menu", command=self.back_to_menu, bg="#f44336", fg="white", font=("Arial", 12, "bold"), relief="raised")
        self.back_button.pack(pady=5)

        # 紀錄分數&失誤標籤
        score_frame = tk.Frame(self.control_frame, bg="#f0f4f0") # 新增一個score_frame專門拿來放這兩個標籤
        score_frame.pack(pady=5)
        self.score_label = tk.Label(score_frame, text="Score: 0", font=("Arial", 12, "bold"), bg="#f0f4f0", fg="#68be8d")
        self.miss_label = tk.Label(score_frame, text="Miss: 0", font=("Arial", 12, "bold"), bg="#f0f4f0", fg="#ba2636")        
        self.score_label.pack(side="left", padx=5)
        self.miss_label.pack(side="left", padx=5)

        # 遊戲區塊
        self.game_frame = tk.Frame(self.frame, bg="#ffffff", relief="sunken", bd=2)
        self.game_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.canvas = tk.Canvas(self.game_frame, bg="#222831")
        self.canvas.pack(expand=True, fill="both")

        self.root.after(100, self.update_canvas_size)
        
    def update_canvas_size(self):
        # 調整設定畫面文字判定線位置
        self.canvas.delete("judge")
        self.canvas.delete("track")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.judge_line = w // 20
        
        # 畫出整條軌道區域（背景陰影）
        track_top = h // 2 - 20
        track_bottom = h // 2 + 20
        self.track = self.canvas.create_rectangle(
            self.judge_line - 10, track_top, 
            w , track_bottom, 
            fill="#1e1e1e", outline="#444", width=2, tags="track"
        )
        
        # 判定區塊
        box_lenth = 40
        self.hitbox = self.canvas.create_rectangle(
            self.judge_line - 10 , h // 2 - box_lenth // 2,
            self.judge_line + box_lenth - 10, h // 2 + box_lenth // 2,
            outline="white", fill="white", width=2, tags="judge"
        )
        
        
    def set_bpm(self, val):
        self.bpm = int(val)
        
    def start_game(self, n):
        self.score = 0
        self.canvas.delete("gameover")
        self.canvas.delete("countdown")
        self.disable_controls()

        # 遊戲開始倒數
        if n == 0:
            self.running = True
            self.beats = []
            self.miss_count = 0
            self.score_label.config(text="Score: 0")
            self.miss_label.config(text="Miss: 0")
            self.canvas.delete("beat")
            self.current_set = self.symbol_sets[self.mode.get()]
        
            self.spawn_beat()
            self.move_beats()
        else:
            self.canvas.create_text(
                    self.canvas.winfo_width()//2,
                    self.canvas.winfo_height()//2,
                    text=str(n), font=("Arial", 60, "bold"), fill="white", tags="countdown")
            self.canvas.after(1000, lambda: self.start_game(n-1))
        
    def spawn_beat(self):
        if not self.running:
            return
        
        symbol = random.choice(self.current_set)
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        y = h // 2
        
        # 畫出要輸入文字的圖形
        text_id = self.canvas.create_text(w + 30, y, text=symbol, font=("Arial", 24), fill="black", tags="beat", anchor="center")
        box_width = 60
        box_height = 60
        radius = 10
        x1 = w
        y1 = y - box_height // 2
        x2 = w + box_width
        y2 = y + box_height // 2
        rounded_rect = self.canvas.create_polygon(
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            smooth=True,
            outline="black", fill="#fffaf4", width=2, tags="beat")
        text_box = rounded_rect
        
        self.canvas.tag_lower(self.track)
        self.canvas.tag_raise(text_id, text_box)
        
        self.beats.append(((text_box, text_id), symbol))
        
        # 計算每隔一段時間(bpm)就生成新的文字
        interval = int(60000 / (self.bpm*2))
        self.root.after(int(interval*3), self.spawn_beat)
        
    def move_beats(self):
        if not self.running:
            return
    
        for (box, item_id), _ in list(self.beats):
            if len(list(self.beats)) == 0:
                continue
            self.canvas.move(box, -4, 0)
            self.canvas.move(item_id, -4, 0)
            x, y = self.canvas.coords(item_id)
            # 處理若文字漏打超過判定線
            if x < self.judge_line - 10:
                self.canvas.delete(item_id)
                self.canvas.delete(box)
                self.beats = [b for b in self.beats if b[0][1] != item_id]
                self.show_feedback("Miss!", "#ff5555")
                self.miss_count += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.miss_label.config(text=f"Miss: {self.miss_count}")
                if self.miss_count >= self.max_miss:
                    self.end_game()
        self.root.after(10, self.move_beats)
        
    # 命中或miss的回饋
    def show_feedback(self, text, color):
        label = self.canvas.create_text(self.judge_line, self.canvas.winfo_height()//2 - 70, 
                                        text=text, font=("Arial", 20, "bold"), 
                                        fill=color, tags="feedback")
        self.canvas.after(500, lambda: self.canvas.delete(label))
        
    def flash_hitbox(self, color="#00ff88"):
        h = self.canvas.winfo_height()
        box_height = 60
        box_width = 60
        x1 = (self.judge_line - box_width // 2) + 10
        y1 = h // 2 - box_height // 2
        x2 = (self.judge_line + box_width // 2) + 10
        y2 = h // 2 + box_height // 2

        flash_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0, tags="flash")
        self.canvas.tag_raise(flash_rect)
        self.root.after(100, lambda: self.canvas.delete(flash_rect))    
    
    def keypress_input(self, event):
        user_input = event.char
        if not user_input or not self.running:
            return
        
        # 判斷是否有打中
        for (box, text), symbol in self.beats:
            x, _ = self.canvas.coords(text)
            x_judge_line_dis = abs(x - self.judge_line)
            if x_judge_line_dis <= 45 and user_input == symbol:
                self.show_feedback("Perfect!", "#00ff88")
                self.flash_hitbox(color="#00ff88")
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.miss_label.config(text=f"Miss: {self.miss_count}")
                self.canvas.delete(text)
                self.canvas.delete(box)
                self.beats = [b for b in self.beats if b[0][1] != text]
                return
            elif x_judge_line_dis <= 100: # 在45~100範圍按下會是miss
                # 沒打中就計算miss+1
                self.show_feedback("Miss!", "#ff5555")
                self.flash_hitbox(color="#ff5555")
                self.miss_count += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.miss_label.config(text=f"Miss: {self.miss_count}")
                self.beats = [b for b in self.beats if b[0][1] != text] 
                self.canvas.delete(text)
                self.canvas.delete(box)
                if self.miss_count >= self.max_miss:
                    self.end_game()
                return 
    
    def end_game(self):
        self.running = False
        self.canvas.delete("beat")
        self.beats.clear()
        # 顯示 Game Over 動畫文字
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        label = self.canvas.create_text(
            w // 2, h // 2,
            text="GAME OVER", font=("Arial", 48, "bold"), fill="#ff4444", tags="gameover")

        def flash(count=0):
            if count < 6:
                current_color = "#ff4444" if count % 2 == 0 else "#f0f4f0"
                self.canvas.itemconfig(label, fill=current_color)
                self.canvas.after(300, lambda: flash(count + 1))
            else:
                self.canvas.itemconfig(label, fill="#ff4444")

        flash()
        self.score_label.config(text=f"Game Over! Score: {self.score}")
        self.miss_label.config(text=f"")
        self.enable_controls()
        
    def disable_controls(self):
        self.bpm_scale.config(state="disabled")
        self.start_button.config(state="disabled")
        self.back_button.config(state="disabled")
        for child in self.control_frame.winfo_children():
            if isinstance(child, tk.Radiobutton):
                child.config(state="disabled")

    def enable_controls(self):
        self.bpm_scale.config(state="normal")
        self.start_button.config(state="normal")
        self.back_button.config(state="normal")
        for child in self.control_frame.winfo_children():
            if isinstance(child, tk.Radiobutton):
                child.config(state="normal")
        
    def back_to_menu(self):
        if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
            self.frame.destroy()
            if hasattr(self.root, "show_main_menu"):
                self.root.config(menu=self.original_menu)
                self.root.show_main_menu()
                
    def destroy(self):
        self.frame.destroy()