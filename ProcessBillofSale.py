import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import ErrorWindowPopup
import datetime
from datetime import datetime
import random

class ProcessBillofSale(tkinter.Tk):
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Process Bill of Sale")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        #creates layout of window using three frames: top and bottom
        self.topFrame = Frame(self)
        self.topFrame.grid(row=0)
        self.bottomFrame = Frame(self)
        self.bottomFrame.grid(row=2)
        
        #topFrame - userID, registration number entry and find button
        self.lblUsername = Label(self.topFrame, text=self.currentUser, height = 1, width = 20, anchor="w")
        self.lblUsername.grid(sticky=W, row = 0)       
        self.instructions = Label(self.topFrame,text="Please fill in the following fields:")
        self.instructions.grid(row=1,padx=75,sticky=W)
        
        #bottomFrame
        ##Vin Number
        self.vin = Label(self.bottomFrame,text="VIN:")
        self.vin.grid(row=0,sticky=E,pady=(10,0))
        self.vinEntry = Entry(self.bottomFrame)
        self.vinEntry.grid(row=0,column=1,pady=(10,0))
        ##PlateNumber
        self.plate = Label(self.bottomFrame,text="Plate Number:")
        self.plate.grid(row=1,sticky=E,pady=(10,0))
        self.plateEntry = Entry(self.bottomFrame)
        self.plateEntry.grid(row=1,column=1,pady=(10,0))                
        
        ##Current Owner's first name and last name
        self.curOwner = Label(self.bottomFrame,text="Current Owner:")
        self.curOwner.grid(row=2,sticky=W,pady=(10,0))
        self.cFname = Label(self.bottomFrame,text="First Name:")
        self.cFname.grid(row=3,column=0,sticky=E)
        self.cFnameEntry = Entry(self.bottomFrame)
        self.cFnameEntry.grid(row=3,column=1)
        self.cLname = Label(self.bottomFrame,text="Last Name:")
        self.cLname.grid(row=3,column=2,sticky=E,padx=(20,0))
        self.cLnameEntry = Entry(self.bottomFrame)
        self.cLnameEntry.grid(row=3,column=3)        
        
        ##NewOwner's first name and last name
        self.newOwner = Label(self.bottomFrame,text="New Owner:")
        self.newOwner.grid(row=4,sticky=W,pady=(10,0))
        self.nFname = Label(self.bottomFrame,text="First Name:")
        self.nFname.grid(row=5,column=0,sticky=E)
        self.nFnameEntry = Entry(self.bottomFrame,width=20)
        self.nFnameEntry.grid(row=5,column=1)
        self.nLname = Label(self.bottomFrame,text="Last Name:")
        self.nLname.grid(row=5,column=2,sticky=E,padx=(20,0))
        self.nLnameEntry = Entry(self.bottomFrame)
        self.nLnameEntry.grid(row=5,column=3)        
    
        self.backBtn = Button(self.bottomFrame, text="Back",command = self.backToMenu)
        self.backBtn.grid(row=6,column=0)
        self.processBtn = Button(self.bottomFrame, text="Process",command=self.processClick) 
        self.processBtn.grid(row=6,column=1)      
        
        
        
    def processClick(self):
        #Command for process button
        vin = self.vinEntry.get()
        plate = self.plateEntry.get()
        cfname = self.cFnameEntry.get()
        clname = self.cLnameEntry.get()
        nfname = self.nFnameEntry.get()
        nlname = self.nLnameEntry.get()
        
        regno = random.randint(100,10000)
        while self.SQLController.CheckUniqueRegNo(regno):
            regno = random.randint(100,10000)
            
        todayDate = datetime.date(datetime.now())

        
        #Checks that vin, first and last name of current and new owner and plate are not blank
        if len(vin)==0 or len(cfname)==0 or len(clname)==0 or len(nfname)==0 or len(nlname)==0 or len(plate)==0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Please fill in all fields.")
            winErr.mainloop()
        else:
            currentOwner = self.SQLController.GetCurOwner(vin,plate)
            if currentOwner is None:
                winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Information not found, please try again")
                winErr.mainloop() 
            elif len(currentOwner)>1:
                winErr = ErrorWindowPopup.ErrorWindowPopup("Error: More than 1 result found. Please try again with a different plate number")
                winErr.mainloop()                 
            elif currentOwner[0][0].lower()!=cfname.lower() and currentOwner[0][1].lower()!=clname.lower():
                winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Name of current owner provided does not match the name to the registered vehicle. Please try again")
                winErr.mainloop()
            else:
                processError = self.SQLController.NewVehicleReg(regno,todayDate,plate.title(),vin,nfname.title(),nlname.title())
                if processError == True:
                    winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Could not process bill of sale, please try again.")
                    winErr.mainloop()
                else:
                    updateExpiry = self.SQLController.UpdateExpiry(currentOwner[0][0], currentOwner[0][1], vin, plate, todayDate)
                    self.vinEntry.delete(0,'end')
                    self.cFnameEntry.delete(0,'end')
                    self.cLnameEntry.delete(0,'end')
                    self.nFnameEntry.delete(0,'end')
                    self.nLnameEntry.delete(0,'end')
                    self.plateEntry.delete(0,'end')
                    successMsg = ErrorWindowPopup.ErrorWindowPopup("Successfully processed bill of sale")
                    successMsg.mainloop()
            
        
    def backToMenu(self):
        #Command for back button. Returns user to main traffic officer menu
        registryMenu = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()          
        registryMenu.mainloop()        
        
        


###TEST REMOVE AFTER TESTED######
def main():
    database = './test.db'
    processBill = ProcessBillofSale(database, 'username1')
    processBill.mainloop()
                    
if __name__ == '__main__':
    main()