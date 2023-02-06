import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text)'
cursor.execute(create_table)

user = (1, 'jose', 'asdf')

inser_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(inser_query,user)

users = [
    (2,'ralf', 'asdf'),
    (3,'anne', 'asdf')
]

select_query = "SELECT * FROM users"
cursor.executemany(inser_query, users)

for row in cursor.execute(select_query):
    print (row)

connection.commit()
connection.close()
