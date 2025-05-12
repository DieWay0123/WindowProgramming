# 建立 P2P 連線端 GUI：JoinGameWindow，輸入 IP 並與主機玩家連線對戰
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import threading
import json

from multiplayer_game import MultiplayerGameWindow

class JoinGameWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TypeRacer - Join")
        # main Frame
        self.frame = tk.Frame(self.root, bg="#ecf0f1")
        self.frame.pack(expand=True, fill="both")

        # 連線相關參數
        self.conn = None
        self.player_name = "Guest"
        self.player_id = None
        self.players_joined = []
        
        self.build_connection_ui()

    def build_connection_ui(self):
        tk.Label(self.frame, text="Enter Host IP:", font=("Arial", 14), bg="#ecf0f1").pack(pady=10)
        self.ip_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(pady=5)

        tk.Label(self.frame, text="Enter Your Name:", font=("Arial", 14), bg="#ecf0f1").pack(pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.name_entry.insert(0, "Guest")
        self.name_entry.pack(pady=5)

        tk.Button(
            self.frame, 
            text="Connect", 
            font=("Arial", 14), 
            bg="#3498db", fg="white",
            command=self.connect_to_host
        ).pack(pady=20)

        self.status_label = tk.Label(self.frame, text="", font=("Arial", 12), bg="#ecf0f1", fg="gray")
        self.status_label.pack()
        
        self.player_list_frame = tk.Frame(self.frame, bg="#ffffff", bd=1, relief="sunken")
        self.player_list_frame.pack(pady=10, padx=20, fill="both", expand=False)
        self.player_list_title = tk.Label(self.player_list_frame, text="Players Joined:", font=("Arial", 12, "bold"), bg="#ffffff", fg="#333")
        self.player_list_title.pack(anchor="w", padx=10, pady=(5, 0))
        self.player_list_box = ttk.Treeview(self.player_list_frame, columns=("name",), show="headings", height=5)
        self.player_list_box.heading("name", text="Player Name")
        self.player_list_box.column("name", anchor="w")
        self.player_list_box.pack(padx=10, pady=5, fill="both")

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

    def connect_to_host(self):
        ip = self.ip_entry.get().strip()
        self.player_name = self.name_entry.get().strip() or "Guest"
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((ip, 5000))
            self.player_id = f"{self.player_name}#{self.conn.getsockname()[1]}"
            self.status_label.config(text="Connected! Waiting for game start...")
            
            self.send_json({
                "type": "introduce",
                "id": self.player_id,
                "name": self.player_name,
            })
            
            threading.Thread(target=self.listen_to_server, daemon=True).start()
        except Exception as e:
            self.status_label.config(text=f"Connection failed: {e}")
            
    def send_json(self, data):
        try:
            msg = json.dumps(data).encode("utf-8")
            self.conn.sendall(msg + b"\n")
        except Exception:
            pass
        
    def listen_to_server(self):
        buffer = ""
        while True:
            try:
                data = self.conn.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    message: dict = json.loads(line)
                    if message.get("type") == "start":
                        print("start")
                        text = message.get("text")
                        self.launch_game_ui(target_article=text)
                    elif message["type"] == "introduce":
                        print("introduce")
                        new_name = message.get("name")
                        self.players_joined = message.get("player_list")
                        if new_name not in self.players_joined:
                            self.players_joined.append(new_name)
                            self.update_player_list()
            except:
                break
            
    def update_player_list(self):
        # 更新玩家名單顯示
        for i in self.player_list_box.get_children():
            self.player_list_box.delete(i)
        for name in self.players_joined:
            self.player_list_box.insert("", "end", values=(name,))

    def launch_game_ui(self, target_article: str):
        self.frame.destroy()
        game = MultiplayerGameWindow(self.root, player_name=self.player_name, connection=self.conn, is_host=False)
        game.player_id = self.player_id
        game.target_article = target_article
        game.target_words = target_article.split()
        game.render_article()
        game.update_stats()
        game.update_all_cars()
        # game.send_progress()
        
    def back_to_menu(self):
        if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
            if self.conn:
                self.conn.close()
            self.destroy()
            if hasattr(self.root, "show_main_menu"):
                self.root.show_main_menu()
        
    def destroy(self):
        self.frame.destroy()
        
