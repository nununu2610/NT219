from functools import wraps
from flask import request, jsonify, g
import jwt
from db import get_db

SECRET_KEY = "supersecret"
REFRESH_SECRET_KEY = "refreshsecret"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return '', 200
        
        token = None
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            return jsonify({'message': 'Token không được cung cấp'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE id = ?", (data['id'],)).fetchone()
            if not user:
                return jsonify({'message': 'User không tồn tại'}), 401
            g.user = {"id": user["id"], "username": user["username"], "role": user["role"]}
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token hết hạn'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ'}), 401

        return f(*args, **kwargs)
    return decorated

def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(g, 'user') or g.user.get("role") != role:
                return jsonify({"message": "Bạn không có quyền truy cập"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


def refresh_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return jsonify({'message': 'Refresh token không được cung cấp'}), 401
        
        try:
            decoded = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Refresh token hết hạn'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Refresh token không hợp lệ'}), 401

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (decoded['id'],)).fetchone()
        if not user or user['refresh_token'] != refresh_token:
            return jsonify({'message': 'Refresh token không hợp lệ'}), 401
        
        g.user = {"id": user["id"], "username": user["username"], "role": user["role"]}
        
        return f(*args, **kwargs)
    return decorated

def log_action(user_id, action):
    db = get_db()
    db.execute(
        "INSERT INTO logs (user_id, action) VALUES (?,?)",
        (user_id, action)
    )
    db.commit()
