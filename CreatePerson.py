import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp

class CreatePersonApp(tkinter.Tk):
    #should pass the uid when creating registryAgentApp to determine who is currently logged in
    def __init__(self, dbPath, fname = None, lname = None, entity = None):
        tkinter.Tk.__init__(self)
        self.title("Add Person")
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        # |fname label  |fname input box |
        # |lname label  |lname input box |
        # |bdate label |bdate input box|
        # |bplace label  |bplace input box |
        # |address label |address input box|
        # |phone label |phone input box|
        
        mainLabelText= "Enter Data For " + entity + ": " + fname + " " + lname
        self.lblMain = Label(self, text=mainLabelText, height = 1, width = 30)
        self.lblMain.grid(sticky="W", row = 1, column = 1)
        
        
        self.lblfname = Label(self, text="First Name: ", height = 1, width = 15)
        self.lblfname.grid(sticky="W", row = 2, column = 1)
        self.lbllname = Label(self, text="Last Name: ", height = 1, width = 15)
        self.lbllname.grid(sticky="W", row = 3, column = 1)
        self.lblbdate = Label(self, text="Birth Date: ", height = 1, width = 15)
        self.lblbdate.grid(sticky="W", row = 4, column = 1)
        self.lblbplace = Label(self, text="Birth Place: ", height = 1, width = 15)
        self.lblbplace.grid(sticky="W", row = 5, column = 1)
        self.lblAddress = Label(self, text="Address: ", height = 1, width = 15)
        self.lblAddress.grid(sticky="W", row = 6, column = 1)
        self.lblPhone = Label(self, text="Phone Number: ", height = 1, width = 15)
        self.lblPhone.grid(sticky="W", row = 7, column = 1)    
        
        self.entfname = Entry(self, width = 20)
        self.entfname.grid(sticky="W", row = 2, column = 2)
        self.entlname = Entry(self, width = 20)
        self.entlname.grid(sticky="W", row = 3, column = 2)
        self.entbdate = Entry(self, width = 20)
        self.entbdate.grid(sticky="W", row = 4, column = 2)     
        self.entbplace = Entry(self, width = 20)
        self.entbplace.grid(sticky="W", row = 5, column = 2)     
        self.entAddress = Entry(self, width = 20)
        self.entAddress.grid(sticky="W", row = 6, column = 2)     
        self.entPhone = Entry(self, width = 20)
        self.entPhone.grid(sticky="W", row = 7, column = 2)     
        
        #no cancel button since this window is for required
        self.btnOk = Button(self, text ="Ok", command=self.OkClick)
        self.btnOk.grid(row = 8, column = 2)
        
        if fname is not None:
            self.entfname.insert(0, fname)
            self.entfname.config(state='disabled')
        if lname is not None:
            self.entlname.insert(0, lname)
            self.entlname.config(state='disabled')
        
    def OkClick(self):
        fname = self.entfname.get()
        lname = self.entlname.get()
        bdate = self.entbdate.get()
        bplace = self.entbplace.get()
        address = self.entAddress.get()
        phone = self.entPhone.get()
        
        self.SQLController.CreatePerson(fname,lname,bdate,bplace,address,phone)
        self.SQLController.CommitAndClose()
        self.destroy()