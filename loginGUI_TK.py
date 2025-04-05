import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# 創建主視窗
root = tk.Tk()
root.title("登入畫面")

# 載入圖片
PIL_image = Image.open("123.jpg")
print(PIL_image)
image = ImageTk.PhotoImage(PIL_image)  # 替換成你圖片的路徑

# 建立顯示圖片的標籤
image_label = tk.Label(root, image=image, height=100, width=100)
image_label.grid(row=0, column=0, columnspan=2, pady=10)

# 建立 ID 輸入框和標籤
id_label = tk.Label(root, text="ID")
id_label.grid(row=1, column=0, padx=10, pady=5)
id_entry = tk.Entry(root)
id_entry.grid(row=1, column=1, padx=10, pady=5)

# 建立密碼輸入框和標籤
password_label = tk.Label(root, text="Password")
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)

# 建立登入按鈕
login_button = tk.Button(root, text="Login")
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# 執行主迴圈
root.mainloop()