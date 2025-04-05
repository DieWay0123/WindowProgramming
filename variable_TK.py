import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("算完壓力好大捏")

def calculate(*args):
  if rate_entry.get() == "" or year_entry.get() == "" or loan_entry.get() == "":
    month_result_var.set(0)
    total_result_var.set(0)
    return
  try:
    rate = float(rate_entry.get())
    years = float(year_entry.get())
    loan = float(loan_entry.get())
    if rate == 0.0:
      month_result_var.set(loan/(years*12))
    else:
      rate = rate/1000
      month_result_var.set((loan * rate) / (1 - (1/((1 + rate) ** (years * 12)))))
    total_result_var.set(month_result_var.get()*12*years)
  except ValueError:
    messagebox.showerror("輸入錯誤", "請輸入有效的數字！")

# 建立輸入框與標籤
tk.Label(root, text="Rate (%)").grid(row=0, column=0, padx=10, pady=5)
rate_entry_var = tk.StringVar()
rate_entry_var.trace_add('write', calculate)
rate_entry = tk.Entry(root, textvariable= rate_entry_var)
rate_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Year").grid(row=1, column=0, padx=10, pady=5)
year_entry_var = tk.StringVar()
year_entry_var.trace_add('write', calculate)
year_entry = tk.Entry(root, textvariable=year_entry_var)
year_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Loan Money").grid(row=2, column=0, padx=10, pady=5)
loan_entry_var = tk.StringVar()
loan_entry_var.trace_add('write', calculate)
loan_entry = tk.Entry(root, textvariable=loan_entry_var)
loan_entry.grid(row=2, column=1, padx=10, pady=5)

# 顯示結果的標籤
tk.Label(root, text="Month").grid(row=3, column=0, padx=10, pady=5)
month_result_var = tk.DoubleVar()
month_result_label = tk.Label(root, textvariable=month_result_var)
month_result_label.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Repayment").grid(row=4, column=0, padx=10, pady=5)
total_result_var = tk.DoubleVar()
total_result_label = tk.Label(root, textvariable=total_result_var)
total_result_label.grid(row=4, column=1, padx=10, pady=5)

root.mainloop()
'''
# 計算按鈕
calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=5, column=0, columnspan=2, pady=10
'''