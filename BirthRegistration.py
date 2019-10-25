import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import datetime

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
        
        self.btnExit = Button(self, text ="Cancel", command=self.CancelClick)
        self.btnExit.grid(row = 10, column = 1)
        self.btnLogin = Button(self, text ="Ok", command=self.OkClick)
        self.btnLogin.grid(row = 10, column = 2)        
        
    def OkClick(self):
        #todo: handle empty inputs
        #from user entry
        fname = self.entfname.get()
        lname = self.entlname.get()
        gender = self.entgender.get()
        bdate = self.entbdate.get()
        bplace = self.entbplace.get()
        ffname = self.entffname.get()
        flname = self.entflname.get()
        mfname = self.entmfname.get()
        mlname = self.endmlname.get()
        
        #query city
        regplace = self.SQLController.QueryUserCity(self.currentUser)
        
        #get current date
        regdate = datetime.date(datetime.now())
        
        #regno = create random 4 digit regno 1000-9999, then check if it is unique in db
        regno = random.randint(1000,10000)
        while self.SQLController.CheckUniqueBirthRegno(regno):
            regno = random.randint(1000,10000)
        
        #query father and mother (check if exists), launch window to create one if not exists
        dadData = self.SQLController.QueryPersonsAll(ffname, flname)
        if dadData is None:
            #enter persons data window
            pass
        momData = self.SQLController.QueryPersonsAll(mfname, mlname)
        if momData is None:
            #enter persons data window
            pass
        address = momData[0] #whatever the address and phone fields are
        phone = momData[1]
        #births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
        self.SQLController.RegisterBirth(regno, fname, lname, regdate, regplace, gender, ffname, flname, mfname, mlname)
        
        #create person if not already exists
        personData = self.SQLController.QueryPersonsAll(fname,lname)
        if personData is None:
            self.SQLController.CreatePerson(fname, lname, bdate, bplace, address, phone)
        
    def CancelClick(self):
        self.destroy()