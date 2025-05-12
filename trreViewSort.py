import tkinter as tk
from tkinter import ttk

class SortableTreeviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview sort!")

        self.tree = ttk.Treeview(root, columns=("State"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in ["State"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
            self.tree.column(col, width=100)

        self.data = [
            "B",
            "C",
            "A",
            "E",
            "Z",
            "H",
            "P",
            "K",
            "L",
            "O",
            "Y"
        ]
        for row in self.data:
            self.tree.insert("", tk.END, values=row)
        self.sort_directions = {col: False for col in ("State")}
    def sort_by_column(self, col, reverse):
        # 取得目前所有 row 的資料
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # 嘗試將資料轉成數字排序，若失敗則以字串排序
        try:
            items.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            items.sort(key=lambda t: t[0], reverse=reverse)

        # 根據排序結果重新排列項目
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

        # 更新排序狀態，下一次點擊要反轉
        self.sort_directions[col] = not reverse
        self.tree.heading(col, command=lambda c=col: self.sort_by_column(c, not reverse))

if __name__ == "__main__":
    root = tk.Tk()
    app = SortableTreeviewApp(root)
    root.mainloop()

'''
class SortableTreeviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview 排序範例")

        self.tree = ttk.Treeview(root, columns=("Name", "Age", "Score"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 設定欄位標題
        for col in ("Name", "Age", "Score"):
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c, False))
            self.tree.column(col, width=100)

        # 放入一些資料
        self.data = [
            ("Alice", 25, 88),
            ("Bob", 30, 75),
            ("Charlie", 22, 90),
            ("David", 28, 65),
            ("Eve", 35, 92),
        ]
        for row in self.data:
            self.tree.insert("", tk.END, values=row)

        # 儲存每個欄位目前的排序狀態
        self.sort_directions = {col: False for col in ("Name", "Age", "Score")}  # False:升序, True:降序

    def sort_by_column(self, col, reverse):
        # 取得目前所有 row 的資料
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # 嘗試將資料轉成數字排序，若失敗則以字串排序
        try:
            items.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            items.sort(key=lambda t: t[0], reverse=reverse)

        # 根據排序結果重新排列項目
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

        # 更新排序狀態，下一次點擊要反轉
        self.sort_directions[col] = not reverse
        self.tree.heading(col, command=lambda c=col: self.sort_by_column(c, not reverse))
'''