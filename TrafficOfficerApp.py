# TrafficOfficerApp
# This application is the main menu for traffic officer users.
# The main menu includes an issue ticket button and find car button that 
# opens its respective windows and functions. There is also a logout button
# that closes the application.

import tkinter
from tkinter import *
import SQLControlClass
import ErrorWindowPopup
import IssueTicket
import FindCarOwner

class TrafficOfficerApp(tkinter.Tk):
    #should pass the uid when creating TrafficOfficerApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Traffic Officer Window")
        
        #create SQL controller for this app usage: SQLControlClass.SQLController(Database Path)
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        self.lblUsername = Label(self, text=self.currentUser)
        self.lblUsername.grid(row = 1, column=1)
       
        #use 'command=' will run the specified function when the button is clicked
        self.btn1 = Button(self, text ="Issue Ticket", command=self.issueTicketClick,width=30)
        self.btn1.grid(row = 2, column=1)
        self.btn2 = Button(self, text ="Find Car Owner", command=self.findCarOwnerClick,width=30)
        self.btn2.grid(row = 3, column=1)
        self.btn3 = Button(self, text ="Logout", command=self.logoutClick,width=30)
        self.btn3.grid(row = 4, column=1)   
        
        
        
    def issueTicketClick(self):
        # Launches the IssueTicketApp window
        issueTicket = IssueTicket.IssueTicketApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()           
        issueTicket.mainloop()
                   
    
    def findCarOwnerClick(self):
        # Launches the FindCarOwnerApp window
        findCar = FindCarOwner.FindCarOwnerApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()           
        findCar.mainloop()  
        
    
    def logoutClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()   




#####TEST REMOVE AFTER TESTED######
#def main():
    #database = './test.db'
    #trafOff = TrafficOfficerApp(database, 'username')
    #trafOff.mainloop()
        
#if __name__ == '__main__':
    #main()