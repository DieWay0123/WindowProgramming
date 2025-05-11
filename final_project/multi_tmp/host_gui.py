from typing import List
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import GROOVE
from tkinter.font import BOLD
import socket
import threading
import json
import random 
import time
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
        self.clients = []
        self.clients_names = []
        self.server_socket: socket.socket = None
        self.conn: socket.socket = None
        self.player_name = None
        self.player_id = None
        self.start_timer = None
        self.game_started = False
        self.remaining_seconds = 10 # 玩家加入倒計時
        
        # 遊戲相關參數
        #TODO load不知道那裡的文本
        self.articles = [
            "The quick brown fox jumps over the lazy dog.",
            "Typing fast requires a lot of practice and precision.",
            "Python is a powerful and beginner-friendly programming language."
        ]
        self.target_article = random.choice(self.articles)
        self.target_words = self.target_article.split()
        
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
        
        
        # 玩家名單frame
        self.player_list_frame = tk.Frame(self.frame, bg="#ffffff", bd=1, relief="sunken")
        self.player_list_frame.pack(padx=20, pady=10, fill="both", expand=False)
        self.player_list_title = tk.Label(self.player_list_frame)
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
    
    def start_hosting(self):
        #!FIX REMOVE
        '''
        self.player_name = self.name_entry.get().strip() or "Host"
        for widget in self.frame.winfo_children():
            widget.destroy()
        '''
        self.player_name = self.name_entry.get().strip() or "Host"
        self.clients_names.append(self.player_name)
        self.update_player_list()
        # 設定 Server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 使用TCP連線
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.host_port))
        self.server_socket.listen(5) # TCP 3way handshake
        self.status.config(text=f"Waiting for players to join ({self.remaining_seconds} seconds)...")
        threading.Thread(target=self.accept_connection, daemon=True).start()
        # threading.Thread(target=self.delayed_game_start, daemon=True).start() # 延後進入遊戲
        self.update_countdown()

    def update_countdown(self):
        if self.remaining_seconds > 0:
            self.status.config(text=f"Waiting for players to join ({self.remaining_seconds} seconds)...")
            self.remaining_seconds -= 1
            self.root.after(1000, self.update_countdown)            
        else:
            if not self.game_started:
                self.launch_game_ui()
                self.game_started = True
    
    def accept_connection(self):
        while not self.game_started:
            try:
                conn, addr = self.server_socket.accept()
                self.conn = conn
                self.clients.append(conn)
                threading.Thread(target=self.listen_to_client, args=(conn,), daemon=True).start()
            except Exception as e:
                print(e)
                break

        '''
        self.conn, self.addr = self.server_socket.accept()
        self.update_status(f"Connected to {self.addr[0]}")
        # 發送題目與host player name
        self.send_json({
            "type": "start",
            "text": self.target_article,
            "host_player_name": self.player_name,
        })
        self.root.after(100, self.launch_game_ui)
        '''

    def listen_to_client(self, conn):
        buffer = ""
        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    try:
                        message: dict = json.loads(line)
                    except:
                        continue
                    
                    if message["type"] == "introduce":
                        print("introduce")
                        name = message.get("name", "Guest")
                        if name not in self.clients_names:
                            self.clients_names.append(name)
                            self.update_player_list()
                        try:
                            data = {
                                "type": "introduce",
                                "id": self.player_id,
                                "name": self.player_name,
                                "player_list": self.clients
                            }
                            self.send_json(data, conn)
                        except:
                            continue
                    self.broadcast_json(message, exclude=conn)
            except socket.timeout:
                continue
            except Exception:
                break

    def broadcast_json(self, message, exclude=None):
        for client in self.clients:
            if client == exclude:
                continue
            try:
                client.sendall(json.dumps(message).encode("utf-8") + b"\n")
            except:
                continue
            
    def update_player_list(self):
        for i in self.player_list_box.get_children():
            self.player_list_box.delete(i)
        for name in self.clients_names:
            self.player_list_box.insert("", "end", values=(name,))

    def launch_game_ui(self):
        # 開始遊戲時要向所有client送出start訊息
        for client in self.clients:
            try:
                data = {
                    "type": "start",
                    "text": self.target_article
                }

                self.send_json(data , client)
            except:
                continue
        
        self.frame.destroy()
        game = MultiplayerGameWindow(self.root, player_name=self.player_name, connection=self.server_socket, is_host=True)
        # game.player_id = self.player_id
        game.target_article = self.target_article
        game.target_words = self.target_words
        game.render_article()
        game.update_stats() 
        game.update_all_cars()
        
        game.send_progress()
    
    def update_status(self, text: str):
        self.status.config(text=text)
    
    def send_json(self, data, conn):
        try:
            msg = json.dumps(data).encode("utf-8")
            conn.sendall(msg + b"\n")
        except Exception:
            pass
        
    def back_to_menu(self):
        if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
            if self.server_socket:
                self.server_socket.close()
                self.conn.close()

            self.destroy()
            if hasattr(self.root, "show_main_menu"):
                self.root.show_main_menu()
    
    def destroy(self):
        self.frame.destroy()