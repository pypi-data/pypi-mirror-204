from tkinter import *
class GirdGui:
    def __init__(self,width_=20,height_=10,wid=5,hei=2,title="GirdGui"):
        self.width_ = width_
        self.height_ = height_
        self.wid = wid
        self.hei = hei
        self.excl = {}
        self.tk = Tk()
        self.title = title
        self.tk.title(self.title)
        for w in range(self.width_):
            for h in range(self.height_):
                self.excl[f"ch{w}_{h}"] = Label(self.tk,width=wid,height=hei,relief="raised",bg="white")
                self.excl[f"ch{w}_{h}"].grid(column=w,row=h)
    def delAll(self):
        for w in range(self.width_):
            for h in range(self.height_):
                self.excl[f"ch{w}_{h}"].config(background='white')
                self.excl[f"ch{w}_{h}"].grid(column=w,row=h)
    def draw(self,x,y,color="blue"):
        self.excl[f"ch{x}_{y}"].config(bg=color)
    def display(self):
        self.tk.mainloop()