import tkinter
from tkinter import *
import SQLControlClass
import TrafficOfficerApp
import ErrorWindowPopup
import datetime
from datetime import datetime
import random


class IssueTicketApp(tkinter.Tk):
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Issue Ticket")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        #creates layout of window using three frames: top, mid, and bottom
        self.topFrame = Frame(self)
        self.topFrame.grid(row=0)
        self.midFrame = Frame(self,height=50,width=300,bg='white')
        self.midFrame.grid(row=1)        
        self.bottomFrame = Frame(self)
        self.bottomFrame.grid(row=2)
        
        #topFrame - userID and enter registration number
        self.lblUsername = Label(self.topFrame, text=self.currentUser, height = 1, width = 20, anchor="w")
        self.lblUsername.grid(sticky="W", row = 0)       
        self.enterRegLabel = Label(self.topFrame,text="Enter a Registration Number")
        self.enterRegLabel.grid(row=1)
        self.enterRegEntry = Entry(self.topFrame)
        self.enterRegEntry.grid(row=1,column=1)
        self.enterRegBtn = Button(self.topFrame, text="Find", command=self.findRegClick) 
        self.enterRegBtn.grid(row=1,column=2)
        
        #midFrame - displays the make, model, year, and color
        ##HEADERS
        self.nameHeader = Label(self.midFrame,text="Name",relief="groove")
        self.nameHeader.grid(row=0,column=0,ipadx=25)        
        self.makeHeader = Label(self.midFrame,text="Make",relief="groove")
        self.makeHeader.grid(row=0,column=1,ipadx=25)
        self.modelHeader = Label(self.midFrame,text="Model",relief="groove")
        self.modelHeader.grid(row=0,column=2,ipadx=25)
        self.yearHeader = Label(self.midFrame,text="Year",relief="groove")
        self.yearHeader.grid(row=0,column=3,ipadx=25)
        self.colorHeader = Label(self.midFrame,text="Color",relief="groove")
        self.colorHeader.grid(row=0,column=4,ipadx=25) 
        ##DATA
        self.name = Label(self.midFrame,text="",bg='white')
        self.name.grid(row=1,column=0)        
        self.make = Label(self.midFrame,text="",bg='white')
        self.make.grid(row=1,column=1)  
        self.model = Label(self.midFrame,text="",bg='white')
        self.model.grid(row=1,column=2)   
        self.year = Label(self.midFrame,text="",bg='white')
        self.year.grid(row=1,column=3)          
        self.color = Label(self.midFrame,text="",bg='white')
        self.color.grid(row=1,column=4)         
    
        #bottomFrame - violation date, text,fine amount and issues ticket
        self.vDate = Label(self.bottomFrame,text="Violation Date (YYYY-MM-DD):")
        self.vDate.grid(row=0,column=0,sticky=E)        
        self.vDateEntry = Entry(self.bottomFrame)
        self.vDateEntry.grid(row=0,column=1)
        self.vText = Label(self.bottomFrame,text="Violation Text:")
        self.vText.grid(row=1,column=0,sticky=E)        
        self.vTextEntry = Entry(self.bottomFrame)
        self.vTextEntry.grid(row=1,column=1)   
        self.fineAmt = Label(self.bottomFrame,text="Fine Amount:")
        self.fineAmt.grid(row=2,column=0,sticky=E)        
        self.fineAmtEntry = Entry(self.bottomFrame)
        self.fineAmtEntry.grid(row=2,column=1)          
        
        self.issueBtn = Button(self.bottomFrame, text="Issue Ticket",command = self.issueClick) 
        self.issueBtn.grid(row=3,column=1)        
        self.backBtn = Button(self.bottomFrame, text="Back",command = self.backToMenu)
        self.backBtn.grid(row=3, column=0)
        
        
    def findRegClick(self):
        regNo = self.enterRegEntry.get()
        regData = self.SQLController.GetReg(regNo)
        if len(regNo) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Please enter a registration number")
            winErr.mainloop()               
        elif regData is None:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Registration Number not found")
            winErr.mainloop()             
        else:
            self.showData(regData)
            
            
    def showData(self,data):
        self.name.config(text=data[0]+' '+data[1])
        self.make.config(text=data[2])
        self.model.config(text=data[3])
        self.year.config(text=data[4])  
        self.color.config(text=data[5])
        
        
    def issueClick(self):
        regNo = self.enterRegEntry.get()
        vDate = self.vDateEntry.get()
        text = self.vTextEntry.get()
        fineAmt = self.fineAmtEntry.get()
        ticketNo = random.randint(0,1000)
        while self.SQLController.CheckUniqueTicketNo(ticketNo):
            ticketNo = random.randint(0,1000)
        #If a date is not given, today's date will be supplied
        if len(vDate)==0:
            vDate = datetime.date(datetime.now())    
        #Checks that registration number, text, and fine amount are not blank
        if len(regNo)==0 or len(text)==0 or len(fineAmt)==0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Please fill in a valid registration number, violation text and fine amount.")
            winErr.mainloop()
        else:
            #Creates ticket and clears fields
            self.SQLController.CreateTicket(ticketNo, regNo, fineAmt, text, vDate)
            self.enterRegEntry.delete(0,'end')
            self.vDateEntry.delete(0,'end')
            self.vTextEntry.delete(0,'end')
            self.fineAmtEntry.delete(0,'end')
            self.showData(['','','','','',''])
            successMsg = ErrorWindowPopup.ErrorWindowPopup("Successfully issued ticket")
            successMsg.mainloop()
            
        
    def backToMenu(self):
        trafficOfficerMenu = TrafficOfficerApp.TrafficOfficerApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()          
        trafficOfficerMenu.mainloop()        
        
        


###TEST######
#def main():
    #database = './test.db'
    #isTi = IssueTicketApp(database, 'issueticket')
    #isTi.mainloop()
                    
#if __name__ == '__main__':
    #main()