import sqlite3
from flask import g
import os

DATABASE = 'mydb.sqlite'

def get_db():
     if 'db' not in g:
        full_path = os.path.abspath(DATABASE)
        print(f"📂 Kết nối SQLite tại: {full_path}")
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
     return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    print("👉 Đang chạy init_db để tạo bảng từ schema.sql")
    db = get_db()
    with open('schema.sql', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()


