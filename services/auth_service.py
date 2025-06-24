from flask import Blueprint, request, jsonify, g
import bcrypt, jwt, datetime
from models.db import get_db
from models.log_model import log_action
from middleware.refresh_token_utils import generate_refresh_token, save_refresh_token, revoke_refresh_token
from crypto_utils.bcrypt_utils import hash_password, verify_password
from crypto_utils.token_utils import generate_access_token, decode_token

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "supersecret"
REFRESH_SECRET_KEY = "refreshsecret"

# -------------------- Đăng ký --------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    db = get_db()
    if db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone():
        return jsonify({"message": "Username đã tồn tại"}), 400

    hashed = hash_password(password)
    cursor = db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
    db.commit()
    log_action(cursor.lastrowid, "Đăng ký")

    return jsonify({"message": "Đăng ký thành công"}), 201

# -------------------- Đăng nhập --------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if not user:
        print("Không tìm thấy user:", username)
        return jsonify({"message": "Sai thông tin đăng nhập"}), 401

    print("So sánh mật khẩu với:", user["password"])

    if not verify_password(password, user["password"]):
        log_action(user["id"], "Đăng nhập thất bại")
        print("Mật khẩu không khớp")
        return jsonify({"message": "Sai thông tin đăng nhập"}), 401

    print("Đăng nhập thành công")

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user["id"])
    save_refresh_token(db, user["id"], refresh_token)
    log_action(user["id"], "Đăng nhập")

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

# -------------------- Đăng xuất --------------------
@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "Thiếu refresh token"}), 400

    db = get_db()
    revoked = revoke_refresh_token(db, refresh_token)
    if revoked:
        return jsonify({"message": "Đăng xuất thành công"})
    return jsonify({"message": "Refresh token không hợp lệ"}), 400
