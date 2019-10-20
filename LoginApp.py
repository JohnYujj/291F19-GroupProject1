import tkinter
from tkinter import *
import sqlite3


class SQLController:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        
    #def check_if_userExists returns bool depending if select from users uid=uid found or not
    #def check_if_uid-pw_match returns bool depending if select user uid/pwd match found or not
    
    def GetUserType(self, username,password):
        self.cursor.execute('SELECT utype FROM users WHERE uid=:username AND pwd=:password',{"username":username,"password":password})
        user = self.cursor.fetchone()
        uType=user[0]
        self.connection.commit()
        return uType        

class LoginApp(tkinter.Tk):
    def __init__(self, SQL):
        tkinter.Tk.__init__(self)
        self.title("Login Window")
        self.SQLController = SQL
        
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
            #launch window for registry agent
            #close sql
        elif utype == 'Traffic Officer':
            print(type)
            #launch window for traffic officer
            #close sql
    
    def exitClick(self):
        self.destroy()

def main():
    database = './test.db'
    appSQL = SQLController(database)
    
    winLogin = LoginApp(appSQL)
    winLogin.mainloop()
    
if __name__ == '__main__':
    main()