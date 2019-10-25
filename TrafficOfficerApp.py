import tkinter
from tkinter import *
import SQLControlClass
import ErrorWindowPopup

class TrafficOfficerApp(tkinter.Tk):
    #should pass the uid when creating TrafficOfficerApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Traffic Officer Window")
        #self.minsize(200,100)
        
        #create SQL controller for this app usage: SQLControlClass.SQLController(Database Path)
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        # |Username|UserType|
        # |Button1          |
        # |Button2          |
        # |ReturnButton     |
        
        self.lblUsername = Label(self, text=self.currentUser)
        self.lblUsername.grid(row = 1, column=1)
       
        #use 'command=' will run the specified function when the button is clicked
        self.btn1 = Button(self, text ="Issue Ticket", command=self.issueTicketClick)
        self.btn1.grid(row = 2, column=1)
        self.btn2 = Button(self, text ="Find Car Owner", command=self.findCarOwnerClick)
        self.btn2.grid(row = 3, column=1)
        self.btn3 = Button(self, text ="Logout", command=self.logoutClick)
        self.btn3.grid(row = 4, column=1)   
        
        
        
    def issueTicketClick(self):
        #launch input window and do sql
        self.SQLController.CommitAndClose()
        self.destroy()
        issueTicket = issueTicketWindow(self.database)
        issueTicketWindow.mainloop()
                   
    
    def findCarOwnerClick(self):
        #launch input window and do sql
        self.destroy()
        findCar = Tk()
        findCar.title("Find Car Owner")        
        pass    
    
    def vehicleRegistrationClick(self):
        #launch input window and do sql
        pass
    
    def logoutClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()   



class issueTicketWindow(tkinter.Tk):
    def __init__(self, dbPath):
        tkinter.Tk.__init__(self)
        self.title("Issue Ticket")
        
        #create SQL controller for this app usage: SQLControlClass.SQLController(Database Path)
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
       
        #use 'command=' will run the specified function when the button is clicked
        self.enterRegLabel = Label(text="Enter a Registration Number")
        self.enterRegLabel.grid(row=1)
        #entry
        self.enterRegEntry = Entry()
        self.enterRegEntry.grid(row=1,column=1)
        #button
        self.enterRegBtn = Button(text="Find",command=print('hello')) 
        self.enterRegBtn.grid(row=1,column=2) 
        
    def findRegClick(self):
        regNo = self.enterRegEntry.get()
        regData = self.SQLController.GetReg(regNo)
        if regData is not None:
            print(regData)
        else:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Registration Number not found")
            winErr.mainloop()            



###TEST######
def main():
    database = './test.db'
    trafOff = TrafficOfficerApp(database, 'traffic officer')
    trafOff.mainloop()
        
if __name__ == '__main__':
    main()