from functools import wraps
from flask import request, jsonify, g
import jwt
from db import get_db
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")

def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if g.user["role"] != role:
                return jsonify({"message": "Bạn không có quyền truy cập"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if request.method == 'OPTIONS':
            return '', 200

        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Bearer <token>

        if not token:
            return jsonify({'message': 'Token không được cung cấp'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            db = get_db()
            user = db.execute("SELECT * FROM users WHERE id = ?", (data['id'],)).fetchone()
            if not user:
                return jsonify({'message': 'User không tồn tại'}), 401
            # ✅ Thêm dòng này để g.user hoạt động
            g.user = {"id": user["id"], "username": user["username"], "role": user["role"]}
        except Exception as e:
            return jsonify({'message': 'Token không hợp lệ'}), 401

        return f(*args, **kwargs)
    return decorated
