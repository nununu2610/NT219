from flask import Blueprint, jsonify, g
from middleware import token_required
from db import get_db

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET'])
@token_required
def get_me():
    user = g.user
    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "role": user["role"]
    })

@user_bp.route('/logs', methods=['GET'])
@token_required
def get_logs():
    user = g.user
    db = get_db()
    rows = db.execute("SELECT * FROM logs WHERE user_id=?", (user["id"],)).fetchall()
    logs = []
    for row in rows:
        logs.append({
            "id": row["id"],
            "action": row["action"],
            "timestamp": row["timestamp"]
        })
    return jsonify(logs)
