import sqlite3
import os

def init_sqlite_db():
    """Initialize SQLite database for local development."""
    conn = sqlite3.connect('database.db')
    
    with open('schema.sql') as f:
        conn.executescript(f.read())
    
    # Insert admin user
    conn.execute('INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)',
                ('admin', 'Admin User', 'admin@example.com', 'admin123'))
    
    # Insert sample posts
    conn.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                ('Welcome to TheCyberForum', 'This is your first post!', 'Admin User'))
    
    conn.commit()
    conn.close()
    print("SQLite database initialized successfully!")

def init_postgres_db():
    """Initialize PostgreSQL database for production."""
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("DATABASE_URL not found in environment variables")
        return
    
    conn = psycopg2.connect(database_url)
    conn.cursor_factory = RealDictCursor
    cur = conn.cursor()
    
    # Read and execute schema
    with open('schema.sql') as f:
        schema = f.read()
        # Convert SQLite syntax to PostgreSQL
        schema = schema.replace('AUTOINCREMENT', 'SERIAL')
        schema = schema.replace('datetime', 'timestamp')
        
        # Execute each statement separately
        statements = schema.split(';')
        for statement in statements:
            if statement.strip():
                cur.execute(statement)
    
    # Insert admin user
    cur.execute('INSERT INTO users (username, name, email, password) VALUES (%s, %s, %s, %s)',
                ('admin', 'Admin User', 'admin@example.com', 'admin123'))
    
    # Insert sample posts
    cur.execute('INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)',
                ('Welcome to TheCyberForum', 'This is your first post!', 'Admin User'))
    
    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL database initialized successfully!")

if __name__ == '__main__':
    # Check if we're on Render (PostgreSQL) or local (SQLite)
    if os.environ.get('DATABASE_URL'):
        init_postgres_db()
    else:
        init_sqlite_db()

