import tkinter
from tkinter import *

class ErrorWindowPopup(tkinter.Tk):
    def __init__(self, errorMsg):
        tkinter.Tk.__init__(self)
        self.title("Error")
        
        self.lblErr = Label(self, text=errorMsg)
        self.lblErr.grid(row = 1, column = 1)
        self.btnOk = Button(self, text="Ok", command=self.okClick)
        self.btnOk.grid(row = 2, column = 1)
        
    def okClick(self):
        self.destroy()