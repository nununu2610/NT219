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
    cur = db.cursor()
    cur.execute("SELECT id, action, timestamp FROM logs WHERE user_id = %s ORDER BY timestamp DESC", (user["id"],))
    rows = cur.fetchall()
    cur.close()

    logs = [{
        "id": row[0],
        "action": row[1],
        "timestamp": row[2].isoformat() if row[2] else None
    } for row in rows]

    return jsonify(logs)
