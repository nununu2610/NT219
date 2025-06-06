from flask import Blueprint, request, jsonify
import bcrypt, jwt, datetime
from db import get_db

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "supersecret"

@auth_bp.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    username, password, role = data.get("username"), data.get("password"), data.get("role")

    if not username or not password or not role:
        return jsonify({"message": "Vui lòng nhập đầy đủ thông tin"}), 400

    db = get_db()
    existing_user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if existing_user:
        return jsonify({"message": "Username đã tồn tại"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_str = hashed.decode()

    try:
        db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_str, role))
        db.commit()
        return jsonify({"message": "Đăng ký thành công"}), 201
    except Exception:
        return jsonify({"message": "Lỗi server"}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    if not username or not password:
        return jsonify({"message": "Vui lòng nhập username và password"}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        token = jwt.encode({
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({"token": token})

    return jsonify({"message": "Sai thông tin đăng nhập"}), 401
