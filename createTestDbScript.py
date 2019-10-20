import sqlite3
import time
import hashlib

#script creating testdb
createTableQuery=   '''
                    CREATE TABLE users (
                                uid TEXT,
                                pwd TEXT,
                                utype TEXT,
                                fname TEXT,
                                lname TEXT,
                                city TEXT,
                                PRIMARY KEY (uid)
                                );
                '''

insert_courses = '''
                    INSERT INTO users(uid, pwd, utype, fname, lname, city) VALUES
                        ('1username', '1password', 'Registry Agent', 'Black', 'White', 'Agent1Town'),
                        ('2username', '2password', 'Registry Agent', 'White', 'Black', 'Agent2Town'),
                        ('3username', '3password', 'Traffic Officer', 'Traffico', 'Oficero', 'TrafficTown');
                 '''




connection = sqlite3.connect("./test.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute(createTableQuery)
connection.commit()
cursor.execute(insert_courses)
connection.commit()    
connection.close()