import tkinter as tk
from tkinter import messagebox

def on_key(event):
  key_pressed = event.keysm

closeTime = 10
def callback():
  global closeTime
  while closeTime:
    first_confirm = messagebox.askokcancel(
      f"確定要關閉視窗?您還有{closeTime}次機會",
      f"視窗關閉-關閉次數{closeTime}"
    )
    if first_confirm == True:
      if messagebox.askokcancel(
        "您去定要繼續關閉視窗嗎",
        "再次確認"
      ) == True:
        closeTime -= 1
        if closeTime == 0:
          root.destroy()
    else:
      break

root = tk.Tk()
root.geometry("400x300")

root.protocol("WM_DELETE_WINDOW", callback)

root.mainloop()
