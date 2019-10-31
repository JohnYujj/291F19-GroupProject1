import tkinter
from tkinter import *
import LoginApp
import sys


def main():
    if len(sys.argv) == 1:
        #test database
        database = './test.db'
    else:
        database = str(sys.argv[1])
    winLogin = LoginApp.LoginApp(database)
    winLogin.mainloop()
    
if __name__ == '__main__':
    main()