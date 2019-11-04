import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import ErrorWindowPopup
import CreatePerson
import datetime
from datetime import datetime
import random

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
        
        self.btnCancel = Button(self, text ="Cancel", command=self.CancelClick)
        self.btnCancel.grid(row = 10, column = 1)
        self.btnOk = Button(self, text ="Ok", command=self.OkClick)
        self.btnOk.grid(row = 10, column = 2)        
        
    def OkClick(self):
        #todo: handle empty inputs
        #from user entry
        fname = self.entfname.get()
        if len(fname) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: First Name must not be empty")
            winErr.mainloop()
            return
        lname = self.entlname.get()
        if len(lname) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Last Name must not be empty")
            winErr.mainloop()
            return        
        gender = self.entgender.get()
        if len(gender) == 0 or not self.isValidEntryGender(gender):
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Gender must be M or F (m,f)")
            winErr.mainloop()
            return                
        bdate = self.entbdate.get()
        if len(bdate) == 0 or not self.checkDate(bdate):
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Birth Date must be in YYYY-MM-DD format")
            winErr.mainloop()
            return          
        bplace = self.entbplace.get()
        if len(bplace) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Birth Place must not be empty")
            winErr.mainloop()
            return          
        ffname = self.entffname.get()
        if len(ffname) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Father First Name must not be empty")
            winErr.mainloop()
            return             
        flname = self.entflname.get()
        if len(flname) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Father Last Name must not be empty")
            winErr.mainloop()
            return                   
        mfname = self.entmfname.get()
        if len(mfname) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Mother First Name must not be empty")
            winErr.mainloop()
            return                   
        mlname = self.entmlname.get()
        if len(mlname) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Mother Last Name must not be empty")
            winErr.mainloop()
            return                   
        
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
            createDad = CreatePerson.CreatePersonApp(self.database, ffname, flname, "Father")
            createDad.mainloop()
            #user should have to press OK again in this window after creatingdad
            return
        
        momData = self.SQLController.QueryPersonsAll(mfname, mlname)
        if momData is None:
            createMom = CreatePerson.CreatePersonApp(self.database, mfname, mlname, "Mother")
            createMom.mainloop()
            return
        
        address = momData[4] #whatever the address and phone fields are
        phone = momData[5]
        
        birthData = self.SQLController.QueryBirthsAll(fname,lname)
        if birthData is not None:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Birth already exists. First Name, Last Name match found in Births Table.")
            winErr.mainloop()            

        #births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
        birthErr = self.SQLController.CreateBirth(regno, fname, lname, regdate, regplace, gender, ffname, flname, mfname, mlname)
        if birthErr:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: SQL Error in Creating Birth. Please check your inputs are of valid types and do not violate unique ID.")
            winErr.mainloop()
            return  
          
        #create person if not already exists
        personData = self.SQLController.QueryPersonsAll(fname,lname)
        if personData is None:
            createPersonErr = self.SQLController.CreatePerson(fname, lname, bdate, bplace, address, phone)
            if createPersonErr: 
                winErr = ErrorWindowPopup.ErrorWindowPopup("Notice: SQL Error in Creating Person after birth registration.")
                winErr.mainloop()
                #this is ok since birth was still created successfully
        
        self.SQLController.CommitAndClose()
        self.destroy()
        winErr = ErrorWindowPopup.ErrorWindowPopup("Birth Registration Success")
        winErr.mainloop()        
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()        
        
    def CancelClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()    
        
    def checkDate(self,date):
        try:
            datetime.strptime(str(date), '%Y-%m-%d')
        except ValueError:
            return False
        else:
            return True    
        
    def isValidEntryGender(self, gender):
        validEntryList = ['m','f','M','F']
        if gender in validEntryList:
            return True
        else:
            return False