import tkinter
from tkinter import *
import SQLControlClass
import RegistryAgentApp
import ErrorWindowPopup
import datetime
from datetime import datetime
import random

class ProcessPaymentApp(tkinter.Tk):
    #should pass the uid when creating registryAgentApp to determine who is currently logged in
    def __init__(self, dbPath, uid):
        tkinter.Tk.__init__(self)
        self.title("Register Birth")
        self.currentUser = uid
        self.database = dbPath
        self.SQLController = SQLControlClass.SQLController(self.database)
        
        # |ticket no.|ticket input box |
        # |payment   |payment input box|
        # |cancel button|ok button       |
        
        self.lbltno = Label(self, text="Ticket Number: ", height = 1, width = 15)
        self.lbltno.grid(sticky="W", row = 1, column = 1)
        self.lblamt = Label(self, text="Payment Amount: ", height = 1, width = 15)
        self.lblamt.grid(sticky="W", row = 2, column = 1)
        
        self.enttno = Entry(self, width = 20)
        self.enttno.grid(sticky="W", row = 1, column = 2)
        self.entamt = Entry(self, width = 20)
        self.entamt.grid(sticky="W", row = 2, column = 2)   
        
        self.btnCancel = Button(self, text ="Cancel", command=self.CancelClick)
        self.btnCancel.grid(row = 3, column = 1)
        self.btnOk = Button(self, text ="Ok", command=self.OkClick)
        self.btnOk.grid(row = 3, column = 2)        
        
    def OkClick(self):
        #TODO: handle empty inputs
        #from user entry
        tno = self.enttno.get()
        if len(tno) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Ticket Number must not be Empty")
            winErr.mainloop()
            return
        amount = self.entamt.get()
        if len(amount) == 0:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Payment Amount must not be Empty")
            winErr.mainloop()
            return     
        amount = int(amount)
        #todays date
        pdate = datetime.date(datetime.now())
        
        #get ticket fine and all payments
        fine = self.SQLController.GetTicketFine(tno)
        if fine is None:
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: Fine not Found. Verify ticket number.")
            winErr.mainloop()
            return
        fine = int(fine[0])
        payments = self.SQLController.GetAllPayments(tno)
        previousPayments = 0
        for payment in payments:
            previousPayments += payment[0]
        balanceAfterPayment = fine - previousPayments - amount
        maxPayment = fine - previousPayments
        
        #if all payments + current payment > fine, show invalid msg and return no action  
        if balanceAfterPayment < 0:
            msg = "Error: Total Payments Exceed Fine. Max Payment is %d." %(maxPayment)
            winErr = ErrorWindowPopup.ErrorWindowPopup(msg)
            return
        
        #otherwise, process payment   
        error = self.SQLController.ProcessPayment(tno,pdate,amount)
        if error: 
            winErr = ErrorWindowPopup.ErrorWindowPopup("Error: SQL Error in Process Payment. Please check your Ticket Number. Ticket Number and Date are the Unique ID (Maximum 1 payment per ticket per day).")
            winErr.mainloop()
        else:
            self.SQLController.CommitAndClose()
            self.destroy()
            msg = "Payment Success. Remaining Balance %d." %(balanceAfterPayment)
            winErr = ErrorWindowPopup.ErrorWindowPopup(msg)
            winErr.mainloop()        
            winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
            winReg.mainloop()
        
    def CancelClick(self):
        self.SQLController.CommitAndClose()
        self.destroy()
        winReg = RegistryAgentApp.RegistryAgentApp(self.database,self.currentUser)
        winReg.mainloop()        