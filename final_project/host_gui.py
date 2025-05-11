from typing import List
import tkinter as tk
from tkinter import messagebox
from tkinter import GROOVE
from tkinter.font import BOLD
import socket
import threading
import json
import random
import os
from multiplayer_game import MultiplayerGameWindow

class HostGameWindow:
    def __init__(self, root: tk.Tk, host_port=5000):
        self.root = root
        self.root.title("TypeRacer - Host")
        
        # main Frame
        self.frame = tk.Frame(self.root, bg="#ecf0f1")
        self.frame.pack(expand=True, fill="both")
                
        # 連線相關參數
        self.host_port = host_port
        self.conn = None
        self.addr = None
        self.player_name = None
        self.player_id = None
        self.opponent_name = None
        
        # 遊戲相關參數
        self.articles = self.load_articles()

        self.target_article = random.choice(self.articles)
        self.target_words = self.target_article.split()
        self.local_progress = 0
        self.remote_progress = 0
        
        # 文本顯示參數
        self.current_word_idx = 0
        self.line = 0
        self.typed_words : List = []
        
        # 輸入使用者名稱和建立等待連線畫面
        self.build_init_game_ui()
    
    def build_init_game_ui(self):
        tk.Label(self.frame, text="Enter your Name!", font=("Arial", 20), bg="#ecf0f1").pack(pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.name_entry.pack(pady=10)
        tk.Button(self.frame, text="Start Hosting", font=("Arial", 14), bg="#27ae60", fg="white",
                command=self.start_hosting).pack(pady=20)
        self.status = tk.Label(self.frame, text="", font=("Arial", 12), bg="#ecf0f1", fg="gray")
        self.status.pack()
        
        tk.Button(
            self.frame,
            text="回到選單",
            font=("Arial", 14),
            bg="#95a5a6",
            fg="#ffffff",
            padx=10,
            pady=5,
            command=self.back_to_menu
        ).pack()
        
    def load_articles(self):
        articles = []
        FOLDER_PATH = "./articles"
        for filename in os.listdir(FOLDER_PATH):
            if filename.endswith(".txt"):
                with open(os.path.join(FOLDER_PATH, filename), "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        articles.append(content)
                        
        if not articles:
            messagebox.showerror("錯誤", "未讀取到任何文章，請檢察文章資料夾")
            self.root.game_window = None
            self.root.show_main_menu()
        return articles
    
    def start_hosting(self):
        self.player_name = self.name_entry.get().strip() or "Host"
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.status = tk.Label(self.frame, text="Waiting for opponent to join...", font=("Arial", 14), bg="#ecf0f1")
        self.status.pack(pady=20)
        
        # 設定 Server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 使用TCP連線
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.host_port))
        self.server_socket.listen(1) # TCP 3way handshake
        threading.Thread(target=self.accept_connection, daemon=True).start()
    
    def accept_connection(self):
        self.conn, self.addr = self.server_socket.accept()
        self.update_status(f"Connected to {self.addr[0]}")
        # 發送題目與host player name
        self.send_json({
            "type": "start",
            "text": self.target_article,
            "host_player_name": self.player_name,
        })
        self.root.after(100, self.launch_game_ui)

    def launch_game_ui(self):
        self.frame.destroy()
        game = MultiplayerGameWindow(self.root, player_name=self.player_name, connection=self.conn, is_host=True)
        # game.player_id = self.player_id
        game.target_article = self.target_article
        game.target_words = self.target_words # !FIX
        game.render_article()
        game.update_stats() 
        game.update_all_cars()
        
        game.send_progress()
    
    def update_status(self, text: str):
        self.status.config(text=text)
    
    def send_json(self, data):
        try:
            msg = json.dumps(data).encode("utf-8")
            self.conn.sendall(msg + b"\n")
        except Exception:
            pass
            
    def update_local_car(self):
        if len(self.target_article) == 0:
            return
        total_words = len(self.target_words)
        completed_words = len(self.typed_words)
        progress = completed_words / total_words if total_words > 0 else 0

        # 根據進度移動車子（總長度為 finish_line_x）
        target_x = int(progress * self.finish_line_x)
        progress_text = f"{int(progress * 100)}%"
        
        # 取得目前car位置並設定小車動畫參數
        car_current_coords = self.track_canvas.coords(self.car)
        car_current_x = car_current_coords[0] if car_current_coords else 0
        steps = 10
        dx = (target_x - car_current_x) /steps
        
        def animate(step):
            if step >= steps:
                self.track_canvas.coords(self.car, target_x, 40)
                self.track_canvas.itemconfig(self.progress_text, text=progress_text)
                return
            new_x = car_current_x + dx*step
            self.track_canvas.coords(self.car, new_x, 40)
            self.track_canvas.itemconfig(self.progress_text, text=progress_text)
            self.track_canvas.after(15, lambda: animate(step + 1))
        animate(0)
        
    def back_to_menu(self):
        if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
            self.destroy()
            if hasattr(self.root, "show_main_menu"):
                self.root.show_main_menu()
    
    def destroy(self):
        self.frame.destroy()