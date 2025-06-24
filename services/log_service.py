# services/log_service.py
from flask import Blueprint, jsonify
from middleware.auth_check import token_required
from models.log_model import get_logs_by_user_id

log_bp = Blueprint("log", __name__, url_prefix="/logs")

@log_bp.route("/", methods=["GET"])
@token_required
def get_logs(current_user):
    logs = get_logs_by_user_id(current_user["id"])
    return jsonify(logs), 200
