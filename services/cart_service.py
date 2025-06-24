# services/cart_service.py
from flask import Blueprint, request, jsonify
from middleware.auth_check import token_required
from models.db import get_db
import uuid

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route("/add", methods=["POST"])
@token_required
def add_to_cart(current_user):
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"message": "Missing product_id"}), 400

    db = get_db()
    db.execute(
        "INSERT INTO cart (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)",
        (str(uuid.uuid4()), current_user["id"], product_id, quantity)
    )
    db.commit()
    return jsonify({"message": "Product added to cart."}), 200

@cart_bp.route("/items", methods=["GET"])
@token_required
def view_cart(current_user):
    db = get_db()
    items = db.execute(
        "SELECT product_id, quantity FROM cart WHERE user_id = ?",
        (current_user["id"],)
    ).fetchall()
    return jsonify([dict(row) for row in items])

@cart_bp.route("/remove", methods=["POST"])
@token_required
def remove_from_cart(current_user):
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"message": "Missing product_id"}), 400

    db = get_db()
    db.execute(
        "DELETE FROM cart WHERE user_id = ? AND product_id = ?",
        (current_user["id"], product_id)
    )
    db.commit()
    return jsonify({"message": "Product removed from cart."})