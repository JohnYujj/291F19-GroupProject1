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
        try:
            self.cursor.execute('INSERT INTO births VALUES(:regno ,:fname ,:lname ,:regdate ,:regplace ,:gender,:ffname,:flname,:mfname,:mlname)',{"regno":regno, "fname":fname, "lname":lname, "regdate":regdate, "regplace":regplace, "gender":gender, "ffname":ffname, "flname":flname, "mfname":mfname, "mlname":mlname})
            self.connection.commit()
        except:
            return True

    ##QUERYING PERSONS
    def QueryPersonsAll(self, first, last):
        self.cursor.execute('SELECT * FROM persons WHERE fname=:first COLLATE NOCASE AND lname=:last COLLATE NOCASE',{"first":first, "last":last})
        person = self.cursor.fetchone()
        if person is None:
            return None
        else:
            return person
        
    def CreatePerson(self, fname, lname, bdate, bplace, address, phone):
        try:
            self.cursor.execute('INSERT INTO persons VALUES(:fname ,:lname ,:bdate ,:bplace ,:address ,:phone)',{"fname":fname, "lname":lname, "bdate":bdate, "bplace":bplace, "address":address, "phone":phone})
            self.connection.commit()
        except:
            return True
    ##QUERY TICKETS
    def GetTicketFine(self, ticketnum):
        self.cursor.execute('SELECT fine FROM tickets WHERE tno=:ticketnum',{'ticketnum':ticketnum})
        fine = self.cursor.fetchone()
        return fine 
    
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
        
    ###PROCESS BILL OF SALE
    def CheckUniqueRegNo(self, regno):
        self.cursor.execute('SELECT * FROM registrations WHERE regno=:regno',{"regno":regno})
        result = self.cursor.fetchone()
        self.connection.commit()
        if result is None:
            return False
        else:
            return True    
    
    def GetCurOwner(self, vin, plate):        
        self.cursor.execute('SELECT fname,lname FROM registrations WHERE vin=:vin AND plate=:plate COLLATE NOCASE GROUP BY regno HAVING MAX(regdate)',{'vin':vin,'plate':plate})
        result = self.cursor.fetchall()
        self.connection.commit()
        if len(result)==0:
            return None
        else:
            return result   
        
        
    def NewVehicleReg(self,regno,regdate,plate,vin,fname,lname):
        self.cursor.execute("SELECT date('now','+1 years')")
        self.connection.commit()
        result = self.cursor.fetchone()
        expiry = result[0]
        
        try:
            self.cursor.execute('INSERT INTO registrations VALUES(:regno, :regdate, :expiry, :plate, :vin, :fname, :lname)',{"regno":regno, "regdate":regdate, "expiry":expiry, "plate":plate, "vin":vin, "fname":fname, "lname":lname})
            self.connection.commit()
        except:
            return True

    
    def UpdateExpiry(self,fname, lname, vin, plate, expiry):
        try:
            self.cursor.execute('UPDATE registrations SET expiry=:expiry WHERE fname LIKE %:fname% AND lname LIKE %:lname% AND vin=:vin AND plate LIKE %:plate%',{'expiry':expiry,'fname':fname,'lname':lname,'vin':vin,'plate':plate})
            self.connection.commit()
        except:
            return True   
        
        
    ##TRAFFIC OFFICER##
    ##ISSUE TICKET APP
    def FindRegVehicle(self, rn):
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
        self.connection.commit()
        if result is None:
            return False
        else:
            return True 
        
    def CreateTicket(self, tno, regno, fine, violation, vdate):
        try:
            self.cursor.execute('INSERT INTO tickets VALUES(:tno ,:regno ,:fine ,:violation ,:vdate)',{"tno":tno, "regno":regno, "fine":fine, "violation":violation, "vdate":vdate})
            self.connection.commit()
        except:
            return True
        
        self.cursor.execute('INSERT INTO tickets VALUES(:tno ,:regno ,:fine ,:violation ,:vdate)',{"tno":tno, "regno":regno, "fine":fine, "violation":violation, "vdate":vdate})
        self.connection.commit()    
    
    ##FIND CAR OWNER
    def FindCarOwner(self,make,model,year,color,plate):
        criteriaLst=[]
        if len(make)!=0:
            criteriaLst.append('make='+"'"+str(make)+"'" + ' COLLATE NOCASE ')
        if len(model)!=0:
            criteriaLst.append('model='+"'"+str(model)+"'"+ ' COLLATE NOCASE ')
        if len(year)!=0:
            criteriaLst.append('year='+"'"+str(year)+"'")
        if len(color)!=0:
            criteriaLst.append('color='+"'"+str(color)+"'"+ ' COLLATE NOCASE ')
        if len(plate)!=0:
            criteriaLst.append('plate='+"'"+str(plate)+"'")+ ' COLLATE NOCASE '
        criteriaStr = ' AND '.join(criteriaLst)
        
        self.cursor.execute('SELECT make, model, year, color, plate, MAX(regdate), expiry, fname, lname FROM registrations r, vehicles v WHERE r.vin=v.vin AND ' + criteriaStr + ' GROUP BY r.vin')
        result = self.cursor.fetchall()
        self.connection.commit()
        if result is None:
            return False
        else:
            return result
    

    def AbstractLife(self,fname,lname):
        self.cursor.execute('select count(ddate), sum(points) from demeritNotices where fname = :fname and lname = :lname',{'fname':fname,'lname':lname})
        return self.cursor.fetchall()
    
    def AbstractYear(self,fname,lname):
        self.cursor.execute('select count(ddate), sum(points) from demeritNotices where fname = :fname and lname = :lname and ddate > date("now", "-2 years")',{'fname':fname,'lname':lname})
        return self.cursor.fetchall()
        
    def TAbstract(self,fname,lname):
        self.cursor.execute('select count(t1.tno),count(t2.tno) from tickets t1, tickets t2 where t1.regno in (select regno from registrations where fname = :fname and lname = :lname) and t2.regno in (select regno from registrations where fname = :fname and lname = :lname) and t2.vdate > date("now", "-2 years")',{'fname':fname,'lname':lname})
        return self.cursor.fetchall()

    
    def TicketView(self,fname,lname):
        self.cursor.execute('select tno, vdate, violation, fine, t.regno, make, model from tickets t, registrations r, vehicles v where r.regno = t.regno and r.vin = v.vin and r.fname = :fname and r.lname = :lname order by vdate desc',{"fname":fname,"lname":lname})
        return self.cursor.fetchall()
    
    def MarriageReg(self,regno,regdate,regplace,fname1,lname1,fname2,lname2):
        self.cursor.execute('INSERT INTO marriages VALUES(:regno,:regdate,:regplace,:fname1,:lname1,:fname2,:lname2',{'regno':regno,'regdate':regdate,'regplace':regplace,'fname1':fname1,'lname1':lname1,'fname2':fname2,'lanem2':lname2})
        self.connection.commit()
    
    def CheckUniqueMarriageRegno(self,regno):
        self.cursor.execute('SELECT * FROM marriages WHERE regno=:regno',{"regno":regno})
        result = self.cursor.fetchone()
        if result is None:
            #if nothing found, the regno is unique and does not exist yet
            return False
        else:
            return True

    def CommitAndClose(self):
        self.connection.commit()	
        self.connection.close()
