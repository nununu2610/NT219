from flask import Blueprint, jsonify, g
from middleware.auth_check import token_required
from models.db import get_db

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    return jsonify({
        "id": g.user["id"],
        "username": g.user["username"],
        "role": g.user["role"]
    })