import tkinter as tk
from tkinter import ttk

# 創建主窗口
root = tk.Tk()
root.title("進度條控制")

# 創建進度條
progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=10)

# 啟動進度條的函數
def start_progress():
    progress_bar.start()

# 停止進度條的函數
def stop_progress():
    progress_bar.stop()

# 改變進度條顏色的函數
def change_color(color):
    progress_bar["style"] = color + ".TProgressbar"

# 創建樣式以支持顏色
style = ttk.Style()
style.configure("Red.TProgressbar", troughcolor="white", background="red")
style.configure("Green.TProgressbar", troughcolor="white", background="green")
style.configure("Blue.TProgressbar", troughcolor="white", background="blue")
style.layout("Red.TProgressbar", 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'})])
style.layout("Green.TProgressbar", style.layout("Red.TProgressbar"))
style.layout("Blue.TProgressbar", style.layout("Red.TProgressbar"))
print(style.theme_use())

# 改變進度條模式的函數
def change_mode(mode):
    progress_bar.config(mode=mode)

# 創建選單
menu_bar = tk.Menu(root)

# 功能選單
function_menu = tk.Menu(menu_bar, tearoff=0)
function_menu.add_command(label="啟動進度", command=start_progress)
function_menu.add_command(label="停止進度", command=stop_progress)
function_menu.add_command(label="退出", command=root.quit)
menu_bar.add_cascade(label="功能", menu=function_menu)

# 外觀選單
appearance_menu = tk.Menu(menu_bar, tearoff=0)
appearance_menu.add_command(label="紅色", command=lambda: change_color("Red"))
appearance_menu.add_command(label="綠色", command=lambda: change_color("Green"))
appearance_menu.add_command(label="藍色", command=lambda: change_color("Blue"))
menu_bar.add_cascade(label="外觀", menu=appearance_menu)

# 模式選單
mode_menu = tk.Menu(menu_bar, tearoff=0)
mode_menu.add_command(label="普通模式", command=lambda: change_mode("determinate"))
mode_menu.add_command(label="不確定模式", command=lambda: change_mode("indeterminate"))
menu_bar.add_cascade(label="模式", menu=mode_menu)

root.config(menu=menu_bar)

# 運行主循環
root.mainloop()
