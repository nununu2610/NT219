import psycopg2
from flask import g, request
import os
from datetime import datetime

# Kết nối tới PostgreSQL thông qua biến môi trường
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cur = db.cursor()

    # Bảng users
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )''')

    # Bảng refresh_tokens
    cur.execute('''CREATE TABLE IF NOT EXISTS refresh_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        token TEXT NOT NULL UNIQUE,
        expires_at TIMESTAMP NOT NULL,
        revoked BOOLEAN NOT NULL DEFAULT FALSE
    )''')

    # Bảng products
    cur.execute('''CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL
    )''')

    # Bảng logs
    cur.execute('''CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        action TEXT,
        ip_address TEXT,
        user_agent TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Bảng carts
    cur.execute('''CREATE TABLE IF NOT EXISTS carts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER DEFAULT 1
    )''')

    db.commit()
    cur.close()

def log_action(user_id, action):
    db = get_db()
    cur = db.cursor()

    ip = request.remote_addr or 'unknown'
    user_agent = request.headers.get('User-Agent', 'unknown')

    cur.execute(
        '''INSERT INTO logs (user_id, action, ip_address, user_agent)
           VALUES (%s, %s, %s, %s)''',
        (user_id, action, ip, user_agent)
    )
    db.commit()
    cur.close()
