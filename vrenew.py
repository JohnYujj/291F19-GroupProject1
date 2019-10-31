# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 13:58:36 2019

@author: cena R
"""

import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import ErrorWindowPopup
import datetime
from datetime import datetime

class Vrenew(tkinter.Tk):
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("renew vehicle")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        self.regno = Label(self, text="registration number", height = 1, width = 15)
        self.regno.grid(sticky="W", row = 1, column = 1)
        self.entregno = Entry(self, width = 20)
        self.entregno.grid(sticky="W", row = 1, column = 2)
        
        self.btnExit = Button(self, text ="exit", command=self.exitClick)
        self.btnExit.grid(row = 2, column = 1)
        self.btnLogin = Button(self, text ="renew", command=self.renewClick)
        self.btnLogin.grid(row = 2, column = 2)
    
    def renewClick(self):
        regno = self.entregno.get()
        expiry = self.SQLController.Checkexpiry(regno)
        if expiry[0][0] > str(datetime.date(datetime.now())):
            self.SQLController.RenewVbefore(regno,expiry[0][0])
        else:
            self.SQLController.RenewVafter(regno)
        self.SQLController.CommitAndClose()
        self.destroy()
        winErr = ErrorWindowPopup.ErrorWindowPopup("vehicle renew success")
        winErr.mainloop()
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop() 
    
    def exitClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()