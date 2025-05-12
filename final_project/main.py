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
        # 調整視窗開啟位置
        self.title("TypeRacer 練習程式")
        self.aspect_ratio = "4:3"
        self.minsize(width=600, height=450)
        self.resizable(True, True)

        self.main_menu_frame = None
        self.game_window = None
        self.create_menu_bar()
        self.show_main_menu()

    def create_menu_bar(self):
        menubar = tk.Menu(self)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="4:3", command=lambda: self.set_ratio("4:3"))
        view_menu.add_command(label="16:9", command=lambda: self.set_ratio("16:9"))
        menubar.add_cascade(label= "View", menu=view_menu)
        self.config(menu=menubar)

    def set_ratio(self, ratio):
        self.aspect_ratio = ratio
        self.set_resolution()

    def set_resolution(self):            
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        if self.aspect_ratio == "4:3":
            width = 960
            height = 720
        else:
            width = 1280
            height = 720
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_main_menu(self):
        self.title("TypeRacer 英打練習")
        self.set_resolution()
        self.resizable(True, True)

        # 先將所有視窗關閉，確保只會有後續創建的Menu畫面
        if self.game_window:
            self.game_window.destroy()
        if self.main_menu_frame:
            self.main_menu_frame.destroy()

        self.main_menu_frame = tk.Frame(self, bg="#1a1a1a")
        self.main_menu_frame.pack(expand=True, fill="both")
        
        self.main_menu_frame.columnconfigure(0, weight=1)
        self.main_menu_frame.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        
        title = tk.Label(
            self.main_menu_frame, 
            text="🕹️Welcome to TypeRacer!", 
            font=("Courier New", 42, "bold"),
            bg="#1a1a1a",
            fg="#ffe600"
        )
        title.grid(row=0, column=0, pady=40, sticky="ns")

        def create_menu_button(text, bg, hover, command, row):
            btn = tk.Button(
                self.main_menu_frame,
                text=text,
                font=("Courier New", 16, "bold"),
                bg=bg,
                fg="white",
                activebackground=hover,
                activeforeground="white",
                width=25,
                height=2,
                bd=4,
                relief="ridge",
                command=command
            )
            btn.grid(row=row, column=0, pady=10, padx=150, sticky="nsew")
            
        create_menu_button("Solo Typing", "#2ecc71", "#58d68d", self.start_solo_race_typing_game, 1)
        create_menu_button("Host Game (2P)", "#3498db", "#5dade2", self.start_host_game, 2)
        create_menu_button("Join Game (2P)", "#8e44ad", "#a569bd", self.start_join_game, 3)
        create_menu_button("TypeBeat Rhythm", "#f39c12", "#f7c65f", self.start_type_beat, 4)
        create_menu_button("Exit", "#e74c3c", "#ec7063", self.quit, 5)   

    def modify_window_size(self, mode):
        if self.aspect_ratio == "4:3":
            if mode == "solo":
                size = (480, 360)
            elif mode == "multi_game":
                size = (960, 720)
            else:
                size = (1400, 400)
            return size
        else:
            if mode == "solo":
                size = (640, 360)
            elif mode == "multi_game":
                size = (1280, 720)
            else:
                size = (1400, 400)

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
