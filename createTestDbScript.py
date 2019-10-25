import sqlite3
import time
import hashlib

#script creating testdb
createTableQuery=   '''
                    CREATE TABLE users (
                                uid 		TEXT,
                                pwd 		TEXT,
                                utype 		TEXT,
                                fname 		TEXT,
                                lname 		TEXT,
                                city 		TEXT,
                                PRIMARY KEY (uid)
                                );
                    
                    CREATE TABLE persons (
                                fname		char(12),
                                lname		char(12),
                                bdate		date,
                                bplace		char(20), 
                                address		char(30),
                                phone		char(12),
                                primary key (fname, lname)
                                );
                                
                    CREATE TABLE births (
                                regno 		int,
                                fname		char(12),
                                lname		char(12),
                                regdate		date,
                                regplace	char(20),
                                gender		char(1),
                                f_fname		char(12),
                                f_lname		char(12),
                                m_fname		char(12),
                                m_lname		char(12),
                                primary key (regno),
                                foreign key (fname,lname) references persons,
                                foreign key (f_fname,f_lname) references persons,
                                foreign key (m_fname,m_lname) references persons
                                );

                    CREATE TABLE marriages (
                                regno		int,
                                regdate		date,
                                regplace	char(20),
                                p1_fname	char(12),
                                p1_lname	char(12),
                                p2_fname	char(12),
                                p2_lname	char(12),
                                primary key (regno),
                                foreign key (p1_fname,p1_lname) references persons,
                                foreign key (p2_fname,p2_lname) references persons
                                );
                  
                  CREATE TABLE vehicles (
                                vin		char(5),
                                make		char(10),
                                model		char(10),
                                year		int,
                                color		char(10),
                                primary key (vin)
                                );
                  
                  
                  CREATE TABLE registrations (
                                regno		int,
                                regdate		date,
                                expiry		date,
                                plate		char(7),
                                vin		char(5), 
                                fname		char(12),
                                lname		char(12),
                                primary key (regno),
                                foreign key (vin) references vehicles,
                                foreign key (fname,lname) references persons
                                );
                  
                  CREATE TABLE tickets (
                                tno		int,
                                regno		int,
                                fine		int,
                                violation	text,
                                vdate		date,
                                primary key (tno),
                                foreign key (regno) references registrations
                                );
                  
                  CREATE TABLE demeritNotices (
                                ddate		date, 
                                fname		char(12), 
                                lname		char(12), 
                                points		int, 
                                desc		text,
                                primary key (ddate,fname,lname),
                                foreign key (fname,lname) references persons
                                );
                  
                  CREATE TABLE payments (
                                tno		int,
                                pdate		date,
                                amount		int,                                
                                primary key (tno, pdate),
                                foreign key (tno) references tickets
                                );                           
                '''

