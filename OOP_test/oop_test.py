import tkinter as tk
from tkinter import *
from oop_base import Tk_Container

class Calculator(Tk_Container):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("小算盤")

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        self.create_widgets()
        self.entry = tk.Entry(self.window, fg='black', bg='gray') #init
        self.entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8)

    def click_calculate_button(self):
        try:
            result = eval(self.enrty.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
    def input_calculator(self, text):
        new_text = self.entry.get() + text
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, new_text)

    def create_widgets(self):
        
        for idx, text in enumerate(self.buttons):
            if(text == '='):
                button = tk.Button(self.window, text=text, command=self.click_calculate_button)
            else:
                button = tk.Button(self.window, text=text, command=lambda text=text: self.input_calculator(text))
            button.grid(column=(idx%4), row=(idx//4)+1, padx=10, pady=10)

if __name__ == '__main__':
    calculator = Calculator()
    calculator.start()