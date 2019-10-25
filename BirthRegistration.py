import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp

class BirthRegistrationApp(tkinter.Tk):
    #should pass the uid when creating registryAgentApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Register Birth")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        # |fname label  |fname input box |
        # |lname label  |lname input box |
        # |gender label |gender input box|
        # |bdate label  |bdate input box |
        # |bplace label |bplace input box|
        # |ffname label |ffname input box|
        # |flname label |flname input box|  
        # |mfname label |mfname input box|
        # |mlname label |mlname input box|
        # |cancel button|ok button       |
        
        self.lblfname = Label(self, text="First Name: ", height = 1, width = 15)
        self.lblfname.grid(sticky="W", row = 1, column = 1)
        self.lbllname = Label(self, text="Last Name: ", height = 1, width = 15)
        self.lbllname.grid(sticky="W", row = 2, column = 1)
        self.lblgender = Label(self, text="Gender: ", height = 1, width = 15)
        self.lblgender.grid(sticky="W", row = 3, column = 1)
        self.lblbdate = Label(self, text="Birth Date: ", height = 1, width = 15)
        self.lblbdate.grid(sticky="W", row = 4, column = 1)
        self.lblbplace = Label(self, text="Birth Place: ", height = 1, width = 15)
        self.lblbplace.grid(sticky="W", row = 5, column = 1)
        self.lblffname = Label(self, text="Father First Name: ", height = 1, width = 15)
        self.lblffname.grid(sticky="W", row = 6, column = 1)
        self.lblflname = Label(self, text="Father Last Name: ", height = 1, width = 15)
        self.lblflname.grid(sticky="W", row = 7, column = 1)
        self.lblmfname = Label(self, text="Mother First Name: ", height = 1, width = 15)
        self.lblmfname.grid(sticky="W", row = 8, column = 1)        
        self.lblmlname = Label(self, text="Mother Last Name: ", height = 1, width = 15)
        self.lblmlname.grid(sticky="W", row = 9, column = 1)
        
        self.entfname = Entry(self, width = 20)
        self.entfname.grid(sticky="W", row = 1, column = 2)
        self.entlname = Entry(self, width = 20)
        self.entlname.grid(sticky="W", row = 2, column = 2)
        self.entgender = Entry(self, width = 20)
        self.entgender.grid(sticky="W", row = 3, column = 2)     
        self.entbdate = Entry(self, width = 20)
        self.entbdate.grid(sticky="W", row = 4, column = 2)     
        self.entbplace = Entry(self, width = 20)
        self.entbplace.grid(sticky="W", row = 5, column = 2)     
        self.entffname = Entry(self, width = 20)
        self.entffname.grid(sticky="W", row = 6, column = 2)     
        self.entflname = Entry(self, width = 20)
        self.entflname.grid(sticky="W", row = 7, column = 2)     
        self.entmfname = Entry(self, width = 20)
        self.entmfname.grid(sticky="W", row = 8, column = 2)     
        self.entmlname = Entry(self, width = 20)
        self.entmlname.grid(sticky="W", row = 9, column = 2)              
        
    def OkClick(self):
        #todo: handle empty
        fname = self.entfname.get()
        lname = self.entlname.get()
        gender = self.entgender.get()
        bdate = self.entbdate.get()
        bplace = self.entbplace.get()
        ffname = self.entffname.get()
        flname = self.entflname.get()
        mfname = self.entmfname.get()
        mlname = self.endmlname.get()
        #city = get user's city SQL
        #date = get today's date
        #regno = create unique regno (either create one mathematically based on unique key or just random and verify its uniqueness with sql search)
                
        #query father and mother (check if exists), launch window to create one if not exists
        dadData = self.SQLController.QueryParent(ffname, flname, 'father')
        momData = self.SQLController.QueryParent(mfname, mlname, 'mother')
        #get mother's address and phone
        address = momData[0]
        phone = momData[1]
        

        self.SQLController.RegisterBirth(fname,lname,gender,bdate,bplace,ffname,flname,mfname,mlname,city,date,regno,address,phone)
        pass
        
    def CancelClick(self):
        self.destroy()