insert_data = '''
                    INSERT INTO users(uid, pwd, utype, fname, lname, city) VALUES
                        ('1username', '1password', 'a', 'Black', 'White', 'Agent1Town'),
                        ('2username', '2password', 'a', 'White', 'Black', 'Agent2Town'),
                        ('3username', '3password', 'o', 'Traffico', 'Oficero', 'TrafficTown'),
                        ('4username', '4password', 'o', 'Oficero', 'Traffico', 'TrafficTown')
                        ;
                        
                    INSERT INTO persons VALUES
                        ('Trayvon','Fox','1892-07-17','PeaceRiver,AB','133 Street PR','443-449-9999'),
                        ('Lillian', 'Bounds', '1899-02-15', 'Spalding, Idaho', 'Los Angeles, US', '213-555-5556'),
                        ('Adam','Rafiei',"1900-01-02","Shiraz,Iran","Tehran,Iran","916-331-3311"),
                        ('James','Smith','1900-08-08','Calgary,AB','43,43Ave','720-000-0001'),
                        ('Walt', 'Disney', '1901-12-05', 'Chicago, US', 'Los Angeles, US', '213-555-5555'),
                        ('Mary','Brown','1905-11-15','Nordegg,AB','22,67Ave','776-655-9955'),
                        ('John', 'Truyens', '1907-05-15', 'Flanders, Belgium', 'Beverly Hills, Los Angeles, US', '213-555-5558'),
                        ('Linda','Smith','1908-02-26','Ohaton,AB','43,43Ave','680-099-9943'),
                        ('Minnie', 'Mouse', '1928-01-05', 'Disneyland', 'Anaheim, US', '714-555-5552'),
                        ('Mickey', 'Mouse', '1928-01-05', 'Disneyland', 'Anaheim, US', '714-555-5551'),
                        ("Mary","Smith","1950-11-08","Calgary,AB","11Ave,1st","604-555-2244"),
                        ("Aunt","Smith","1951-12-08","Calgary,AB","11Ave,1st","888-555-2244"),
                        ("Dave","Fox","1950-03-29","Calgary,AB","11Ave,1st","664-110-8763"),
                        ("Uncle","Fox","1951-03-29","Calgary,AB","11Ave,1st","780-110-8743"),
                        ('Michael','Fox','1981-06-09','Edmonton, AB','Manhattan, New York, US', '212-111-1111'),
                        ('Cousin1','Fox','1981-06-09','Edmonton, AB','Manhattan, New York, US', '666-111-1111'),
                        ('Cousin2','Fox','1991-02-06','Edmonton, AB','Manhattan, New York, US', '666-111-1111'),
                        ("Megan","Fox","1982-06-09","Calgary,AB","12Ave,101st","780-460-1134"),
                        ("Fatima","Fox","1992-06-09","Calgary,AB","12Ave,101st","444-470-7734"),
                        ("Lisa","Bounds","1999-04-10","Spalding,Idaho","Moscow,101st","604-420-1234"),
                        ('Diane','Wong','1973-04-04','England','London,Hackney','766-664-6678'),
                        ('Davood','Rafiei',date('now','-21 years'),'Iran','100 Lovely Street,Edmonton,AB', '780-111-2222'),
                        ('Linda','Fox','1991-02-04','England','London','344-447-7755'),
                        ('Tammy','Fox','1991-02-04','England','Manchester','344-111-2345'),
                        ('Henry','Wong','1993-04-04','Canada','Alert','566-664-6678'),
                        ('Michael','Parenti','1991-02-04','England','London','344-447-7755'),
                        ('Diane','Lee','1973-04-04','England','London,Hackney','434-596-234')
                        ;
                        
                    INSERT INTO births VALUES
                        (1,'Mary','Smith','1920-04-04','Ohaton,AB','F','James','Smith','Linda','Smith'),
                        (2,'Aunt','Smith','1922-06-04','Ohaton,AB','F','James','Smith','Linda','Smith'),
                        (3,'Dave','Fox','1922-03-06','Calgary,AB','M','Trayvon','Fox','Mary','Brown'),
                        (5,'Uncle','Fox','1925-11-06','Calgary,AB','M','Trayvon','Fox','Mary','Brown'),
                        (6,'Cousin1', 'Fox', '1982-06-10', 'Edmonton,AB', 'F', 'Walt', 'Disney', 'Aunt', 'Smith'),
                        (7,'Cousin2', 'Fox', '1991-02-06', 'Edmonton,AB', 'F', 'Uncle', 'Fox', 'Lillian', 'Bounds'),
                        (100,'Mickey', 'Mouse', '1928-02-05', 'Anaheim, US', 'M', 'Walt', 'Disney', 'Lillian', 'Bounds'),
                        (200,'Minnie', 'Mouse', '1928-02-04', 'Anaheim, US', 'M', 'Walt', 'Disney', 'Lillian', 'Bounds'),
                        (300,'Michael', 'Fox', '1981-06-10', 'Edmonton,AB', 'M', 'Dave', 'Fox', 'Mary', 'Smith'),
                        (310,'Megan', 'Fox', '1982-06-10', 'Edmonton,AB', 'F', 'Dave', 'Fox', 'Mary', 'Smith'),
                        (320,'Fatima', 'Fox', '1992-06-10', 'Edmonton,AB', 'F', 'Dave', 'Fox', 'Lillian', 'Bounds'),
                        (330,'Adam', 'Rafiei', '1960-02-10', 'Iran', 'M', 'Walt', 'Disney', 'Mary', 'Brown'),
                        (400,'Lisa', 'Bounds', '1999-04-16', 'Spalding,Idaho', 'F', 'John', 'Truyens', 'Lillian', 'Bounds'),
                        (600,'Davood', 'Rafiei', date('now','-21 years'), 'Iran', 'M', 'Adam', 'Rafiei', 'Mary', 'Smith'),
                        (700,'Linda','Fox','1991-02-06','England','F',"Michael","Fox","Lisa","Bounds"),
                        (750,'Tammy','Fox','1991-02-04','England','F',"Michael","Fox","Lisa","Bounds"),
                        (775,'Henry','Wong','1993-04-05','Canada','M',"Michael","Fox","Diane","Wong")
                        ;
                    
                    INSERT INTO marriages VALUES                 
                        (200, '1925-07-13', 'Idaho, US', 'Walt', 'Disney', 'Lillian', 'Bounds'),
                        (201, '1969-05-03', 'Los Angeles, US', 'Lillian', 'Bounds', 'John', 'Truyens'),
                        (300, '1990-04-13', 'Idaho, US', 'Michael', 'Fox', 'Lisa', 'Bounds'),
                        (301, '1992-09-12', 'Idaho, US', 'Diane', 'Wong','Michael', 'Fox'),
                        (305, '1945-09-11', 'Idaho, US', 'Mickey', 'Mouse', 'Lisa', 'Bounds')
                        ;
                        
                    INSERT INTO vehicles VALUES
                        (200, 'Chevrolet', 'Camaro', 1969, 'red'),
                        (100, 'Doge', 'Challenger', 1969, 'red'),
                        (101, 'Doge', 'Challenger', 1969, 'red'),
                        (300, 'Mercedes', 'SL 230', 1969, 'black'),
                        (400, 'Mercedes', 'Benz', 1980, 'white'),
                        (500, 'Ferrari', 'F1', 1999, 'red'),
                        (600, 'Toyota', 'Camry', 2005, 'black'),
                        (700, 'Nissan', 'Altima', 2005, 'black'),
                        (801, 'Honda', 'Accord', 2005, 'white'),
                        (800, 'Maza', '3', 2005, 'white'),
                        (900, 'Nissan', 'Altima', 2010, 'red'),
                        (1000, 'Nissan', 'Altima', 2010, 'blue'),
                        (1001, 'Toyota', 'Camry', 2010, 'green')
                        ;
                        
                    INSERT INTO registrations VALUES
                        (300, '1964-05-06','1965-05-06', 'Plate1',100, 'Walt', 'Disney'),
                        (302, '2019-01-06','2020-01-06', 'Plate2',100, 'Lillian', 'Bounds'),
                        (801, '2019-01-06','2020-08-25', 'Plate3',101, 'Michael', 'Fox'),
                        (802, '2018-12-08','2019-12-08', 'Plate4',300, "Diane","Wong"),
                        (803, '2018-01-08','2020-01-08', 'Plate5',200, "Diane","Wong"),
                        (804, '2018-12-25','2019-12-25', 'Plate6',500, "Diane","Wong"),
                        (805, '2018-12-16','2020-12-16', 'Plate7',600, 'John', 'Truyens'),
                        (901, '2018-11-16','2019-11-16', 'Plate9',801, 'John', 'Truyens'),
                        (902, '2016-10-11','2017-10-11', 'PlateA',800, 'Lisa', 'Bounds'),
                        (806, '1999-01-11','2001-01-11', 'Plate8',900, 'John', 'Truyens'),
                        (903, '2016-02-29','2018-02-28', 'PlateB', 1000, 'Lisa', 'Bounds'),
                        (905, '2017-06-26','2019-06-26', 'PlateC', 1001, 'Davood', 'Rafiei'),
                        (1001, '2019-01-16','2021-01-16', 'PlateD',200, 'John', 'Truyens'),
                        (1002, '2018-11-11','2020-11-11', 'PlateE',100, 'Lisa', 'Bounds'),
                        (1003, '2018-01-11','2019-09-30', 'PlateF',101, 'John', 'Truyens'),
                        (1004, '2019-02-29','2020-02-28', 'PlateG', 700, 'Lisa', 'Bounds'),
                        (1005, '2019-06-26','2020-06-26', 'PlateH', 1000, 'Davood', 'Rafiei')
                        ;
                        
                    INSERT INTO tickets VALUES
                        (100,300,40,'red ligHt violation','1964-08-20'),
                        (101,805,40,'Red light violaTion','2018-12-20'),
                        (107,905,40,'red violatioN','2019-01-20'),
                        (109,902,150,'yellow light violation','2018-01-21'),
                        (108,803,150,'Stunting','2019-02-29'),
                        (102,901,220,'DUI','2019-02-18'),
                        (103,806,70,'illegal parking','2016-08-30'),
                        (104,805,40,'speeding','2019-02-29'),
                        (105,905,10,'yellow light violation','2019-02-28'),
                        (106,905,220,'red violation','2018-12-30'),
                        (111,805,220,'DUI','2019-06-12'),
                        (112,801,220,'red light violation','2019-06-30'),
                        (113,801,221,'grand theft auto','2020-12-30'),
                        (114,801,222,'grand theft auto','2020-12-30'),
                        (115,801,222,'grand theft auto','2020-12-30')
                        ;
                        
                    INSERT INTO demeritNotices VALUES
                        ('1991-03-29', 'Lisa', 'Bounds', 10, 'DUI'),
                        ('2018-07-20', 'Michael', 'Fox', 4, 'Speeding'),
                        ('1993-04-25', 'Diane', 'Wong', 2, 'Speeding'),
                        ('2018-03-20', 'Michael', 'Fox', 12, 'DWI'),
                        ('2019-10-31', 'Diane', 'Wong', 2, 'Speeding'),
                        ('1964-08-20', 'Walt', 'Disney', 4, 'Speeding'),
                        ('1991-03-30', 'Lisa', 'Bounds', 4, 'Speeding'),
                        ('2019-09-28', 'Mickey', 'Mouse', 12, 'DUI'),
                        ('2018-08-20', 'Walt', 'Disney', 20, 'Vehicular Manslaughter'),
                        ('1994-03-30', 'Lisa', 'Bounds', 4, 'Speeding'),
                        ('2019-03-22', 'Mickey', 'Mouse', 12, 'DUI')
                        ;
                        
                    INSERT INTO payments VALUES
                        (103,'2016-09-13',70),
                        (108, '2019-03-07',150),
                        (111,'2019-07-03',220),
                        (114,'2021-03-23',200),
                        (115,'2021-03-23',70),
                        (115,'2021-04-07',80)
                        ;
                        
                 '''


connection = sqlite3.connect("./test.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS persons;")
cursor.execute("DROP TABLE IF EXISTS births;")
cursor.execute("DROP TABLE IF EXISTS marriages;")
cursor.execute("DROP TABLE IF EXISTS vehicles;")
cursor.execute("DROP TABLE IF EXISTS registrations;")
cursor.execute("DROP TABLE IF EXISTS tickets;")
cursor.execute("DROP TABLE IF EXISTS demeritNotices;")
cursor.execute("DROP TABLE IF EXISTS payments;")
cursor.executescript(createTableQuery)
connection.commit()

cursor.executescript(insert_data)
connection.commit()   

connection.close()