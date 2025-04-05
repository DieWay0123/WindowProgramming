import tkinter as tk

def button_click(text):
    #print("Test")
    current_text = entry.get()
    new_text = current_text + text
    entry.delete(0, tk.END)
    entry.insert(tk.END, new_text)

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def clear():
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("小算盤")

entry = tk.Entry(root, fg='black')
entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8)

button_texts = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+"
]

for i, text in enumerate(button_texts):
    if(text=='='):
      button = tk.Button(root, text=text, command=calculate)
    else:
      button = tk.Button(root, text=text, command=lambda text=text: button_click(text))
    button.grid(row=(i//4)+1, column=(i%4), sticky='nsew', padx=5, pady=5)

clear_button = tk.Button(root, text="C", command=clear)
clear_button.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

# 動態調整按鈕和列的大小
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

root.mainloop()
