import tkinter
from tkinter import *
#Frame from tkinter
class LoginApp(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Login Window")
        
        self.lblUsername = Label(self, text="Username: ")
        self.lblUsername.grid(row = 1, column = 1)
        self.lblPassword = Label(self, text="Password: ")
        self.lblPassword.grid(row = 2, column = 1)
        self.entUsername = Entry(self)
        self.entUsername.grid(row = 1, column = 2)
        self.entPassword = Entry(self)
        self.entPassword.grid(row = 2, column = 2)        
        
        self.exitButton = Button(self, text ="Exit", command=self.exitClick)
        self.exitButton.grid(row = 3, column = 1)
        self.loginButton = Button(self, text ="Login", command=self.loginClick)
        self.loginButton.grid(row = 3, column = 2)       
    
    def getUsername(self):
        username = self.entUsername.get()
        return username
    
    def getPassword(self):
        password = self.entPassword.get()
        return password
    
    def loginClick(self):
        username = self.getUsername()
        password = self.getPassword()
        #do SQL here
        print(username)
        print(password)
    
    def exitClick(self):
        self.destroy()

def main():
    winLogin = LoginApp()
    winLogin.mainloop()
    
if __name__ == '__main__':
    main()