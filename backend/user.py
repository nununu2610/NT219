from flask import Blueprint, jsonify, g
from middleware import token_required

user_bp = Blueprint('user', __name__)

# Lấy thông tin người dùng hiện tại
@user_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        user_info = {
            "id": g.user["id"],
            "username": g.user["username"],
            "role": g.user["role"]
        }
        return jsonify(user_info)
    except Exception as e:
        print("Lỗi khi lấy thông tin user:", e)
        return jsonify({"error": "Không thể lấy thông tin người dùng"}), 500
