# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:58:59 2019

@author: cena R
"""

import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import datetime
from datetime import datetime
import random
import CreatePerson

class MarriageRegistrationApp(tkinter.Tk):
    #should pass the uid when creating registryAgentApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("register marriage")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        self.pfname1 = Label(self, text="First Name 1", height = 1, width = 15)
        self.pfname1.grid(sticky="W", row = 1, column = 1)
        self.plname1 = Label(self, text="Last Name 1", height = 1, width = 15)
        self.plname1.grid(sticky="W", row = 2, column = 1)
        self.pfname2 = Label(self, text="First Name 2", height = 1, width = 15)
        self.pfname2.grid(sticky="W", row = 3, column = 1)
        self.plname2 = Label(self, text="Last Name 2", height = 1, width = 15)
        self.plname2.grid(sticky="W", row = 4, column = 1)
        self.entpfname1 = Entry(self, width = 20)
        self.entpfname1.grid(sticky="W", row = 1, column = 2)
        self.entplname1 = Entry(self, width = 20)
        self.entplname1.grid(sticky="W", row = 2, column = 2)
        self.entpfname2 = Entry(self, width = 20)
        self.entpfname2.grid(sticky="W", row = 3, column = 2)
        self.entplname2 = Entry(self, width = 20)
        self.entplname2.grid(sticky="W", row = 4, column = 2)
        self.empty = Label(self,text = '',height = 1, width = 3)
        self.empty.grid(sticky='w',row = 1, column = 3)
        
        self.btnExit = Button(self, text ="exit", command=self.exitClick)
        self.btnExit.grid(row = 5, column = 1)
        self.btnLogin = Button(self, text ="confirm", command=self.confirmClick)
        self.btnLogin.grid(row = 5, column = 2)
    
    def confirmClick(self):
        pfname1 = self.entpfname1.get()
        plname1 = self.entplname1.get()
        pfname2 = self.entpfname2.get()
        plname2 = self.entplname2.get()
        regdate = datetime.date(datetime.now())
        regplace = self.SQLController.QueryUserCity(self.currentUser)
        regno = random.randint(1000,10000)
        while self.SQLController.CheckUniqueMarriageRegno(regno):
            regno = random.randint(1000,10000)
            
        p1Data = self.SQLController.QueryPersonsAll(pfname1, plname1)
        if p1Data is None:
            createP = CreatePerson.CreatePersonApp(self.database, pfname1, plname2, "p1")
            createP.mainloop()
            return
        p2Data = self.SQLController.QueryPersonsAll(pfname2, plname2)
        if p2Data is None:
            createP = CreatePerson.CreatePersonApp(self.database, pfname2, plname2, "p2")
            createP.mainloop()
            return
        
        self.SQLController.MarriageReg(regno,regdate,regplace,pfname1,plname1,pfname2,plname2)
        
        winErr = ErrorWindowPopup.ErrorWindowPopup("marriage registration success")
        winErr.mainloop()        
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()  
    
    def exitClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()  