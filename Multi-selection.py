from tkinter import *


def chage_color():
    color = "pink" if var.get()==1 else("lightgreen" if var.get()==2 else "lightgray")
    fm.config(bg=color)    
    lab.config(bg=fm.cget("bg"))
    python.config(bg=fm.cget("bg"), activebackground=fm.cget("bg"))
    java.config(bg=fm.cget("bg"), activebackground=fm.cget("bg"))
    ruby.config(bg=fm.cget("bg"), activebackground=fm.cget("bg"))

root = Tk()
root.title("Frame")

var = IntVar()
var.set(1)

colorfm = Frame(width=250,height=30,bg="pink")
pinkrb = Radiobutton(colorfm, text="Pink", bg="pink",variable=var, value=1, command=chage_color)
greenrb = Radiobutton(colorfm, text="Green", bg="pink",variable=var, value=2, command=chage_color)
brownrb = Radiobutton(colorfm, text="Gray", bg="pink",variable=var, value=3, command=chage_color)
pinkrb.grid(padx=10, pady=10, row=0, column=0)
greenrb.grid(padx=10, pady=10, row=0, column=1)
brownrb.grid(padx=10, pady=10, row=0, column=2)
colorfm.pack(padx=10,pady=10)

fm = Frame(width=150,height=80,borderwidth=5,bg="lightblue") # 建立框架
lab = Label(fm,text="請複選常用的程式語言",bg="lightblue")     # 建立標籤
lab.pack()

python = Checkbutton(fm,text="Python",bg=fm.cget("bg"),activebackground=fm.cget("bg"))          # 建立python核取方塊          
python.pack(anchor=W)
java = Checkbutton(fm,text="Java",bg=fm.cget("bg"),activebackground=fm.cget("bg"))              # 建立java核取方塊
java.pack(anchor=W)
ruby = Checkbutton(fm,text="Ruby",bg=fm.cget("bg"),activebackground=fm.cget("bg"))              # 建立ruby核取方塊
ruby.pack(anchor=W)
fm.pack(padx=10,pady=10)                        # 包裝框架

root.mainloop()








