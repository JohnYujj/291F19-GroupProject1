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
        self.connection.commit()
        if result is None:
            return False
        else:
            return True 
        
    def CreateTicket(self, tno, regno, fine, violation, vdate):
        self.cursor.execute('INSERT INTO tickets VALUES(:tno ,:regno ,:fine ,:violation ,:vdate)',{"tno":tno, "regno":regno, "fine":fine, "violation":violation, "vdate":vdate})
        self.connection.commit()    
    
    
    ##FIND CAR OWNER
    def FindCarOwner(self,make,model,year,color,plate):
        criteriaLst=[]
        if len(make)!=0:
            criteriaLst.append('make LIKE '+"'%"+str(make)+"%'")
        if len(model)!=0:
            criteriaLst.append('model LIKE '+"'%"+str(model)+"%'")
        if len(year)!=0:
            criteriaLst.append('year LIKE '+"'%"+str(year)+"%'")
        if len(color)!=0:
            criteriaLst.append('color LIKE '+"'%"+str(color)+"%'")
        if len(plate)!=0:
            criteriaLst.append('plate LIKE '+"'%"+str(plate)+"%'")
        criteriaStr = ' AND '.join(criteriaLst)
        
        self.cursor.execute('SELECT make, model, year, color, plate, MAX(regdate), expiry, fname, lname FROM registrations r, vehicles v WHERE r.vin=v.vin AND ' + criteriaStr + ' GROUP BY r.vin')
        result = self.cursor.fetchall()
        self.connection.commit()
        if result is None:
            return False
        else:
            return result
        
    
    def CommitAndClose(self):
        self.connection.commit()	
        self.connection.close()