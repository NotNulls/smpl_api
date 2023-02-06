import sqlite3

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

create_tabele = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_tabele)

create_tabele = "CREATE TABLE IF NOT EXISTS items ( name text, price real)"
cursor.execute(create_tabele)

connect.commit()
connect.close()



