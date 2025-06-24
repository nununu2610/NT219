from functools import wraps
from flask import request, jsonify, g
import jwt

SECRET_KEY = "supersecret"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Lấy token từ Header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Thiếu token"}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user = {
                "id": payload["id"],
                "username": payload["username"],
                "role": payload["role"]
            }
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token đã hết hạn"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token không hợp lệ"}), 401

        return f(*args, **kwargs)
    return decorated
