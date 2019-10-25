import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import ErrorWindowPopup

class LoginApp(tkinter.Tk):
    def __init__(self, dbPath):
        tkinter.Tk.__init__(self)
        self.title("Login Window")
        
        #create SQL controller for this app usage: SQLControlClass.SQLController(Database Path)
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)        
        
        #basically this is grid which is how items in gui are organized
        # |username label|username input box|
        # |password label|password input box|
        # |close button  |process login btn |
        
        self.lblUsername = Label(self, text="Username: ", height = 1, width = 10)
        self.lblUsername.grid(sticky="W", row = 1, column = 1)
        self.lblPassword = Label(self, text="Password: ", height = 1, width = 10)
        self.lblPassword.grid(sticky="W", row = 2, column = 1)
        
        #entry is a text that has get method to get the user's input
        self.entUsername = Entry(self, width = 20)
        self.entUsername.grid(sticky="W", row = 1, column = 2)
        self.entPassword = Entry(self,show="*", width = 20)
        self.entPassword.grid(sticky="W", row = 2, column = 2)
        
        #use 'command=' will run the specified function when the button is clicked
        self.btnExit = Button(self, text ="Exit", command=self.exitClick)
        self.btnExit.grid(row = 3, column = 1)
        self.btnLogin = Button(self, text ="Login", command=self.loginClick)
        self.btnLogin.grid(row = 3, column = 2)
    
    def loginClick(self):
        username = self.entUsername.get()
        password = self.entPassword.get()
        utype = self.SQLController.GetUserType(username,password)
        if utype == 'Registry Agent':
            #create next app to be launched usage: RegistryAgentApp.RegistryAgentApp(Database Path, Username Input)
            winReg = RegistryAgentApp.RegistryAgentApp(self.database,username)
            
            #close this window and launch next
            self.SQLController.CommitAndClose()
            self.destroy()
            winReg.mainloop()
        elif utype == 'Traffic Officer':
            print(type)
            #launch window for traffic officer
            #close sql
        elif utype is None:
            #launch error window usage: ErrorWindowPopup.ErrorWindowPopup(<string>ErrorMsg)
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Invalid Username or Password")
            winErr.mainloop()
    
    def exitClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()