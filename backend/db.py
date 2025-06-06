import sqlite3
from flask import g

DATABASE = 'mydb.sqlite'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, check_same_thread=False, timeout=10)
        g.db.row_factory = sqlite3.Row
    return g.db

    conn = sqlite3.connect('mydb.sqlite', check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# def init_db():
#     db = get_db()
#     try:
#         db.execute('''CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE,
#             password TEXT,
#             role TEXT
#         )''')
#         db.execute('''CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             description TEXT,
#             price REAL
#         )''')
#         db.execute('''CREATE TABLE IF NOT EXISTS logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             action TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES users(id)
#         )''')
#         db.execute('''CREATE TABLE IF NOT EXISTS carts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             product_id INTEGER,
#             quantity INTEGER DEFAULT 1,
#             FOREIGN KEY (user_id) REFERENCES users(id),
#             FOREIGN KEY (product_id) REFERENCES products(id)
#         )''')
#         db.commit()
#     finally:
#         db.close()


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )''')
    db.commit()
