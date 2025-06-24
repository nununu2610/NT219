from functools import wraps
from flask import request, g, jsonify
from crypto_utils.token_utils import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token thiếu"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Định dạng token sai (phải bắt đầu bằng 'Bearer ')"}), 401

        token = auth_header.split(" ")[1]  # Lấy phần token sau "Bearer"

        try:
            payload = decode_token(token)
            g.user = payload
        except Exception as e:
            return jsonify({"message": f"Token không hợp lệ: {str(e)}"}), 401
        return f(*args, **kwargs)
    return decorated


def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if g.user["role"] != role:
                return jsonify({"message": "Không đủ quyền truy cập"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
