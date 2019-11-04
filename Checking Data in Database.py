import sqlite3


database = './test.db'
conn = sqlite3.connect('./test.db')
c = conn.cursor()

c.execute('SELECT * FROM births')
data = c.fetchall()
conn.commit()
for i in data:
    print(i)