import os
import psycopg2
import sqlite3
from flask import g
from urllib.parse import urlparse

def get_db():
    """
    Trả về connection tới PostgreSQL nếu có DATABASE_URL,
    ngược lại dùng SQLite (cho chạy cục bộ).
    """
    if 'db' not in g:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            print("👉 Kết nối đến: PostgreSQL")  # ✅ Dòng xác nhận
            conn = psycopg2.connect(db_url)
            conn.autocommit = True
        else:
            print("👉 Kết nối đến: SQLite")  # ✅ Dòng xác nhận
            sqlite_path = os.path.join(os.getcwd(), 'mydb.sqlite3')
            conn = sqlite3.connect(sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES)
            conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Tạo bảng nếu chưa tồn tại.
    - Dùng SQL chuẩn tương thích Postgres và SQLite.
    """
    db = get_db()
    cur = db.cursor()
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price NUMERIC NOT NULL
    );

    CREATE TABLE IF NOT EXISTS cart (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        quantity INTEGER DEFAULT 1 NOT NULL
    );

    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        action TEXT NOT NULL,
        ip_address TEXT,
        user_agent TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS refresh_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        token TEXT NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        revoked BOOLEAN DEFAULT FALSE
    );
    """
    cur.execute(ddl)
    if hasattr(db, 'commit'):
        db.commit()
