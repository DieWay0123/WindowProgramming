from dataclasses import asdict, dataclass
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List
import os
import json

@dataclass
class Student:
    name: str
    score: int
    deleted: bool = False

class ScoreManager:
    def __init__(self, root):
        self.root = root
        self.root.title("學生成績管理系統")
        self.data_file = "students_data.json"
        
        self.students: Dict[str, List[Student]] = {}
        self.show_deleted = tk.BooleanVar()
        self.scoreList_showMethod_variable = tk.StringVar(self.root, "name_sorted")

        self.load_data()
        self.build_gui()
        self.update_score_listBox()

    def save_data(self):
        data = {name: [asdict(r) for r in records] for name, records in self.students.items()}
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    self.students = {name: [Student(**r) for r in records] for name, records in raw.items()}
            except Exception as e:
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
                        command=self.update_score_listBox).grid(row=3, column=0)
        tk.Radiobutton(self.root, 
                        variable=self.scoreList_showMethod_variable, 
                        val="score_sorted", text="依分數排序", 
                        command=self.update_score_listBox).grid(row=3, column=1)
        tk.Checkbutton(self.root, 
                        variable=self.show_deleted, 
                        text="顯示已刪除紀錄", 
                        command=self.update_score_listBox).grid(row=3, column=2)

        # scoreList
        self.score_lb = tk.Listbox(self.root, width=40, height=10)
        self.score_lb.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        

        # Listbox_scrollBar
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.score_lb.yview)
        self.score_lb.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=4, column=4, sticky="ns")
        
        # score_filter
        tk.Label(self.root, text="分數篩選").grid(row=5, column=0, columnspan=3, sticky="NSEW")
        self.score_filter = tk.Scale(self.root, from_=0, to=100, tickinterval=60, orient=tk.HORIZONTAL, command=self.update_score_listBox)
        self.score_filter.set(0)
        self.score_filter.grid(row=6, column=0, columnspan=5, sticky="NSEW")
    
        # 
        for i in range(0, 7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(0, 3):
            self.root.grid_columnconfigure(i, weight=1)
    # --------------------------------------
    # Function
    # --------------------------------------
    def update_score_listBox(self, val=0):
        self.score_lb.delete(0, tk.END)
        val = self.score_filter.get()
        status = ""
        records = []
        for name, record in self.students.items():
            if self.show_deleted.get():
                status = " (已刪除)"
                for rec in record:
                    if rec.score >= val and rec.deleted == True:
                        records.append(rec)
                        # self.score_lb.insert(tk.END, f"{rec.name} - {rec.score} (已刪除)")
            else:
                latest_record = record[-1]
                if not latest_record.deleted and latest_record.score >= val:
                    records.append(latest_record)
                    # self.score_lb.insert(tk.END, f"{name} - {latest_record.score}")
        for rec in sorted(records, key=self.select_scoreList_showMethod):
            self.score_lb.insert(tk.END, f"{rec.name} - {rec.score}{status}")

    def add_student(self):
        name = self.name_entry.get().strip()
        score_str = self.score_entry.get().strip()
                
        try:
            score = int(score_str)
            if not(0 <= score <= 100):
                raise ValueError
        except ValueError:
            messagebox.showwarning("輸入錯誤", "請輸入有效的整數數字成績(0~100)")
            return
        
        if name in self.students:
            latest_record = self.students[name][-1]
            if not latest_record.deleted:
                messagebox.showwarning("警告", "已有相同名稱的學生")
                return
        else:
            self.students[name] = []
        student_record = Student(name, score, deleted=False)
        self.students[name].append(student_record)
        self.save_data()
        self.update_score_listBox()
        return
    
    def search_student(self):
        name = self.name_entry.get().strip()
        if name in self.students and not self.students[name][-1].deleted:
            messagebox.showinfo("查詢結果", f"{name} - {self.students[name][-1].score}分")
        else:
            messagebox.showerror("錯誤", "查無此人")
        return
    
    def delete_student(self):
        name = self.name_entry.get().strip()
        if name in self.students and not self.students[name][-1].deleted:
            self.students[name][-1].deleted = True
            self.save_data()
            self.update_score_listBox()
            messagebox.showinfo("成功", f"已刪除{name}的分數")
        else:
            messagebox.showerror("錯誤", "查無此人，請確認是否已紀錄或已刪除")
        return
    
    def update_student(self):
        name = self.name_entry.get().strip()
        score_str = self.score_entry.get().strip()
        if name in self.students and not self.students[name][-1].deleted:
            try:
                score = int(score_str)
                if not (0 <= score <= 100):
                    raise ValueError
            except ValueError:
                messagebox.showwarning("輸入錯誤", "請輸入有效的整數數字成績(0~100)")
                return
            self.students[name][-1].score = score
            self.save_data()
            self.update_score_listBox()
            messagebox.showinfo("成功", f"{name}的分數已更新為{score}")
        else:
            messagebox.showerror("錯誤", "查無此人")
        return
    def select_scoreList_showMethod(self, student):
        if self.scoreList_showMethod_variable.get() == "name_sorted":
            return student.name
        return -student.score

if __name__ == '__main__':
    root = tk.Tk()
    app = ScoreManager(root)
    app.root.mainloop()