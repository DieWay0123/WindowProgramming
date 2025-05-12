# main.py
from mimetypes import MimeTypes
import tkinter as tk
from game import GameWindow
from host_gui import HostGameWindow
from join_gui import JoinGameWindow
from type_beat_trainer import TypeBeatTrainerWindow


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TypeRacer 練習程式")
        self.geometry("700x500")
        self.configure(bg="#f0f4f8")  # 背景顏色
        
        self.main_menu_frame = None
        self.game_window = None
        self.show_main_menu()

    def show_main_menu(self):
        self.title("TypeRacer 練習程式")
        # 先將所有視窗關閉，確保只會有後續創建的Menu畫面
        if self.game_window:
            self.game_window.destroy()
        if self.main_menu_frame:
            self.main_menu_frame.destroy()

        self.geometry("700x500")
        self.main_menu_frame = tk.Frame(self, bg="#f0f4f8")
        self.main_menu_frame.pack(expand=True, fill="both")
        
        self.main_menu_frame.columnconfigure(0, weight=1)
        self.main_menu_frame.rowconfigure([0, 1, 2, 3], weight=1)

        title = tk.Label(
            self.main_menu_frame, 
            text="Welcome to TypeRacer!", 
            font=("Helvetica", 32, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        title.grid(row=0, column=0, pady=40, sticky="ns")

        solo_race_typing_start_button = tk.Button(
            self.main_menu_frame, 
            text="Start Solo Typing", 
            font=("Arial", 16), 
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            width=25,
            height=2,
            command=self.start_solo_race_typing_game
        )
        solo_race_typing_start_button.grid(row=1, column=0, pady=5, sticky="ns")

        # 開主機對戰模式按鈕
        host_game_button = tk.Button(
            self.main_menu_frame,
            text="Host Game (2P)",
            font=("Arial", 16),
            bg="#2980b9",
            fg="white",
            activebackground="#3498db",
            activeforeground="white",
            width=25,
            height=2,
            command=self.start_host_game
        ).grid(row=2, column=0, pady=5, sticky="ns")

        # 加入對戰模式按鈕
        join_game_button = tk.Button(
            self.main_menu_frame,
            text="Join Game (2P)",
            font=("Arial", 16),
            bg="#8e44ad",
            fg="white",
            activebackground="#9b59b6",
            activeforeground="white",
            width=25,
            height=2,
            command=self.start_join_game
        ).grid(row=3, column=0, pady=5, sticky="ns")

        typebeat_button = tk.Button(
            self.main_menu_frame,
            text="TypeBeat Rhythm",
            font=("Arial", 16),
            bg="#f39c12",
            fg="white",
            activebackground="#f1c40f",
            activeforeground="white",
            width=25,
            height=2,
            command=self.start_type_beat
        )
        typebeat_button.grid(row=4, column=0, pady=5, sticky="ns")

        exit_button = tk.Button(
            self.main_menu_frame, 
            text="Exit", 
            font=("Arial", 16), 
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            width=25,
            height=2,
            command=self.quit
        )
        exit_button.grid(row=5, column=0, pady=5, sticky="ns")
        

    def start_solo_race_typing_game(self):
        self.main_menu_frame.destroy()
        self.game_window = GameWindow(self)
        
    def start_host_game(self):
        self.main_menu_frame.destroy()
        self.game_window = HostGameWindow(self)

    def start_join_game(self):
        self.main_menu_frame.destroy()
        self.game_window = JoinGameWindow(self)
    
    def start_type_beat(self):
        self.main_menu_frame.destroy()
        self.game_window = TypeBeatTrainerWindow(self)

def main():
    app = MainMenu()
    app.mainloop()

if __name__ == "__main__":
    main()
