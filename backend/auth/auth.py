from flask import Blueprint, request, jsonify, g
import bcrypt, jwt, datetime
from db import get_db
from middleware import refresh_token_required  # import middleware
from flask import request


auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "supersecret"
REFRESH_SECRET_KEY ="refreshsecret"

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
        access_token = jwt.encode({
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")

        refresh_token = jwt.encode({
            "id": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
        }, REFRESH_SECRET_KEY, algorithm="HS256")

        if isinstance(access_token, bytes):
            access_token = access_token.decode()
        if isinstance(refresh_token, bytes):
            refresh_token = refresh_token.decode()

        # Lưu refresh_token vào DB
        db.execute("UPDATE users SET refresh_token = ? WHERE id = ?", (refresh_token, user["id"]))
        db.commit()

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    else:
        return jsonify({"message": "Sai username hoặc password"}), 401


@auth_bp.route('/auth/refresh', methods=['POST'])
@refresh_token_required
def refresh():
    # g.user đã được middleware set sẵn
    access_token = jwt.encode({
        "id": g.user["id"],
        "username": g.user["username"],
        "role": g.user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

    if isinstance(access_token, bytes):
        access_token = access_token.decode()

    return jsonify({"access_token": access_token})

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return '', 200

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Thiếu Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
        if not user_id:
            return jsonify({"message": "Token không hợp lệ"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token đã hết hạn"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token không hợp lệ"}), 401

    db = get_db()
    # Kiểm tra refresh token có trong DB không
    user = db.execute("SELECT * FROM users WHERE id = ? AND refresh_token = ?", (user_id, token)).fetchone()
    if not user:
        return jsonify({"message": "Token không hợp lệ hoặc đã đăng xuất trước đó"}), 401

    # Nếu hợp lệ thì xóa refresh token khỏi DB
    db.execute("UPDATE users SET refresh_token = NULL WHERE id = ?", (user_id,))
    db.commit()

    return jsonify({"message": "Đăng xuất thành công"}), 200

