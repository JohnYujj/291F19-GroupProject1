import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp

class LoginApp(tkinter.Tk):
    def __init__(self, dbPath):
        tkinter.Tk.__init__(self)
        self.title("Login Window")
        
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)        
        
        #basically this is grid which is how items in gui are organized
        # |username label|username input box|
        # |password label|password input box|
        # |close button  |process login btn |
        
        self.lblUsername = Label(self, text="Username: ")
        self.lblUsername.grid(row = 1, column = 1)
        self.lblPassword = Label(self, text="Password: ")
        self.lblPassword.grid(row = 2, column = 1)
        
        #entry is a text that has get method to get the user's input
        self.entUsername = Entry(self)
        self.entUsername.grid(row = 1, column = 2)
        self.entPassword = Entry(self)
        self.entPassword.grid(row = 2, column = 2)
        entryList = [self.entUsername, self.entPassword]
        
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
            print(utype)
            self.SQLController.CommitAndClose()
            winReg = RegistryAgentApp.RegistryAgentApp(self.database,username)
            self.destroy()
            winReg.mainloop()
            #close sql
        elif utype == 'Traffic Officer':
            print(type)
            #launch window for traffic officer
            #close sql
    
    def exitClick(self):
        self.destroy()