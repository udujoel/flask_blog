import sqlite3
from datetime import datetime

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('First Post', 'Content for the first post', 'admin')
            )

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Second Post', 'Content for the second post', 'admin')
            )
cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Third Post', 'Content for the Third post', 'admin')
            )


# Users
cur.execute( "INSERT INTO users (username, name, email, password, member_since) VALUES (?,?,?,?,?)",
            ('admin', 'admin', 'admin@gmail.com', 'admin', datetime.now())
            )

connection.commit()
connection.close()
