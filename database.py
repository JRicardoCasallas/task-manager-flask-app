import sqlite3, os
DB_PATH='database.db'

def get_db():
    conn=sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn=get_db()
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        completed INTEGER,
        user_id INTEGER
    )''')
    conn.commit()
