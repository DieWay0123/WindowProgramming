from dataclasses import asdict, dataclass
from email import message
from multiprocessing import Value
import select
import tkinter as tk
from tkinter import HORIZONTAL, messagebox, ttk, filedialog
from typing import Dict, List
import os
import json
import csv
import statistics
import difflib
import re

@dataclass
class Student:
    name: str
    score: int
    deleted: bool = False
    note: str = ""

class ScoreManager:
    def __init__(self, root):
        self.root = root
        self.root.title("學生成績管理系統")
        self.data_file = "students_data.json"
        
        self.students: Dict[str, List[Student]] = {}
        self.show_deleted = tk.BooleanVar()
        self.isDescending = tk.BooleanVar()
        self.scoreList_showMethod_variable = tk.StringVar(self.root, "name_sorted")
        self.dark_mode = False
        self.style = ttk.Style()

        self.load_data(filepath=self.data_file)
        self.build_gui()
        self.update_score_listBox()

    def save_data(self):
        data = {name: [asdict(r) for r in records] for name, records in self.students.items()}
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    self.students = {name: [Student(**r) for r in records] for name, records in raw.items()}
            except Exception as e:
                self.students = {}


    # --------------------------------------
    # GUI Build
    # --------------------------------------    
    def build_gui(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="匯入檔案", command=self.import_csv)
        filemenu.add_command(label="匯出csv", command=self.export_csv)
        
        thememenu = tk.Menu(menubar, tearoff=0)
        thememenu.add_command(label="切換 Dark Mode", command=self.toggle_dark_mode)
        
        menubar.add_cascade(label="檔案", menu=filemenu)
        menubar.add_cascade(label="主題", menu=thememenu)
        self.root.config(menu=menubar)

        # frame layout
        # top - 輸入與操作按鈕
        # middle - 排序選項&分數listbox
        # bottom - 分數篩選
        # stats - 成績資訊(平均, Q1/2/3, 及格人數...)
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=5, expand=True)
        sep = ttk.Separator(self.root, orient=HORIZONTAL)
        sep.pack(padx=10, fill=tk.X)
        
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(fill="both", padx=10, pady=5, anchor="s", expand=True)
        self.middle_frame.columnconfigure(0, weight=1)
        self.middle_frame.columnconfigure(1, weight=1)
        self.middle_frame.columnconfigure(2, weight=1)
        self.middle_frame.columnconfigure(3, weight=1)
        self.middle_frame.rowconfigure(1, weight=1)
        sep = ttk.Separator(self.root, orient=HORIZONTAL)
        sep.pack(padx=10, fill=tk.X)
        
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill="both", expand=True)
        
        self.stats_frame = tk.LabelFrame(self.root, text="統計資料", labelanchor="n", padx=10, pady=10)
        self.stats_frame.pack(side='bottom', fill='both', expand='True')
        
        # name entry
        tk.Label(self.top_frame, text="姓名").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.top_frame)
        self.name_entry.grid(row=0, column=1, columnspan=2)

        # score entry
        tk.Label(self.top_frame, text="分數").grid(row=1, column=0)
        self.score_entry = tk.Entry(self.top_frame)
        self.score_entry.grid(row=1, column=1, columnspan=2)
        
        # 備註欄
        tk.Label(self.top_frame, text="備註").grid(row=2, column=0)
        self.note_entry = tk.Text(self.top_frame, height=3, width=30)
        self.note_entry.grid(row=2, column=1, columnspan=2)
        tk.Button(self.top_frame, text="刪除該名學生備註資料", command=self.clear_student_note).grid(row=2, column=3, padx=10)
        
        # score CRUD buttons
        tk.Button(self.top_frame, text="新增", command=self.add_student).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(self.top_frame, text="查詢", command=self.search_student).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(self.top_frame, text="刪除", command=self.delete_student).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(self.top_frame, text="更新", command=self.update_student).grid(row=1, column=4, padx=5, pady=5)
        tk.Button(self.top_frame, text="移除已刪除紀錄", command=self.clear_deleted_records).grid(row=0, column=5, padx=5, pady=5)
        tk.Button(self.top_frame, text="刪除所有資料", command=self.clear_all_records).grid(row=1, column=5, padx=5, pady=5)        
        # scoreList rdButtons
        tk.Radiobutton(self.middle_frame, 
                        variable=self.scoreList_showMethod_variable, 
                        val="name_sorted", text="依姓名排序", 
                        command=self.update_score_listBox).grid(row=0, column=0, sticky='w')
        tk.Radiobutton(self.middle_frame, 
                        variable=self.scoreList_showMethod_variable, 
                        val="score_sorted", text="依分數排序", 
                        command=self.update_score_listBox).grid(row=0, column=1, sticky='w')
        tk.Checkbutton(self.middle_frame,
                        variable=self.isDescending,
                        text="降序排列",
                        command=self.update_score_listBox).grid(row=0, column=2, sticky='w')
        tk.Checkbutton(self.middle_frame, 
                        variable=self.show_deleted, 
                        text="顯示已刪除紀錄", 
                        command=self.update_score_listBox).grid(row=0, column=3, sticky='w')

        # scoreList
        self.score_lb = tk.Listbox(self.middle_frame)
        self.score_lb.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        self.score_lb.bind("<Double-1>", self.score_lb_double_click)

        # Listbox_scrollBar
        self.dark_mode_style = ttk.Style()
        self.x_scrollbar = ttk.Scrollbar(self.middle_frame, orient='horizontal', command=self.score_lb.xview)
        self.y_scrollbar = ttk.Scrollbar(self.middle_frame, orient='vertical', command=self.score_lb.yview)
        self.score_lb.configure(xscrollcommand=self.x_scrollbar.set)
        self.score_lb.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.grid(row=1, column=4, sticky="ns")
        self.x_scrollbar.grid(row=2, column=0, columnspan=4, sticky="ews")
        
        # score_filter
        self.score_filter_label = tk.Label(self.bottom_frame, text="分數篩選").pack(fill='both')
        self.score_filter = tk.Scale(self.bottom_frame, from_=0, to=100, tickinterval=60, orient=tk.HORIZONTAL, command=self.update_score_listBox)
        self.score_filter.set(0)
        self.score_filter.pack(fill='both')
        
        # stats data
        self.stats_label = tk.Label(self.stats_frame, text="分數統計資料")
        self.stats_label.pack()

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
                if latest_record.deleted == False and latest_record.score >= val:
                    records.append(latest_record)
                    # self.score_lb.insert(tk.END, f"{name} - {latest_record.score}")
        for rec in sorted(records, key=self.select_scoreList_showMethod, reverse=self.isDescending.get()):
            note = f"(備註: {rec.note})" if rec.note else ""
            self.score_lb.insert(tk.END, f"{rec.name} - {rec.score}{status}{note}")
        
        if records and len(records) >=2:
            scores = [rec.score for rec in records]
            stats = f"人數: {len(scores)}\t \
            及格人數: {sum(1 for s in scores if s >= 60)}\t \
            平均: {statistics.mean(scores):.2f}\n \
            Q3(25%): {statistics.quantiles(scores, n=4)[2]:.2f}\t \
            Q2(50%): {statistics.median(scores):.2f}\t \
            Q1(75%): {statistics.quantiles(scores, n=4)[0]:.2f}"
        else:
            stats = "目前無可統計資料(僅一筆資料/無資料)"
        self.stats_label.config(text=stats)

    def add_student(self):
        name = self.name_entry.get().strip()
        score_str = self.score_entry.get().strip()
        note = self.note_entry.get("1.0", tk.END).rstrip()
                
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
        student_record = Student(name, score, deleted=False, note=note)
        self.students[name].append(student_record)
        self.name_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
        self.note_entry.delete("1.0", tk.END)
        messagebox.showinfo("成功", f"已成功新增{name}同學的成績!")
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
            self.name_entry.delete(0, tk.END)
            self.score_entry.delete(0, tk.END)
        else:
            messagebox.showerror("錯誤", "查無此人，請確認是否已紀錄或已刪除")
        return
    
    def update_student(self):
        name = self.name_entry.get().strip()
        score_str = self.score_entry.get().strip()
        note = self.note_entry.get("1.0", tk.END).rstrip()
        if name in self.students and not self.students[name][-1].deleted:
            try:
                if (len(score_str) == 0 and not note):
                    raise ValueError
                if len(score_str) != 0 and not score_str.isdigit():
                    raise ValueError
                if len(score_str) != 0 and not (0 <= int(score_str) <= 100):
                    raise ValueError
            except ValueError:
                messagebox.showwarning("輸入錯誤", "請輸入有效的整數數字成績(0~100)或備註內容")
                return
            
            if score_str.isdigit():
                score = int(score_str)
                self.students[name][-1].score = score
                messagebox.showinfo("成功", f"{name}的分數已更新為{score}")
            if note:
                self.students[name][-1].note = note
                messagebox.showinfo("成功", f"{name}的備註內容已更新")
            self.save_data()
            self.update_score_listBox()
            self.name_entry.delete(0, tk.END)
            self.score_entry.delete(0, tk.END)
            self.note_entry.delete("1.0", tk.END)
        else:
            messagebox.showerror("錯誤", "查無此人")
        return
    def select_scoreList_showMethod(self, student):
        if self.scoreList_showMethod_variable.get() == "name_sorted":
            return student.name
        return student.score
    
    def import_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("支援格式", "*.csv *.json")])
        if not filepath:
            return
        try:
            if filepath.endswith(".csv"):
                import_students = {}
                with open(filepath, mode='r', encoding="utf-8-sig") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        name = row['姓名'].strip()
                        score = int(row["成績"].strip())
                        deleted = row["已刪除"].strip().lower() in ["true", "1", "yes"]
                        note = row.get("備註", "")
                        if name not in import_students:
                            import_students[name] = []
                        import_students[name].append(Student(name, score, deleted, note))
                self.students = import_students            
            elif filepath.endswith(".json"):
                self.load_data(filepath)
            else:
                raise ValueError("不支援的檔案格式")
            self.save_data()
            self.update_score_listBox()
            messagebox.showinfo("匯入成功", f"已成功匯入 {filepath}")
        except Exception as e:
            messagebox.showerror("匯入失敗", f"發生錯誤：{e}")
            
    def export_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        with open(filepath, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["姓名", "成績", "已刪除", "備註"])
            for name, records in self.students.items():
                for r in records:
                    writer.writerow([r.name, r.score, r.deleted, r.note])
            file.close()
        messagebox.showinfo("匯出成功", f"已匯出到 {filepath}")
        
    def clear_deleted_records(self):
        ask_msg = messagebox.askyesno("確認刪除", "是否確認要刪除已刪除歷史資料?")
        if ask_msg:
            for name in list(self.students.keys()):
                self.students[name] = [rec for rec in self.students[name] if not rec.deleted]
                if not self.students[name]:
                    del self.students[name]
            self.save_data()
            self.update_score_listBox()
            messagebox.showinfo("刪除成功", "已刪除所有刪除歷史資料!")
        
    def clear_all_records(self):
        ask_msg = messagebox.askyesno("確認刪除", "是否確認要刪除所有學生資料?")
        if ask_msg:
            self.students = {}
            self.save_data()
            self.update_score_listBox()
            messagebox.showinfo("刪除成功", "已刪除所有學生資料!")
    
    def toggle_dark_mode(self):
        bg = "#F2F2F2" if self.dark_mode else "#2e2e2e"
        fg = "#000000" if self.dark_mode else "#FFFFFF"
        bottom_frame_bg =  "#F2F2F2" if self.dark_mode else "#404040"

        widgets = [
            self.root, self.top_frame, self.middle_frame, self.bottom_frame,
            self.name_entry, self.score_entry, self.score_lb
        ]
        
        for w in widgets:
            w.configure(bg=bg)
        for child in self.top_frame.winfo_children() + self.middle_frame.winfo_children():
            try:
                if type(child) == tk.Radiobutton or type(child) == tk.Checkbutton:
                    child.configure(bg=bg, fg=fg, selectcolor=bg)
                else:
                    child.configure(bg=bg, fg=fg)
                
            except:
                pass
            
        for child in self.bottom_frame.winfo_children() + self.stats_frame.winfo_children() + [self.bottom_frame, self.stats_frame]:
            try:
                child.configure(bg=bottom_frame_bg, fg=fg)
            except:
                pass

        self.score_lb.configure(bg=bg, fg=fg)
        self.dark_mode = not self.dark_mode
    
    def score_lb_double_click(self, event):
        selection = self.score_lb.curselection()
        if selection:
            select_content = self.score_lb.get(selection)
            match = re.match(r"(.+?)\s*-\s*(\d+)(?:\(備註:\s*(.+?)\))?", select_content)
            
            self.name_entry.delete(0, tk.END)
            self.score_entry.delete(0, tk.END)
            self.note_entry.delete("0.0", tk.END)
            
            self.name_entry.insert(0, match.group(1))
            self.score_entry.insert(0, match.group(2))
            self.note_entry.insert("0.0", match.group(3) if match.group(3) else "")

    def clear_student_note(self):
        name = self.name_entry.get().strip()
        if name in self.students and not self.students[name][-1].deleted and len(self.students[name][-1].note) != 0:
            self.students[name][-1].note = ""
            self.save_data()
            self.update_score_listBox()
        else:
            messagebox.showerror("錯誤", "查無有效學生可清除備註")
            return
        messagebox.showinfo("成功", f"已移除{name}學生的備註資料!")

    
if __name__ == '__main__':
    root = tk.Tk()
    app = ScoreManager(root)
    app.root.mainloop()