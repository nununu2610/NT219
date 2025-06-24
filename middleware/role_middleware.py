from functools import wraps
from flask import jsonify, g

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user" not in g:
                return jsonify({"message": "Chưa xác thực"}), 401
            if g.user["role"] not in roles:
                return jsonify({"message": "Không có quyền"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
