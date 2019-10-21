import tkinter
from tkinter import *

class ErrorWindowPopup(tkinter.Tk):
    def __init__(self, errorMsg):
        tkinter.Tk.__init__(self)
        self.title("Error")
        
        #pack will auto space them
        self.lblErr = Label(self, text=errorMsg)
        self.lblErr.pack()
        self.btnOk(self, text="Ok", command=self.okClick)
        self.btnOk.pack()
        
    def okClick(self):
        self.destroy()