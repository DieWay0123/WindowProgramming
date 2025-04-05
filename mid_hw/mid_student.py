import tkinter as tk
from tkinter import messagebox, ttk
import os
import json


class ScoreManager:
    def __init__(self, root):
        self.root = root
        self.root.title("學生成績管理系統")
        self.data_file = "students_data.json"
        self.students = {}
        self.scoreList_showMethod_variable = tk.StringVar(self.root, "name_sorted")

        self.load_data()
        self.build_gui()
        self.update_score_listBox()

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.students, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.students = json.load(f)
        else:
            self.students = {}

    # --------------------------------------
    # GUI Build
    # --------------------------------------    
    def build_gui(self):
        # name entry
        tk.Label(self.root, text="姓名").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        # score entry
        tk.Label(self.root, text="分數").grid(row=1, column=0)
        self.score_entry = tk.Entry(self.root)
        self.score_entry.grid(row=1, column=1)

        # score CRUD buttons
        tk.Button(self.root, text="新增", command=self.add_student).grid(row=0, column=2)
        tk.Button(self.root, text="查詢", command=self.search_student).grid(row=0, column=3)
        tk.Button(self.root, text="刪除", command=self.delete_student).grid(row=1, column=2)
        tk.Button(self.root, text="更新", command=self.update_student).grid(row=1, column=3)
        
        # scoreList rdButtons
        tk.Radiobutton(self.root, 
                        variable=self.scoreList_showMethod_variable, 
                        val="name_sorted", text="依姓名排序", 
                        command=self.select_scoreList_showMethod).grid(row=3, column=0)
        tk.Radiobutton(self.root, 
                        variable=self.scoreList_showMethod_variable, 
                        val="score_sorted", text="依分數排序", 
                        command=self.select_scoreList_showMethod).grid(row=3, column=1)
        tk.Radiobutton(self.root, 
                        variable=self.scoreList_showMethod_variable, 
                        val="show_deleted", text="顯示已刪除分數", 
                        command=self.select_scoreList_showMethod).grid(row=3, column=2)

        # scoreList
        self.score_lb = tk.Listbox(self.root, width=40, height=10)
        self.score_lb.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        # scrollBar
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.score_lb.yview)
        self.score_lb.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=4, column=4, sticky="ns")

    # --------------------------------------
    # Function
    # --------------------------------------
    def update_score_listBox(self):
        self.score_lb.delete(0, tk.END)
        data = self.students.items()
        for name, score in data:
            self.score_lb.insert(tk.END, f"{name} - {score}")
        return

    def add_student(self):
        name = self.name_entry.get()
        score = self.score_entry.get()
        if not name or not score.isdigit():
            messagebox.showwarning("輸入錯誤", "請輸入姓名與數字成績")
        if name in self.students:
            messagebox.showwarning("警告", "已有相同名稱的學生")
        else:
            self.students[name] = int(score)
            self.save_data()
            self.update_score_listBox()
        return
    
    def search_student(self):
        return
    
    def delete_student(self):
        return
    
    def update_student(self):
        return
    def select_scoreList_showMethod(self):
        return

if __name__ == '__main__':
    root = tk.Tk()
    app = ScoreManager(root)
    app.root.mainloop()