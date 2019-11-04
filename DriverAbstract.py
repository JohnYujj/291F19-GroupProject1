# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:12:54 2019

@author: cena R
"""

import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp

class DA(tkinter.Tk):
    #should pass the uid when creating registryAgentApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("driver abstract")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        # input name
        self.lblUsername = Label(self, text="first name", height = 1, width = 10)
        self.lblUsername.grid(sticky="W", row = 1, column = 1)
        self.lblPassword = Label(self, text="last name", height = 1, width = 10)
        self.lblPassword.grid(sticky="W", row = 2, column = 1)
        self.entfname = Entry(self, width = 20)
        self.entfname.grid(sticky="W", row = 1, column = 2)
        self.entlname = Entry(self, width = 20)
        self.entlname.grid(sticky="W", row = 2, column = 2)
        self.empty = Label(self,text = '',height = 1, width = 10)
        self.empty.grid(sticky='w',row = 3, column = 3)
        
        self.btnExit = Button(self, text ="exit", command=self.exitClick)
        self.btnExit.grid(row = 3, column = 1)
        self.btnLogin = Button(self, text ="abstract", command=self.confirmClick)
        self.btnLogin.grid(row = 3, column = 2)
        self.btnticket = Button(self, text ="ticket", command=self.ticketClick)
        self.btnticket.grid(row = 3, column = 3)
        
    def confirmClick(self):
        fname = self.entfname.get()
        lname = self.entlname.get()
        rLife = self.SQLController.AbstractLife(fname,lname)
        rYear = self.SQLController.AbstractYear(fname,lname)
        tLife = self.SQLController.TAbstractLife(fname,lname)
        tYear = self.SQLController.TAbstractYear(fname,lname)
        
        # display result
        self.space = Label(self,text = '',height = 1, width = 10)
        self.space.grid(sticky='w',row = 4, column = 1)
        self.tno = Label(self,text = 'number of tickets',height = 1, width = 15)
        self.tno.grid(sticky='w',row = 5, column = 2)
        self.ddate = Label(self,text = 'number of notices',height = 1, width = 15)
        self.ddate.grid(sticky='w',row = 5, column = 3)
        self.points = Label(self,text = 'sum of points',height = 1, width = 15)
        self.points.grid(sticky='w',row = 5, column = 4)
        self.time1 = Label(self,text = 'lifetime',height = 1, width = 15)
        self.time1.grid(sticky='w',row = 6, column = 1)
        self.time2 = Label(self,text = 'past 2 years',height = 1, width = 15)
        self.time2.grid(sticky='w',row = 7, column = 1)
        self.tno1 = Label(self,text = tLife[0][0],height = 1, width = 15)
        self.tno1.grid(sticky='w',row = 6, column = 2)
        self.ddate1 = Label(self,text = rLife[0][0],height = 1, width = 15)
        self.ddate1.grid(sticky='w',row = 6, column = 3)
        if rLife[0][1] == None:
            self.points1 = Label(self,text = '0',height = 1, width = 15)
        else:
            self.points1 = Label(self,text = rLife[0][1],height = 1, width = 15)
        self.points1.grid(sticky='w',row = 6, column = 4)
        self.tno2 = Label(self,text = tYear[0][0],height = 1, width = 15)
        self.tno2.grid(sticky='w',row = 7, column = 2)
        self.ddate2 = Label(self,text = rYear[0][0],height = 1, width = 15)
        self.ddate2.grid(sticky='w',row = 7, column = 3)
        if rYear[0][1] == None:
            self.points2 = Label(self,text = '0',height = 1, width = 15)
        else:
            self.points2 = Label(self,text = rYear[0][1],height = 1, width = 15)
        self.points2.grid(sticky='w',row = 7, column = 4)
                
    def ticketClick(self):
        fname = self.entfname.get()
        lname = self.entlname.get()
        ticket = self.SQLController.TicketView(fname,lname)
        winTicket = TicketView(ticket)
        winTicket.show()
        
    def exitClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()
        
class TicketView(tkinter.Tk):
    def __init__(self,ticket):
        tkinter.Tk.__init__(self)
        self.title("ticket info")
        self.n = 0
        self.tl = ticket
        
        self.tno = Label(self,text = 'ticket number',height = 1, width = 15)
        self.tno.grid(sticky='w',row = 1, column = 1)
        self.ddate = Label(self,text = 'violation date',height = 1, width = 15)
        self.ddate.grid(sticky='w',row = 1, column = 2)
        self.points = Label(self,text = 'description',height = 1, width = 15)
        self.points.grid(sticky='w',row = 1, column = 3)
        self.points = Label(self,text = 'fine',height = 1, width = 15)
        self.points.grid(sticky='w',row = 1, column = 4)
        self.points = Label(self,text = 'registration number',height = 1, width = 15)
        self.points.grid(sticky='w',row = 1, column = 5)
        self.points = Label(self,text = 'car maker',height = 1, width = 15)
        self.points.grid(sticky='w',row = 1, column = 6)
        self.points = Label(self,text = 'car model',height = 1, width = 15)
        self.points.grid(sticky='w',row = 1, column = 7)
        
        if len(self.tl) > 5:
            self.btnExit = Button(self, text ="exit", command=self.exitClick)
            self.btnExit.grid(row = 7, column = 1)
            self.btnP = Button(self, text ="previous", command=self.preClick)
            self.btnP.grid(row = 7, column = 3)
            self.btnN = Button(self, text ="next", command=self.nextClick)
            self.btnN.grid(row = 7, column = 4)
        else:
            self.btnExit = Button(self, text ="exit", command=self.exitClick)
            self.btnExit.grid(row = len(self.tl)+2, column = 1)
    
    def show(self):
        # display result
        if len(self.tl) > 5:
            for i in range(5):
                if (self.n*5+i) < len(self.tl):
                    self.t = Label(self,text = str(self.tl[self.n*5+i][0]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 1)
                    self.t = Label(self,text = str(self.tl[self.n*5+i][1]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 2)
                    self.t = Label(self,text = str(self.tl[self.n*5+i][2]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 3)
                    self.t = Label(self,text = str(self.tl[self.n*5+i][3]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 4)
                    self.t = Label(self,text = str(self.tl[self.n*5+i][4]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 5)
                    self.t = Label(self,text = str(self.tl[self.n*5+i][5]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 6)
                    self.t = Label(self,text = str(self.tl[self.n*5+i][6]),height = 1, width = 15)
                    self.t.grid(sticky='w',row = i+2, column = 7)
                else:
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 1)
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 2)
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 3)
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 4)
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 5)
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 6)
                    self.empty = Label(self,text = '',height = 1, width = 15)
                    self.empty.grid(sticky='w',row = i+2, column = 7)
        else:
            for i in range(len(self.tl)):
                self.t = Label(self,text = str(self.tl[i][0]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 1)
                self.t = Label(self,text = str(self.tl[i][1]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 2)
                self.t = Label(self,text = str(self.tl[i][2]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 3)
                self.t = Label(self,text = str(self.tl[i][3]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 4)
                self.t = Label(self,text = str(self.tl[i][4]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 5)
                self.t = Label(self,text = str(self.tl[i][5]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 6)
                self.t = Label(self,text = str(self.tl[i][6]),height = 1, width = 15)
                self.t.grid(sticky='w',row = i+2, column = 7)
        
        if len(self.tl) > 5:
            if len(self.tl)%5 == 0:
                self.page = Label(self,text = 'page '+str(self.n+1)+'/'+str(len(self.tl)//5),height = 1, width = 15)
                self.page.grid(sticky='w',row = 7, column = 7)
            else:
                self.page = Label(self,text = 'page '+str(self.n+1)+'/'+str(len(self.tl)//5+1),height = 1, width = 15)
                self.page.grid(sticky='w',row = 7, column = 7)
        else:
            self.page = Label(self,text = 'page '+str(self.n+1)+'/1',height = 1, width = 15)
            self.page.grid(sticky='w',row = len(self.tl)+2, column = 7)
    
    def preClick(self):
        if self.n > 0:
            self.n = self.n-1
            self.show()
    
    def nextClick(self):
        if self.n < len(self.tl)//5:
            self.n = self.n+1
            self.show()
    
    def exitClick(self):
        self.destroy()