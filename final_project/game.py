import os
import tkinter as tk
from tkinter import GROOVE, messagebox
import time
import random
from tkinter.font import BOLD
from typing import List, Dict

class GameWindow:
    def set_resolution(self):            
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if self.aspect_ratio == "4:3":
            width = 480
            height = 360
        else:
            width = 640
            height = 360
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 4) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    # 遊戲時版本的menu
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="4:3", command=lambda: self.set_ratio("4:3"))
        view_menu.add_command(label="16:9", command=lambda: self.set_ratio("16:9"))
        menubar.add_cascade(label= "View", menu=view_menu)
        self.root.config(menu=menubar)

    def set_ratio(self, ratio):
        self.aspect_ratio = ratio
        self.set_resolution()

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.resizable(False, False)
        self.original_menu = self.root["menu"]
        self.create_menu_bar()

        self.articles = self.load_articles()
        if not self.articles:
            return 
        self.target_article = random.choice(self.articles)
        self.target_words = self.target_article.split()
        self.start_time = None
        self.is_typing = None
        
        # 調整視窗開啟位置
        self.aspect_ratio = getattr(root, 'aspect_ratio', '4:3')
        self.set_resolution()
        # stats相關紀錄參數
        self.has_made_mistake = False # 用於避免同個單字輸入錯誤被重複計算
        self.total_wrong_words = 0
        
        # 文本顯示參數
        self.current_word_idx = 0
        self.line = 0
        self.typed_words : List = [] # 儲存使用者已經正確輸入的單字們(已經通過空白鍵進入下一個)
        
        self.create_GUI()

    def create_GUI(self):
        ARTICLE_FG = "#ffffff"
        ARTICLE_BG = "#2c3e50"
        ENTRY_BG = "#ecf0f1"
        BUTTON_COLOR = "#3498db"
        BUTTON_TEXT = "#ffffff"
        FONT = ("Arial", 14)
        TITLE_FONT = ("Arial", 18, "bold")
        
        # Frame排版管理
        self.frame = tk.Frame(self.root) # main Frame
        self.race_car_frame = tk.Frame(self.frame)
        self.text_frame = tk.Frame(self.frame)
        self.bottom_frame = tk.Frame(self.frame)
        
        self.frame.pack(expand=True, fill="both")
        self.race_car_frame.grid(column=0, row=0, sticky="ew")
        self.text_frame.grid(column=0, row=1, sticky="nsew")
        self.bottom_frame.grid(column=0, row=2, sticky="nsew")
        self.frame.configure(bg="#ecf0f1")
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        
        # 建立車車進度條區塊
        self.create_progress_bar()
        
        # 文章顯示區塊
        self.article_display = tk.Text(
            self.text_frame, 
            height=7,
            wrap="word",
            font=FONT, 
            bg=ARTICLE_BG,
            fg=ARTICLE_FG,
            borderwidth=0,
            padx=10,
        )
        self.article_display.pack(pady=10, expand=True, fill="both")
        self.article_display.bind("<Configure>", self.on_article_display_resize)
        # 設定文本文字顏色樣式，用以區分打過的字，目前打到哪...
        self.article_display.tag_config("correct", foreground="lime")
        self.article_display.tag_config("incorrect", foreground="red")
        self.article_display.tag_config("default", foreground=ARTICLE_FG, background=ARTICLE_BG)
        self.article_display.tag_config("current_correct", foreground="lime", underline=1)
        self.article_display.tag_config("current_incorrect", foreground="red", underline=1)
        self.article_display.tag_config("current_pending", foreground=ARTICLE_FG, underline=1)
        self.article_display.tag_config("extra_wrong", foreground="red", background="#ffe6e6", underline=1)
        self.article_display.config(state="disabled")
        
        # typing Area
        self.typing_entry = tk.Entry(
            self.bottom_frame,
            font=FONT,
            bg=ENTRY_BG,
            width=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        self.typing_entry.pack(expand=True, fill='x')
        self.typing_entry.bind("<space>", self.on_space_press)
        self.typing_entry.bind("<KeyRelease>", self.on_key_release)
        
        # 統計資訊
        self.stats_label = tk.Label(
            self.bottom_frame, 
            text="WPM: 0 | Accuracy: 100% | Words: 0 / 0 | Time: 0s",
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        self.stats_label.pack(pady=5)
        
        # 重新遊玩和回到菜單按鈕
        self.restart_button = tk.Button(
            self.bottom_frame,
            text="重新開始",
            font=FONT,
            bg=BUTTON_COLOR,
            fg=BUTTON_TEXT,
            padx=10,
            pady=5,
            command=self.restart_game
        )
        self.restart_button.pack(pady=10)
        
        self.menu_button = tk.Button(
            self.bottom_frame,
            text="回到選單",
            font=FONT,
            bg="#95a5a6",
            fg=BUTTON_TEXT,
            padx=10,
            pady=5,
            command=self.back_to_menu
        )
        self.menu_button.pack(pady=5)
        
        
        self.render_article()
        self.update_stats()
    
    # current_input: 目前單字輸入的位置(目前進行中的單字優)
    def render_article(self, current_iunput=""):
        # 重新渲染文本框前要先將舊資訊清除
        self.article_display.config(state="normal")
        self.article_display.delete("1.0", tk.END)
        for tag in self.article_display.tag_names():
            self.article_display.tag_remove(tag, "1.0", tk.END)

        for i, word in enumerate(self.target_words):
            for j, char in enumerate(word):
                tag = "default"
                # 處理已經完成的單字文本顯示
                if i < len(self.typed_words):
                    if j < len(self.typed_words[i]):
                        if self.typed_words[i][j] == char:
                            tag = "correct"
                        #!FIX 考慮只保留correct，因為已完成單字應該必定為correct
                        else:
                            tag = "incorrect"
                    else:
                        tag = "incorrect"
                # 處理目前進行到的單字文本顯示
                elif i == self.current_word_idx:
                    if j < len(current_iunput):
                        if current_iunput[j] == char:
                            tag = "current_correct"
                        else:
                            tag = "current_incorrect"
                    else:
                        tag = "current_pending"
                self.article_display.insert(tk.END, char, tag)
        
            # 當目前單字多餘輸入時同樣在文本上顯示錯誤
            if i == self.current_word_idx and len(current_iunput) > len(word):
                extra_text = current_iunput[len(word):]
                for c in extra_text:
                    self.article_display.insert(tk.END, c, "extra_wrong")            
            self.article_display.insert(tk.END, " ", "default") # 不要忘了單字間的空格
        self.article_display.config(state="disabled")
        self.article_display.yview_scroll(self.line, "units")
    
    def on_article_display_resize(self, event):
        self.line = 0
        prev_line = 0
        self.auto_scroll_after_first_line_done()
        while (self.line - prev_line) == 1 and self.line < 100:
            prev_line = self.line
            self.auto_scroll_after_first_line_done()
            self.render_article()
        return 
    
    def auto_scroll_after_first_line_done(self):
        text = self.article_display
        target = self.target_words
        typed = self.typed_words
        
        # 若不需要調整
        bbox = self.article_display.bbox("end-1c")
        if bbox:
            x, y, w, h = bbox
            if y+h <= self.article_display.winfo_height():
                return

        # 從index "1.0" 開始逐字找第一行
        line_end_idx = None
        prev_y = None
        for offset in range(len(self.target_article)):
            idx = f"1.0 + {offset} chars"
            bbox = text.bbox(idx)
            if not bbox:
                continue #!FIX
            x, y, w, h = bbox
            if prev_y is None:
                prev_y = y
            elif y != prev_y:
                line_end_idx = f"1.0 + {offset - 1} chars"
                break
        else:
            line_end_idx = f"1.0 + {len(self.target_article) - 1} chars"

        # 取得該位置的字元並向前尋找該字屬於哪個單字
        char_pos = text.index(line_end_idx)
        linear_index = int(char_pos.split('.')[1])  # 因為整段是 1 行
        word_end = 0
        for i, word in enumerate(typed):
            word_end += len(word) + 1
            if linear_index + 1 == word_end:
                self.line += 1
                break

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

    def on_key_release(self, event):
        current_input = self.typing_entry.get()
        
        # 計算輸入錯誤次數
        if self.current_word_idx < len(self.target_words):
            target_word = self.target_words[self.current_word_idx]
            is_wrong = False
            # 判斷目前輸入與目前打到的文本單字是否有錯誤
            for j in range(min(len(current_input), len(target_word))):
                if current_input[j] != target_word[j]:
                    is_wrong = True
                    break
            if len(current_input) > len(target_word):
                is_wrong = True
            if is_wrong and not self.has_made_mistake:
                self.total_wrong_words += 1
                self.has_made_mistake = True
            
        self.render_article(current_iunput=current_input)
        if not self.is_typing:
            self.start_time = time.time()
            self.is_typing = True
            # 暫時關閉menu不能更改尺寸
            emptyMenu = tk.Menu()
            self.root.config(menu=emptyMenu)
    
    def on_space_press(self, event):
        typed_word = self.typing_entry.get().strip()
        if self.current_word_idx < len(self.target_words):
        # 若目前打的單字完全正確可以進入下一個單字
            if typed_word == self.target_words[self.current_word_idx]:
                self.typed_words.append(typed_word)
                self.current_word_idx += 1
                self.typing_entry.delete(0, tk.END)
                self.has_made_mistake = False
                self.render_article()
                self.auto_scroll_after_first_line_done()
                self.update_stats()
                self.update_progress_bar()
            
                # 當全部文章都打完時
                if self.current_word_idx >= len(self.target_words):
                    self.typing_entry.config(state="disabled")
                    self.update_stats(final=True)
                    self.car_blink_at_finish(self.car)
                    self.create_menu_bar()
        return "break"       
    
    # 每當打正確一個單字時計算數據
    def update_stats(self, final=False):
        total_typed = sum(len(w) for w in self.typed_words)
        
        elapsed_time = time.time() - self.start_time if self.is_typing else 0
        wpm = (total_typed * 60) / (5 * elapsed_time) if elapsed_time > 0 else 0
        correct_words = len(self.typed_words)-self.total_wrong_words
        accuracy = (correct_words / len(self.typed_words)) * 100 if self.typed_words else 100

        msg = f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}% | Words: {correct_words} / {len(self.target_words)} | Time: {int(elapsed_time)}s"
        if final:
            msg = f"完成! {msg}"
        self.stats_label.config(text=msg)

    def create_progress_bar(self):
        # 設定 Canvas 作為賽道進度條底圖
        self.track_canvas = tk.Canvas(self.race_car_frame, height=80, bg="#eeeae7", highlightthickness=0, border=1, relief=GROOVE)
        self.track_canvas.grid(row=0, column=0, sticky="ew", pady=0, padx=5)
        self.race_car_frame.columnconfigure(0, weight=1)
        # 調整視窗時，動態更新終點與起點位置
        self.track_canvas.bind("<Configure>", self.resize_progress_bar)
        # 初始化車子與進度百分比文字
        self.car = self.track_canvas.create_text(0, 0, text="🏎️", fill='#800000', font=("Arial",32), anchor="nw")
        self.progress_text = self.track_canvas.create_text(10, 5, text="0%", font=("Arial", 18, BOLD), anchor="nw")

    def resize_progress_bar(self, event):
        self.finish_line_x = self.track_canvas.winfo_width() - 60 # 取得canvas最右端x座標
        # 建立賽道地板
        self.track_canvas.delete("floor")
        self.track_canvas.create_line(
            0, 80,
            self.finish_line_x, 80,
            fill="black",
            width=10,
            dash=(5, 5),
            tags="floor"
        )
        
        # 隨視窗大小重新設定終點位置
        self.track_canvas.delete("finish_line")
        self.track_canvas.create_line( # 先建立終點旗桿
            self.finish_line_x, 0,
            self.finish_line_x, 80,
            fill="black",
            width=3,
            dash=(4, 4),
            tags="finish_line"
        )
        self.track_canvas.create_text(self.finish_line_x - 30, 10, text="🏁", font=("Arial", 20), tags="finish_line") # 建立終點線旗幟
        self.update_progress_bar() # 更新車子位置

    def update_progress_bar(self):
        if not hasattr(self, 'car'):
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
                self.track_canvas.coords(self.car, target_x, 30)
                self.track_canvas.itemconfig(self.progress_text, text=progress_text)
                return
            new_x = car_current_x + dx*step
            self.track_canvas.coords(self.car, new_x, 30)
            self.track_canvas.itemconfig(self.progress_text, text=progress_text)
            self.track_canvas.after(15, lambda: animate(step + 1))
        animate(0)
        
    # 小車抵達終點時閃爍
    def car_blink_at_finish(self, car):
        if not hasattr(self, 'car'):
            return

        blink_count = 3  # 閃爍次數（來回算一次）

        def blink(step):
            if step >= blink_count:
                self.track_canvas.itemconfig(car, state="normal")
                return
            state = "hidden" if step % 2 == 0 else "normal"
            self.track_canvas.itemconfig(car, state=state)
            self.track_canvas.after(200, lambda: blink(step + 1))
        blink(0)
        
    def restart_game(self):
        # 重新開始打字練習，並重置各個參數
        self.start_time = None
        self.is_typing = False
        self.current_word_idx = 0
        self.typed_words = []
        self.has_made_mistake = False
        self.total_wrong_words = 0
        self.line = 0

        self.resize_progress_bar("event")
        
        self.target_article = random.choice(self.articles)
        self.target_words = self.target_article.split()
        self.typing_entry.config(state="normal")
        self.typing_entry.delete(0, tk.END)
        self.stats_label.config(text="")
        self.render_article()
        self.update_stats()
        self.create_menu_bar()
        
    def back_to_menu(self):
        if messagebox.askyesno("回到標題", "是否確定要回到標題呢?"):
            self.destroy()
            self.root.config(menu=self.original_menu)
            if hasattr(self.root, "show_main_menu"):
                self.root.show_main_menu()
    
    def destroy(self):
        self.frame.destroy()
        '''
        self.race_car_frame.destroy()
        self.text_frame.destroy()
        self.bottom_frame.destroy()
        '''