import tkinter
from tkinter import *
import SQLControlClass
import LoginApp


def main():
    database = './test.db'
    winLogin = LoginApp.LoginApp(database)
    winLogin.mainloop()
    
if __name__ == '__main__':
    main()