import sqlite3

class SQLController:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    ##QUERYING USER
    def GetUserType(self, username,password):
        self.cursor.execute('SELECT utype FROM users WHERE uid=:username AND pwd=:password',{"username":username,"password":password})
        user = self.cursor.fetchone()
        self.connection.commit()
        if user is None: 
            return None
        else:
            uType=user[0]
            return uType    
        
    def QueryUserCity(self, username):
        self.cursor.execute('SELECT city FROM users WHERE uid=:username',{"username":username})
        city = self.cursor.fetchone()
        if city is None:
            return None
        else: 
            return city[0]
        
    ##QUERYING BIRTHS   
    def CheckUniqueBirthRegno(self, regno):
        self.cursor.execute('SELECT * FROM births WHERE regno=:regno',{"regno":regno})
        result = self.cursor.fetchone()
        if result is None:
            #if nothing found, the regno is unique and does not exist yet
            return False
        else:
            return True
    
    def CreateBirth(self, regno, fname, lname, regdate, regplace, gender, ffname, flname, mfname, mlname):
        self.cursor.execute('INSERT INTO births VALUES(:regno ,:fname ,:lname ,:regdate ,:regplace ,:gender,:ffname,:flname,:mfname,:mlname)',{"regno":regno, "fname":fname, "lname":lname, "regdate":regdate, "regplace":regplace, "gender":gender, "ffname":ffname, "flname":flname, "mfname":mfname, "mlname":mlname})

    ##QUERYING PERSONS
    def QueryPersonsAll(self, first, last):
        self.cursor.execute('SELECT * FROM persons WHERE fname=:first AND lname=:last',{"first":first, "last":last})
        person = self.cursor.fetchone()
        if person is None:
            return None
        else:
            return person
        
    def CreatePerson(self, fname, lname, bdate, bplace, address, phone):
        self.cursor.execute('INSERT INTO persons VALUES(:fname ,:lname ,:bdate ,:bplace ,:address ,:phone)',{"fname":fname, "lname":lname, "bdate":bdate, "bplace":bplace, "address":address, "phone":phone})
        self.connection.commit()
        
    ##QUERY TICKETS
    def GetTicketFine(self, ticketnum):
        self.cursor.execute('SELECT fine FROM tickets WHERE tno=:ticketnum',{'ticketnum':ticketnum})
        fine = self.cursor.fetchone()
        return int(fine[0])    
    
    ##QUERY PAYMENTS
    def GetAllPayments(self, ticketnum):
        self.cursor.execute('SELECT amount FROM payments WHERE tno=:ticketnum',{'ticketnum':ticketnum})
        payments = self.cursor.fetchall()
        return payments
        
    def ProcessPayment(self, ticketnum, ticketdate, ticketamount):
        try:
            self.cursor.execute('INSERT INTO payments VALUES(:ticketnum, :ticketdate, :ticketamount)',{'ticketnum':ticketnum, 'ticketdate':ticketdate, 'ticketamount':ticketamount})
            self.connection.commit()
        except:
            #Return True if error happened in sql execution
            #sqlite3 module in python cannot return specific error, can only say some error happened and make guess on cause. 
            return True
        
    ##TRAFFIC OFFICER##
    ##ISSUE TICKET APP
    def GetReg(self, rn):
        self.cursor.execute('SELECT fname, lname, make, model, year, color FROM registrations r, vehicles v WHERE r.vin = v.vin AND regno=:number',{"number":rn})
        reg = self.cursor.fetchone()  
        self.connection.commit()
        if reg is None:
            return None
        else:
            return reg 
        
    def CheckUniqueTicketNo(self, tno):
        self.cursor.execute('SELECT * FROM tickets WHERE tno=:tno',{"tno":tno})
        result = self.cursor.fetchone()
        if result is None:
            return False
        else:
            return True 
        
    def CreateTicket(self, tno, regno, fine, violation, vdate):
        self.cursor.execute('INSERT INTO tickets VALUES(:tno ,:regno ,:fine ,:violation ,:vdate)',{"tno":tno, "regno":regno, "fine":fine, "violation":violation, "vdate":vdate})
        self.connection.commit()    
        
    def CommitAndClose(self):
        self.connection.commit()	
        self.connection.close()