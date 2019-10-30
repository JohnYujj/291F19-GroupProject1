# FindCarOwnerApp
# This application is a window launch that allows the user to look for the owner
# of a car by providing one of: make, model, year, color, and plate.
# The applications will take the user's input to find the matches in the database
# and returns the results in a new window depending on the amount of matches.

import tkinter
from tkinter import *
import SQLControlClass
import TrafficOfficerApp
import ErrorWindowPopup
import CarOwnerResults


class FindCarOwnerApp(tkinter.Tk):
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Find Car Owner")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        self.error = None
        
        #Creates layout of window using three frames: top and bottom
        self.topFrame = Frame(self)
        self.topFrame.grid(row=0)
        self.bottomFrame = Frame(self)
        self.bottomFrame.grid(row=1)        
        
        #topFrame - userID and enter registration number
        self.lblUsername = Label(self.topFrame, text=self.currentUser, height = 1, width = 20, anchor="w")
        self.lblUsername.grid(sticky="W", row = 0)
        self.instructions = Label(self.topFrame, text="Please fill in one or more of the following fields")
        self.instructions.grid(row = 1)         
        
        #bottomFrame - displays entry for user input, find owner, and back button
        self.make = Label(self.bottomFrame,text="Make:")
        self.make.grid(row=0,sticky=E)
        self.makeEntry = Entry(self.bottomFrame)
        self.makeEntry.grid(row=0,column=1)
        self.model = Label(self.bottomFrame,text="Model:")
        self.model.grid(row=1,sticky=E)
        self.modelEntry = Entry(self.bottomFrame)
        self.modelEntry.grid(row=1,column=1)
        self.year = Label(self.bottomFrame,text="Year:")
        self.year.grid(row=2,sticky=E)
        self.yearEntry = Entry(self.bottomFrame)
        self.yearEntry.grid(row=2,column=1)    
        self.color = Label(self.bottomFrame,text="Color:")
        self.color.grid(row=3,sticky=E)
        self.colorEntry = Entry(self.bottomFrame)
        self.colorEntry.grid(row=3,column=1)      
        self.plate = Label(self.bottomFrame,text="Plate:")
        self.plate.grid(row=4,sticky=E)
        self.plateEntry = Entry(self.bottomFrame)
        self.plateEntry.grid(row=4,column=1)          
                 
        self.findOwnerBtn = Button(self.bottomFrame, text="Find Owner",command=self.findOwnerClick) 
        self.findOwnerBtn.grid(row=5,column=1)        
        self.backBtn = Button(self.bottomFrame, text="Back",command = self.backToMenu)
        self.backBtn.grid(row=5, column=0)
        
    
    def findOwnerClick(self):
        make = self.makeEntry.get()
        model = self.modelEntry.get()
        year = self.yearEntry.get()
        color = self.colorEntry.get()
        plate = self.plateEntry.get()
        #Checks to see that at least one entry is filled
        if len(make)==0 and len(model)==0 and len(year)==0 and len(color)==0 and len(plate)==0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Please fill in at least one field.")
            winErr.mainloop()
        else:
            #Obtains the results of the search from the user's entries
            results = self.SQLController.FindCarOwner(make,model,year,color,plate)
            if len(results)==0:
                #If no matches are found an error window will appear
                winErr = ErrorWindowPopup.ErrorWindowPopup("No matches found for given criteria.")
                winErr.mainloop()                
            elif len(results)>4:
                #If more than 4 matches - MoreThanFour window will appear
                resultsMore = CarOwnerResults.MoreThanFour(self.database, self.currentUser, [make,model,year,color,plate],results)
                self.SQLController.CommitAndClose()
                self.destroy() 
                resultsMore.mainloop()
            elif len(results)<=4:
                #If less than 4 - LessThanFour window will appear
                resultsLess = CarOwnerResults.LessThanFour(self.database, self.currentUser, [make,model,year,color,plate],results)
                self.SQLController.CommitAndClose()
                self.destroy()
                resultsLess.mainloop()
                
        
    def backToMenu(self):
        # returns the user back to the Traffic Officer Menu Window
        trafficOfficerMenu = TrafficOfficerApp.TrafficOfficerApp(self.database,self.currentUser)
        self.SQLController.CommitAndClose()
        self.destroy()          
        trafficOfficerMenu.mainloop()        
        
        


####TEST REMOVE AFTER TESTED######
#def main():
    #database = './test.db'
    #findCar = FindCarOwnerApp(database, 'Find Car Owner')
    #findCar.mainloop()
                    
#if __name__ == '__main__':
    #main()