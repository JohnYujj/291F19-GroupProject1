import sqlite3

class SQLController:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        
    #def check_if_userExists returns bool depending if select from users uid=uid found or not
    #def check_if_uid-pw_match returns bool depending if select user uid/pwd match found or not
    
    def GetUserType(self, username,password):
        self.cursor.execute('SELECT utype FROM users WHERE uid=:username AND pwd=:password',{"username":username,"password":password})
        user = self.cursor.fetchone()
        uType=user[0]
        self.connection.commit()
        return uType     
    
    def CommitAndClose(self):
        self.connection.commit()	
        self.connection.close()