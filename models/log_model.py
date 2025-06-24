from flask import request, g
from models.db import get_db

def log_action(user_id, action):
    db = get_db()
    ip = request.remote_addr or 'unknown'
    user_agent = request.headers.get('User-Agent', 'unknown')

    db.execute('''
        INSERT INTO logs (user_id, action, ip_address, user_agent)
        VALUES (?, ?, ?, ?)
    ''', (user_id, action, ip, user_agent))
    db.commit()

def get_logs_by_user_id(user_id):
    db = get_db()
    cursor = db.execute('''
        SELECT timestamp, action, ip_address, user_agent
        FROM logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))
    return cursor.fetchall()
