import sqlite3
from datetime import datetime

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Posts
cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('First Post', 'Content for the first post', 'admin')
            )

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Second Post', 'Content for the second post', 'admin')
            )

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Third Post', 'Content for the Third post', 'admin')
            )

cur.execute( "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
            ('Fourth Post', 'Content for the Fourth post', 'user')
            )

# Users
cur.execute( "INSERT INTO users (username, name, email, password, member_since) VALUES (?,?,?,?,?)",
            ('admin', 'admin', 'admin@gmail.com', 'admin', datetime.now())
            )

cur.execute( "INSERT INTO users (username, name, email, password, member_since) VALUES (?,?,?,?,?)",
            ('user', 'user', 'user@gmail.com', 'user', datetime.now())
            )

# Comments
cur.execute( "INSERT INTO comments (post_id, author, content) VALUES (?,?,?)",
            (1, 'admin', 'This is a sample comment')
            )

cur.execute( "INSERT INTO comments (post_id, author, content) VALUES (?,?,?)",
            (2, 'user', 'This is a sample comment')
            )

connection.commit()
connection.close()

