# CarOwnerResults
# This application displays the results of the input provided by the user
# If more than four matches, FindCarOwner will launch the MoreThanFour
# window that allows the user to select from the list of results.
# If less than four matches, FIndCarOwner will launch the LessThanFour 
# window that displays the results

import tkinter
from tkinter import *
import SQLControlClass
import ErrorWindowPopup
import FindCarOwner


class MoreThanFour(tkinter.Tk):
    #Displays results for car owners found if there are more than four matches
    def __init__(self, dbPath, uid, criteria,results):
        tkinter.Tk.__init__(self)
        self.title("Car Owners")
        self.database = dbPath
        self.currentUser = uid
        self.criteria = str(criteria)
        self.results = results
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        #creates layout of window using three frames: top, mid, and bottom
        self.topFrame = Frame(self)
        self.topFrame.grid(row=0)
        self.midFrame = Frame(self)
        self.midFrame.grid(row=1)           
        self.bottomFrame = Frame(self)
        self.bottomFrame.grid(row=2)        
        
        #topFrame - shows userID, criteria given and instructions to select list
        self.lblUsername = Label(self.topFrame, text=self.currentUser, height = 1, width = 20, anchor="w")
        self.lblUsername.grid(sticky="W", row = 0)
        self.criteriaLabel = Label(self.topFrame,text="Showing results for: " + self.criteria)
        self.criteriaLabel.grid(row=1)
        self.selectResult = Label(self.topFrame, text="Please select one of the following")
        self.selectResult.grid(row=2)
        
        
        #midFrame   shows the results with a scrollable box
        self.resultBox = Listbox(self.midFrame,width=40,selectmode=SINGLE,height=6)
        self.resultBox.grid(row=1,columnspan=5)
        self.hSbr = Scrollbar(self.midFrame,orient=VERTICAL,command=self.resultBox.yview)
        self.hSbr.grid(row=1,column=5,sticky=NS)
        self.vSbr = Scrollbar(self.midFrame,orient=HORIZONTAL,command=self.resultBox.xview)
        self.vSbr.grid(row=30,sticky=EW)
        self.resultBox.config(yscrollcommand=self.hSbr.set,xscrollcommand=self.vSbr.set)
        row = 0
        for line in self.results:
            self.resultBox.insert(row, self.results[row][:5])
            row+=1
          
        #bottomFrame - contains back and select button 
        self.backBtn = Button(self.bottomFrame, text="Back",command = self.backToMenu)
        self.backBtn.grid(row=0, column=0)
        self.findOwnerBtn = Button(self.bottomFrame, text="Select",command=self.selectClick) 
        self.findOwnerBtn.grid(row=0,column=1)        
            
            
    def selectClick(self):
        selection = self.resultBox.curselection()
        if len(selection) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Please make a selection.")
            winErr.mainloop()   
        else:
            index = self.resultBox.curselection()[0] #returns row index of selected match
            #Upon selection - new window shows: make,model,year,color,plate,regno, expiry, name
            criteria = self.resultBox.get(self.resultBox.curselection())
            selectedWindow = LessThanFour(self.database, self.currentUser, criteria, [self.results[index]])
            self.SQLController.CommitAndClose()
            self.destroy()          
            selectedWindow.mainloop()            
    
    
    # returns the user back to the main menu of traffic officer
    def backToMenu(self):
        findOwnerMenu = FindCarOwner.FindCarOwnerApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()          
        findOwnerMenu.mainloop()         
        


class LessThanFour(tkinter.Tk):
    #Displays results for car owners found if there are less than four matches
    def __init__(self, dbPath, uid, criteria, results):
        tkinter.Tk.__init__(self)
        self.title("Car Owners")
        self.database = dbPath
        self.currentUser = uid
        self.criteria = str(criteria)
        self.results = results
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        #creates layout of window using three frames: top, mid and bottom
        self.topFrame = Frame(self)
        self.topFrame.grid(row=0)
        self.midFrame = Frame(self)
        self.midFrame.grid(row=1)           
        self.bottomFrame = Frame(self)
        self.bottomFrame.grid(row=2)        
        
        #topFrame - userID, and shows the criteria given
        self.lblUsername = Label(self.topFrame, text=self.currentUser, height = 1, width = 20, anchor=W)
        self.lblUsername.grid(sticky="W", row = 0)
        self.criteriaLabel = Label(self.topFrame,text="Showing results for: " + self.criteria)
        self.criteriaLabel.grid(row=1)
        
        #midFrame - shows the results
        self.makeHeader = Label(self.midFrame,text="Make",relief="groove")
        self.makeHeader.grid(row=0,column=0,ipadx=25)
        self.modelHeader = Label(self.midFrame,text="Model",relief="groove")
        self.modelHeader.grid(row=0,column=1,ipadx=25)
        self.yearHeader = Label(self.midFrame,text="Year",relief="groove")
        self.yearHeader.grid(row=0,column=2,ipadx=25)
        self.colorHeader = Label(self.midFrame,text="Color",relief="groove")
        self.colorHeader.grid(row=0,column=3,ipadx=25)
        self.plateHeader = Label(self.midFrame,text="Plate",relief="groove")
        self.plateHeader.grid(row=0,column=4,ipadx=25)
        self.regdateHeader = Label(self.midFrame,text="RegDate",relief="groove")
        self.regdateHeader.grid(row=0,column=5,ipadx=25)
        self.expiryHeader = Label(self.midFrame,text="Expiry",relief="groove")
        self.expiryHeader.grid(row=0,column=6,ipadx=25)
        self.nameHeader = Label(self.midFrame,text="Name",relief="groove")
        self.nameHeader.grid(row=0,column=7,columnspan=2,ipadx=25)

        #Displays the results and attaches to the window
        rowIndex = 1
        for data in self.results:
            data = list(data)
            print(data)
            for columnIndex in range(9):
                text = str(data[columnIndex])
                textLbl = text + str(columnIndex)
                self.textLbl = Label(self.midFrame,text=text)
                self.textLbl.grid(row=rowIndex,column=columnIndex)
            rowIndex+=1     
           
         #bottomFrame - contains a back button that directs the user back to menu   
        self.backBtn = Button(self.bottomFrame, text="Back",command = self.backToMenu)
        self.backBtn.grid(row=0, column=0)       
            
        
    def backToMenu(self):
        findOwnerMenu = FindCarOwner.FindCarOwnerApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()          
        findOwnerMenu.mainloop()              
                


####TEST REMOVE AFTER TESTED######
#def main():
    #database = './test.db'
    #more = LessThanFour(database, 'username',['red'],[('Chevrolet','Camaro',1969,'red','plate1','2019-06-30','2025-10-09','John','Doe'),('Doge','Challenger',1969,'red','plate2','2016-03-05','2021-09-08','Jane','Doe'),('Doge','Challenger',1969,'red','plate3','2009-01-02','2019-11-19','Miss','Sunny'),('Doge','Challenger',1969,'red','plate4','2017-08-10','2019-10-08','Mister','Sunny')])
    #more.mainloop()
                    
#if __name__ == '__main__':
    #main()