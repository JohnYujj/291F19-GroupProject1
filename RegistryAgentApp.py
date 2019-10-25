import tkinter
from tkinter import *
import SQLControlClass
import LoginApp
import BirthRegistration

class RegistryAgentApp(tkinter.Tk):
    #should pass the uid when creating registryAgentApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Registry Agent Window")
        
        #create SQL controller for this app usage: SQLControlClass.SQLController(Database Path)
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        # |Username|UserType|
        # |Button1          |
        # |Button2          |
        # |Button3          |
        # |Button4          |
        # |Button5          |
        # |Button6          |
        # |ReturnButton     |
        
        self.lblUsername = Label(self, text=self.currentUser, height = 1, width = 20, anchor="w")
        self.lblUsername.grid(sticky="W", row = 1, column = 1)
       
        #use 'command=' will run the specified function when the button is clicked
        self.btn1 = Button(self, text ="Register Birth", command=self.birthRegistrationClick, height = 1, width = 20, anchor="w")
        self.btn1.grid(sticky="W", row = 2, column = 1)
        self.btn2 = Button(self, text ="Register Marriage", command=self.marriageRegistrationClick, height = 1, width = 20, anchor="w")
        self.btn2.grid(sticky="W", row = 3, column = 1)
        self.btn3 = Button(self, text ="Renew Vehicle Registration", command=self.vehicleRegistrationClick, height = 1, width = 20, anchor="w")
        self.btn3.grid(sticky="W", row = 4, column = 1)
        self.btn4 = Button(self, text ="Process Bill of Sale", command=self.processBillClick, height = 1, width = 20, anchor="w")
        self.btn4.grid(sticky="W", row = 5, column = 1)
        self.btn5 = Button(self, text ="Process Payment", command=self.processPaymentClick, height = 1, width = 20, anchor="w")
        self.btn5.grid(sticky="W", row = 6, column = 1)
        self.btn6 = Button(self, text ="Give Driver Abstract", command=self.giveAbstractClick, height = 1, width = 20, anchor="w")
        self.btn6.grid(sticky="W", row = 7, column = 1)
        self.btn7 = Button(self, text ="Logout", command=self.logoutClick, height = 1, width = 20, anchor="w")
        self.btn7.grid(sticky="W", row = 8, column = 1)   
        
        
    def birthRegistrationClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()
        winBirthRegistration = BirthRegistration.BirthRegistrationApp(self.database, self.currentUser)
        winBirthRegistration.mainloop()        
    
    def marriageRegistrationClick(self):
        #launch input window and do sql
        pass    
    
    def vehicleRegistrationClick(self):
        #launch input window and do sql
        pass    
    
    def processBillClick(self):
        #launch input window and do sql
        pass    
    
    def processPaymentClick(self):
        #launch input window and do sql
        pass    
    
    def giveAbstractClick(self):
        #launch input window and do sql
        pass
    
    def logoutClick(self):
        #destroy and create loginwindow
        winLogin = LoginApp.LoginApp(self.database)
        self.SQLController.CommitAndClose()
        self.destroy()
        winLogin.mainloop()