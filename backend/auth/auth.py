from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required
import bcrypt, jwt, datetime
from db import get_db, log_action
from middleware import refresh_token_required
from refresh_token_utils import generate_refresh_token, save_refresh_token, revoke_refresh_token
from limiter import limiter

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = "supersecret"
REFRESH_SECRET_KEY = "refreshsecret"

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

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor = db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
        db.commit()
        user_id = cursor.lastrowid
        log_action(user_id, "Đăng ký")
        return jsonify({"message": "Đăng ký thành công"}), 201
    except Exception as e:
        return jsonify({"message": f"Lỗi server: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@limiter.limit("5 per minute")   # Moi IP chi ddc dang nhap 5lan/phut
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    if not username or not password:
        return jsonify({"message": "Vui lòng nhập username và password"}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user:
        if bcrypt.checkpw(password.encode(), user["password"].encode()):
            # Đăng nhập thành công
            access_token = jwt.encode({
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, SECRET_KEY, algorithm="HS256")
            access_token = access_token.decode() if isinstance(access_token, bytes) else access_token

            refresh_token = generate_refresh_token(user["id"])
            save_refresh_token(db, user["id"], refresh_token)

            log_action(user["id"], "Đăng nhập")
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            # Ghi log nếu sai mật khẩu
            log_action(user["id"], "Đăng nhập thất bại (sai mật khẩu)")
            return jsonify({"message": "Sai username hoặc password"}), 401
    else:
        # Không ghi log nếu username không tồn tại
        return jsonify({"message": "Sai username hoặc password"}), 401


@auth_bp.route('/auth/refresh', methods=['POST'])
@refresh_token_required
def refresh():
    db = get_db()

    old_token = request.get_json().get("refresh_token")
    revoke_refresh_token(db, old_token)

    new_refresh_token = generate_refresh_token(g.user["id"])
    save_refresh_token(db, g.user["id"], new_refresh_token)

    access_token = jwt.encode({
        "id": g.user["id"],
        "username": g.user["username"],
        "role": g.user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")
    access_token = access_token.decode() if isinstance(access_token, bytes) else access_token

    return jsonify({
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }), 200

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    print("Received logout data:", data)  # DEBUG dòng này

    if not data:
        return jsonify({"message": "Thiếu dữ liệu đầu vào"}), 400

    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Thiếu refresh token"}), 400

    refresh_token = data["refresh_token"]

    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token hết hạn"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Refresh token không hợp lệ"}), 401

    db = get_db()
    revoke_refresh_token(db, refresh_token)

    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        log_action(user["id"], "Đăng xuất")

    return jsonify({"message": "Đăng xuất thành công"}), 200

@auth_bp.route('/logs', methods=['GET'])
@jwt_required  # middleware kiểm tra token
def view_logs():
    if g.user["role"] != "admin":
        return jsonify({"message": "Không có quyền"}), 403

    db = get_db()
    logs = db.execute("SELECT * FROM logs ORDER BY timestamp DESC").fetchall()
    return jsonify([dict(row) for row in logs])

