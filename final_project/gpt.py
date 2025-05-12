# 改進版 GameWindow：支援當使用者輸入長度 > 單字長度時，仍顯示多餘錯誤字元
import tkinter as tk
import time
import random

class GameWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, bg="#ffffff")
        self.frame.pack(expand=True, fill="both")

        self.texts = self.load_texts()
        self.target_text = random.choice(self.texts)
        self.target_words = self.target_text.split()
        self.start_time = None
        self.is_typing = False
        self.current_word_index = 0
        self.typed_words = []

        self.create_widgets()

    def load_texts(self):
        return [
            "The quick brown fox jumps over the lazy dog.",
            "Typing fast requires a lot of practice and precision.",
            "Python is a powerful and beginner-friendly programming language."
        ]

    def create_widgets(self):
        self.text_display = tk.Text(self.frame, height=5, width=70, font=("Arial", 14), bg="#ffffff", borderwidth=0)
        self.text_display.pack(pady=10)
        self.text_display.config(state="disabled")

        self.entry = tk.Entry(self.frame, font=("Courier", 14), width=70)
        self.entry.pack(pady=10)
        self.entry.bind("<space>", self.on_space_press)
        self.entry.bind("<KeyRelease>", self.on_key_release)

        self.stats_label = tk.Label(self.frame, text="WPM: 0 | Accuracy: 100% | Words: 0 / 0 | Time: 0s",
                                    font=("Arial", 12), bg="#ffffff", fg="#444")
        self.stats_label.pack(pady=10)

        self.render_text()

    def render_text(self, current_input=""):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        for tag in self.text_display.tag_names():
            self.text_display.tag_delete(tag)

        char_index = 0
        for i, word in enumerate(self.target_words):
            for j, char in enumerate(word):
                tag = "default"
                if i < len(self.typed_words):
                    if j < len(self.typed_words[i]):
                        if self.typed_words[i][j] == char:
                            tag = "correct"
                        else:
                            tag = "incorrect"
                    else:
                        tag = "incorrect"
                elif i == self.current_word_index:
                    if j < len(current_input):
                        if current_input[j] == char:
                            tag = "current_correct"
                        else:
                            tag = "current_incorrect"
                    else:
                        tag = "current_pending"

                self.text_display.insert(tk.END, char, tag)
                char_index += 1

            # 顯示多打的錯誤字元（額外輸入）
            if i == self.current_word_index and len(current_input) > len(word):
                extra = current_input[len(word):]
                for c in extra:
                    self.text_display.insert(tk.END, c, "extra_wrong")
                    char_index += 1

            self.text_display.insert(tk.END, " ", "default")
            char_index += 1

        # 標籤樣式
        self.text_display.tag_config("correct", foreground="green")
        self.text_display.tag_config("incorrect", foreground="red")
        self.text_display.tag_config("default", foreground="gray")
        self.text_display.tag_config("current_correct", foreground="green", underline=1)
        self.text_display.tag_config("current_incorrect", foreground="red", underline=1)
        self.text_display.tag_config("current_pending", foreground="gray", underline=1)
        self.text_display.tag_config("extra_wrong", foreground="red", underline=1, background="#ffe6e6")

        self.text_display.config(state="disabled")

    def on_key_release(self, event):
        current_input = self.entry.get()
        self.render_text(current_input=current_input)

    def on_space_press(self, event):
        typed_word = self.entry.get().strip()
        target_word = self.target_words[self.current_word_index] if self.current_word_index < len(self.target_words) else ""

        if not self.is_typing:
            self.start_time = time.time()
            self.is_typing = True

        # 僅當輸入完全正確才可進入下一單字
        if typed_word == target_word:
            self.typed_words.append(typed_word)
            self.current_word_index += 1
            self.entry.delete(0, tk.END)
            self.render_text()
            self.update_stats()

            if self.current_word_index >= len(self.target_words):
                self.entry.config(state="disabled")
                self.update_stats(final=True)

        return "break"

    def update_stats(self, final=False):
        correct_words = sum(1 for i in range(min(len(self.typed_words), len(self.target_words)))
                            if self.typed_words[i] == self.target_words[i])
        total_typed = sum(len(w) for w in self.typed_words)
        elapsed = time.time() - self.start_time if self.is_typing else 0
        wpm = (total_typed * 60) / (5 * elapsed) if elapsed > 0 else 0
        accuracy = (correct_words / len(self.typed_words)) * 100 if self.typed_words else 100

        msg = f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}% | Words: {correct_words} / {len(self.target_words)} | Time: {int(elapsed)}s"
        if final:
            msg = f"🎉 Done! {msg}"
        self.stats_label.config(text=msg)
