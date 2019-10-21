import tkinter
from tkinter import *
import SQLControlClass

class RegistryAgentApp(tkinter.Tk):
    #should pass the uid when creating registryAgentApp
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Registry Agent Window")
        
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
        
        self.lblUsername = Label(self, text=uid)
        self.lblUsername.grid(row = 1, column = 1)
       
        #use 'command=' will run the specified function when the button is clicked
        self.btn1 = Button(self, text ="Register Birth", command=self.birthRegistrationClick)
        self.btn1.grid(row = 2, column = 1)
        self.btn2 = Button(self, text ="Register Marriage", command=self.marriageRegistrationClick)
        self.btn2.grid(row = 3, column = 1)
        self.btn2 = Button(self, text ="Renew Vehicle Registration", command=self.vehicleRegistrationClick)
        self.btn2.grid(row = 4, column = 1)
        self.btn2 = Button(self, text ="Process Bill of Sale", command=self.processBillClick)
        self.btn2.grid(row = 5, column = 1)
        self.btn2 = Button(self, text ="Process Payment", command=self.processPaymentClick)
        self.btn2.grid(row = 6, column = 1)
        self.btn2 = Button(self, text ="Give Driver Abstract", command=self.giveAbstractClick)
        self.btn2.grid(row = 7, column = 1)
        self.btn2 = Button(self, text ="Logout", command=self.logoutClick)
        self.btn2.grid(row = 8, column = 1)   
        
        
    def birthRegistrationClick(self):
        #launch input window and do sql
        pass            
    
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
        #destroy and go back to loginWindow
        pass