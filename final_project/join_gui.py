# 建立 P2P 連線端 GUI：JoinGameWindow，輸入 IP 並與主機玩家連線對戰
import tkinter as tk
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
        self.frame = tk.Frame(self.root, bg="#1a1a1a")
        self.frame.pack(expand=True, fill="both")

        # 連線相關參數
        self.conn = None
        self.player_name = "Player"
        self.player_id = None
        self.host_name = "Host"
        self.target_article = ""

        self.build_connection_ui()

    def build_connection_ui(self):
        tk.Label(self.frame, text="Enter Host IP:", font=("Courier New", 24, "bold"), bg="#1a1a1a", fg="#ffe600").pack(pady=20)
        self.ip_entry = tk.Entry(self.frame, font=("Courier New", 14), bg="#ecf0f1", fg="#2c3e50", insertbackground="black", width=25, justify="center")
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.pack(pady=5)

        tk.Label(self.frame, text="Enter Your Name:", font=("Courier New", 24, "bold"), bg="#1a1a1a", fg="white").pack(pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Courier New", 14), bg="#ecf0f1", fg="#2c3e50", insertbackground="black", width=25, justify="center")
        self.name_entry.insert(0, "Guest")
        self.name_entry.pack(pady=5)

        self.connect_button = tk.Button(
            self.frame, 
            text="Connect to Host", 
            font=("Courier New", 16, "bold"), 
            bg="#27ae60", fg="white",
            activebackground="#2ecc71",
            relief="ridge", bd=4, padx=10, pady=5,
            command=self.connect_to_host
        )
        self.connect_button.pack(pady=20)

        self.status_label = tk.Label(self.frame, text="Awaiting connection...", font=("Courier New", 12), bg="#2c3e50", fg="gray", relief="groove", bd=3, padx=10, pady=5, width=30)
        self.status_label.pack(pady=5)

        tk.Button(
            self.frame,
            text="回到選單",
            font=("Arial", 14),
            bg="#95a5a6",
            fg="#ffffff",
            padx=10,
            pady=5,
            command=self.back_to_menu
        ).pack(pady=10)

    def connect_to_host(self):
        ip = self.ip_entry.get().strip()
        self.connect_button.config(state="disabled")
        self.player_name = self.name_entry.get().strip() or "Guest"
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((ip, 5000))
            self.player_id = f"{self.player_name}#{self.conn.getsockname()[1]}"
            self.status_label.config(text="Connected! Waiting for game start...")
            
            self.root.after(500, self.launch_game_ui)
            # threading.Thread(target=self.listen_for_messages, daemon=True).start()
        except Exception as e:
            self.connect_button.config(state="normal")
            self.status_label.config(text=f"Connection failed: {e}")
    '''
    def listen_for_messages(self):
        buffer = ""
        while True:
            try:
                data = self.conn.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    message = json.loads(line)
                    self.handle_message(message)
            except (ConnectionResetError, json.JSONDecodeError):
                break
    '''
    '''
    def handle_message(self, msg):
        if msg["type"] == "start":
            self.text = msg["text"]
            self.host_name = msg.get("host_player_name", "Host")
            self.send_json({"type": "introduce", "name": self.player_name, "id": self.player_id})
            self.root.after(100, self.launch_game_ui)
    '''

    def launch_game_ui(self):
        self.frame.destroy()
        game = MultiplayerGameWindow(self.root, player_name=self.player_name, connection=self.conn, is_host=False)
        game.player_id = self.player_id
        game.render_article()
        game.update_stats()
        game.update_all_cars()

    '''可移除'''
    def send_json(self, data):
        try:
            msg = json.dumps(data).encode("utf-8")
            self.conn.sendall(msg + b"\n")
        except Exception:
            pass
        
    def back_to_menu(self):
        if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
            self.destroy()
            if hasattr(self.root, "show_main_menu"):
                self.root.show_main_menu()
        
    def destroy(self):
        self.frame.destroy()
        
