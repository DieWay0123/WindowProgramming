# multiplayer_game.py
import enum
import socket
import tkinter as tk
from tkinter import messagebox
import threading
import json
import time
import random
from turtle import left, width

from game import GameWindow

class MultiplayerGameWindow(GameWindow):
    def __init__(self, root, player_name, connection: socket.socket, is_host=False):
        self.player_name: str = player_name
        self.conn: socket.socket = connection
        self.conn.settimeout(1.0)
        self.player_id: str = f"{player_name}#{connection.getsockname()[1]}"
        self.is_host: bool = is_host
        
        self.players_progress: dict = {self.player_id: 0}
        self.players_car_ids: dict = {} # 小車的canvas id
        self.players_name_ids: dict = {} # 玩家名字的canvas id
        self.lock: threading.Lock = threading.Lock()
        self.ready_to_start = False
        self.game_over = False
        self.is_destroyed = False
        self.finish_order: list = [] # 紀錄完成順序
        self.left_players: set = set() # 紀錄中途離開的玩家
        
        super().__init__(root)
        if hasattr(self, "typing_entry"):
            self.typing_entry.config(state="disabled")
        
        self.countdown_label = tk.Label(self.bottom_frame, text="Waiting for game to start...", font=("Arial", 40), bg="#ecf0f1", fg="#444")
        self.countdown_label.pack()

        # 多人遊玩移除重新開始按鈕  
        if hasattr(self, "restart_button"):
            self.restart_button.destroy()

        threading.Thread(target=self.listen_for_updates, daemon=True).start()

    def start_countdown(self, seconds=3):
        def countdown():
            for i in range(seconds, 0, -1):
                self.countdown_label.config(text=f"Game starts in {i}...")
                time.sleep(1)
            self.countdown_label.config(text="Go!")
            self.typing_entry.config(state="normal")
            self.typing_entry.focus()

        self.typing_entry.config(state="disabled")
        threading.Thread(target=countdown, daemon=True).start()

    def create_progress_bar(self):
        canvas_height = max(100, 30 + len(self.players_progress)*30)
        self.track_canvas = tk.Canvas(
            self.race_car_frame, 
            bg="#eeeae7", 
            height=canvas_height, 
            highlightthickness=0,
            border=1,
            relief=tk.GROOVE
        )
        self.track_canvas.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        # self.race_car_frame.rowconfigure(0, weight=1)
        self.race_car_frame.columnconfigure(0, weight=1)
        self.track_canvas.bind("<Configure>", self.resize_progress_bar)

        self.add_or_update_car(self.player_id, self.player_name, is_self=True)

    def resize_progress_bar(self, event): # 更新全部車子位置
        self.finish_line_x = self.track_canvas.winfo_width() - 60
        
        # 隨視窗大小重新設定終點位置
        self.track_canvas.delete("finish_line")
        self.track_canvas.create_line(
            self.finish_line_x, 0, 
            self.finish_line_x, self.track_canvas.winfo_height(),
            fill="black", width=3, dash=(4, 4), tags="finish_line"
        )
        self.track_canvas.create_text(
            self.finish_line_x - 30, 10,
            text="🏁",
            font=("Arial", 20), tags="finish_line"
        )
    
        self.update_all_tracks()
        self.update_all_cars()

    def add_or_update_car(self, player_id, player_name, is_self=False):
        if player_id not in self.players_progress:
            self.players_progress[player_id] = 0
        if player_id not in self.players_car_ids:
            # 預設由x=10, y每個跑道佔50
            idx = len(self.players_car_ids)
            y = 50 + idx*50
            
            car_label =  "🏎️" if is_self else "🏍️"
            player_label = f"{player_name} (you)" if is_self else player_name
            color = '#800000' if is_self else "black"
            car_id = self.track_canvas.create_text(10, y+10, text=car_label, fill=color, anchor="w", font=("Arial", 32))
            name_id = self.track_canvas.create_text(10, y, text=player_label, anchor="w", font=("Arial", 12), fill="blue")
            
            self.players_car_ids[player_id] = car_id
            self.players_name_ids[player_id] = name_id
            
        self.update_all_tracks()
        self.update_remote_car(player_id=player_id)
    
    # 隨視窗或玩家人數更新調整賽道地板    
    def update_all_tracks(self):
        self.track_canvas.delete("track_line")
        car_count = len(self.players_car_ids)
        total_height = max(150, 50 + car_count * 50)
        self.track_canvas.config(height=total_height)
        
        for idx, player_id in enumerate(self.players_car_ids.keys()):
            y = 50 + idx*50
            x = self.track_canvas.coords(self.players_car_ids[player_id])[0]
            if player_id in self.players_name_ids:
                self.track_canvas.coords(self.players_name_ids[player_id], x, y)
            if player_id in self.players_car_ids:
                self.track_canvas.coords(self.players_car_ids[player_id], x, y + 10)
            self.track_canvas.create_line(
                0, y+30,
                self.track_canvas.winfo_width()-60, y+30,
                fill="black",
                dash=(5, 5),
                tags="track_line"
            )

    def on_space_press(self, event):
        typed_word = self.typing_entry.get().strip()
        if self.current_word_idx < len(self.target_words):
            if typed_word == self.target_words[self.current_word_idx]:
                self.typed_words.append(typed_word)
                self.current_word_idx += 1
                self.typing_entry.delete(0, tk.END)
                self.has_made_mistake = False
                self.render_article()
                self.auto_scroll_after_first_line_done()
                self.update_stats()
                self.update_local_car() # 與solo版不同之處
                self.send_progress() # 與solo版不同之處
                print(self.target_words)
                if self.current_word_idx >= len(self.target_words):
                    self.typing_entry.config(state="disabled")
                    self.update_stats(final=True)
        return "break"

    def send_progress(self):
        msg = {
            "type": "progress",
            "name": self.player_name,
            "player_id": self.player_id,
            "words": len(self.typed_words),
            "finished": self.current_word_idx == len(self.target_words)
        }
        self.send_json(msg)

    def send_json(self, data):
        try:
            msg = json.dumps(data).encode("utf-8")
            self.conn.sendall(msg + b"\n")
        except Exception:
            pass

    def listen_for_updates(self):
        buffer = ""
        while not self.is_destroyed:
            try:
                data = self.conn.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    try:
                        message = json.loads(line)
                        self.handle_message(message)
                    except:
                        continue
            except socket.timeout:
                continue
            except (ConnectionResetError, json.JSONDecodeError):
                if not self.is_destroyed and self.game_over:
                    self.root.after(0, lambda: messagebox.showerror("連線中斷", "與對手的連線已中斷。"))
                break

    def handle_message(self, msg):
        with self.lock:
            if self.is_destroyed:
                return             
            if msg["type"] == "progress": # host
                print("progress")
                player_id = msg["player_id"]
                name = msg["name"]
                self.players_progress[player_id] = msg["words"]
                self.add_or_update_car(player_id, name)
                # self.update_remote_car(player_id)
                
                if msg["finished"] and player_id not in self.finish_order:
                    self.finish_order.append(player_id)
                    if not self.game_over and len(self.finish_order) == len(self.players_progress):
                        self.game_over = True
                        self.show_results()
                
            elif msg["type"] == "introduce": # host
                print("introduce")
                name = msg["name"]
                player_id = msg["id"]
                self.add_or_update_car(player_id, name)
                if not self.ready_to_start:
                    self.ready_to_start = True
                    self.start_countdown()
                
            elif msg["type"] == "start": # join
                print("start")
                name = msg["host_player_name"]
                self.target_article: str = msg["text"]
                self.target_words = self.target_article.split()
                self.render_article()
                self.update_stats()
                self.update_all_tracks()
                self.update_all_cars()
                if not self.ready_to_start:
                    self.send_json({
                        "type": "introduce",
                        "name": self.player_name,
                        "id": self.player_id,
                    })
                    self.ready_to_start = True
                    self.start_countdown()
                    
            elif msg["type"] == "leave":
                print("leave")
                player_id = msg["id"]
                if player_id not in self.finish_order:
                    self.finish_order.append(player_id)
                    self.left_players.add(player_id)
                    self.check_game_over()

    def check_game_over(self):
        if not self.game_over and len(self.finish_order) == len(self.players_progress):
            self.game_over = True
            self.create_menu_bar()
            self.show_results()

    def update_local_car(self):
        self.players_progress[self.player_id] = len(self.typed_words)
        self.update_remote_car(self.player_id)
        
        # 若已完成，自己加入 finished_order
        if (
            not self.game_over and
            self.player_id not in self.finish_order and
            len(self.typed_words) == len(self.target_words)
        ):
            self.finish_order.append(self.player_id)
            if len(self.finish_order) == len(self.players_progress):
                self.game_over = True
                self.show_results()
        
    def update_all_cars(self):
        for player_id in self.players_progress:
            self.update_remote_car(player_id)
            
    # 依照名字取得
    def update_remote_car(self, player_id):
        if len(self.target_words) == 0 or player_id not in self.players_car_ids:
            return
        
        idx = list(self.players_car_ids.keys()).index(player_id)
        y_name = 50 + idx*50
        y_car = y_name + 10
        
        
        car = self.players_car_ids[player_id]
        name = self.players_name_ids[player_id]
        max_x = self.track_canvas.winfo_width() - 90
        progress_ratio = self.players_progress[player_id] / len(self.target_words) if len(self.target_words) >0 else 0
        
        # 位置計算
        car_current_coords = self.track_canvas.coords(car)
        car_current_x = car_current_coords[0]
        target_x = int(progress_ratio * max_x)
        steps = 10
        dx = (target_x - car_current_x) / steps
        
        def animate(step):
            if step >= steps:
                self.track_canvas.coords(car, target_x, y_car)
                self.track_canvas.coords(name, target_x ,y_name)
                return
            new_x = car_current_x + dx*step
            self.track_canvas.coords(car, new_x, y_car)
            self.track_canvas.coords(name, new_x, y_name)
            self.track_canvas.after(15, lambda: animate(step + 1))
            
        if player_id in self.players_name_ids and player_id in self.players_car_ids:
            animate(0)

    def show_results(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Game Results")
        WINDOW_WIDTH = 500
        WINDOW_HEIGHT = 500
        result_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        result_window.resizable(False, False)

        # 畫面顯示在螢幕正中間
        screen_width = result_window.winfo_screenwidth()
        screen_height = result_window.winfo_screenheight()
        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        result_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        result_window.configure(bg="#f8f9fa")
        
        title_label = tk.Label(result_window, text="🏁 Game Over! Results", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#333")
        title_label.pack(pady=10)
        
        # 結算彩帶動畫
        confetti = []
        confetti_anim_id = [None] #保存彩帶canvas物件的id 後續停止使用
        canvas = tk.Canvas(result_window, bg="#f8f9fa", highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        def create_confetti():
            canvas.update_idletasks()
            for _ in range(30):
                x = random.randint(0, max(50, 400))
                y = random.randint(-100, 0)
                color = random.choice(["#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6"])
                shape = canvas.create_oval(x, y, x+6, y+6, fill=color, outline="")
                confetti.append(shape)

        def animate_confetti():
            for shape in confetti:
                canvas.move(shape, 0, 5)
                coords = canvas.coords(shape)
                if coords[1] > 400:
                    canvas.move(shape, 0, -500)
            confetti_anim_id[0] = canvas.after(50, animate_confetti)
        
        def stop_confetti():
            if confetti_anim_id[0]:
                canvas.after_cancel(confetti_anim_id[0])
                confetti_anim_id[0] = None
            for shape in confetti:
                canvas.delete(shape)
            confetti.clear()

        create_confetti()
        animate_confetti()
        result_window.after(5000, stop_confetti) # 5秒後停止彩帶掉落
        
        # 冠軍閃爍動畫
        def animate_winner(label):
            def blink(count=0):
                if count < 6:
                    label.config(font=("Arial", 24, "bold"))
                    label.config(font=("Arial", 22 + (2 if count % 2 == 0 else 0), "bold"))
                    label.after(300, lambda: blink(count + 1))
                else:
                    label.config(font=("Arial", 24, "bold"))
            blink()
        
        # 分別遊玩到結束玩家和中途退出玩家
        active_players = [pid for pid in self.finish_order if pid not in self.left_players]
        left_players = [pid for pid in self.finish_order if pid in self.left_players]
        ordered_players = active_players + left_players

        # 展示排名
        for idx, pid in enumerate(ordered_players):
            player_name = self.track_canvas.itemcget(self.players_name_ids[pid], "text")
            is_self = (pid == self.player_id)
            is_left = (pid in self.left_players)
            is_first = (idx == 0 and not is_left)
            
            if is_left:
                display_text = f"{player_name} ❌ Left"
                fg_color = "#999"
                font_style = ("Arial", 14, "italic")
            else:
                display_text = f"🥇 {player_name}" if idx == 0 else f"{idx + 1}. {player_name}"
                fg_color = '#800000' if is_self else "#555"
                font_style = ("Arial", 16, "bold") if is_self else ("Arial", 16)
            
            delay = idx*2000
            def show_label(text=display_text, color=fg_color, font=font_style, winner=is_first):
                label = tk.Label(result_window, text=text, font=font, bg="#f8f9fa", fg=color)
                label.pack(pady=5)
                if(winner):
                    animate_winner(label)
            result_window.after(delay, show_label)
    
        
    def back_to_menu(self):
        try:
            if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
                self.send_json({
                    "type": "leave",
                    "id": self.player_id
                })
                self.destroy()
                if hasattr(self.root, "show_main_menu"):
                    self.root.show_main_menu()
                self.game_over = True
        except:
            pass

    def destroy(self):
        self.is_destroyed = True
        self.frame.destroy()
