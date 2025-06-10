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
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        return jsonify({"message": "Username đã tồn tại"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, hashed, role))
        db.commit()

        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cur.fetchone()[0]
        cur.close()

        log_action(user_id, "Đăng ký")
        return jsonify({"message": "Đăng ký thành công"}), 201
    except Exception as e:
        cur.close()
        return jsonify({"message": f"Lỗi server: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    if not username or not password:
        return jsonify({"message": "Vui lòng nhập username và password"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user:
        user_id, db_username, db_password, db_role = user
        if bcrypt.checkpw(password.encode(), db_password.encode()):
            access_token = jwt.encode({
                "id": user_id,
                "username": db_username,
                "role": db_role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, SECRET_KEY, algorithm="HS256")

            access_token = access_token.decode() if isinstance(access_token, bytes) else access_token
            refresh_token = generate_refresh_token(user_id)
            save_refresh_token(db, user_id, refresh_token)

            log_action(user_id, "Đăng nhập")
            cur.close()
            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        else:
            log_action(user_id, "Đăng nhập thất bại (sai mật khẩu)")
            cur.close()
            return jsonify({"message": "Sai username hoặc password"}), 401
    else:
        cur.close()
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
    if not data:
        return jsonify({"message": "Thiếu dữ liệu đầu vào"}), 400

    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "Thiếu refresh token"}), 400

    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token hết hạn"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Refresh token không hợp lệ"}), 401

    db = get_db()
    revoke_refresh_token(db, refresh_token)

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        log_action(user[0], "Đăng xuất")

    return jsonify({"message": "Đăng xuất thành công"}), 200


@auth_bp.route('/logs', methods=['GET'])
@jwt_required
def view_logs():
    if g.user["role"] != "admin":
        return jsonify({"message": "Không có quyền"}), 403

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    logs = cur.fetchall()
    cur.close()

    return jsonify([{
        "id": row[0],
        "user_id": row[1],
        "action": row[2],
        "ip_address": row[3],
        "user_agent": row[4],
        "timestamp": row[5].isoformat() if row[5] else None
    } for row in logs])
