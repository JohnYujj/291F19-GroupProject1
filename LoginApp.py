import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import ErrorWindowPopup

class LoginApp(tkinter.Tk):
    def __init__(self, dbPath):
        tkinter.Tk.__init__(self)
        self.title("Login Window")
        
        #create SQL controller for this app, remember to commit it when exiting app or when next statement needed
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
        self.entPassword = Entry(self,show="*")
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
            print(utype) #debug msg
            #call this before closing an app since each app has independent sqlcontroller
            self.SQLController.CommitAndClose()
            #create next app to be launched
            winReg = RegistryAgentApp.RegistryAgentApp(self.database,username)
            #close current window
            self.destroy()
            #launch next window
            winReg.mainloop()
        elif utype == 'Traffic Officer':
            print(type)
            #launch window for traffic officer
            #close sql
        elif utype is None:
            #launch error window invalid pass
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Invalid Username or Password")
            winErr.mainloop()
    
    def exitClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()