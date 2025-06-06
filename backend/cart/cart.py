from flask import Blueprint, request, jsonify, g
from middleware import token_required
from db import get_db
from utils import encrypt, decrypt

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@token_required
def get_cart():
    db = get_db()
    user_id = g.user["id"]
    rows = db.execute("SELECT * FROM carts WHERE user_id=?", (user_id,)).fetchall()
    cart_items = []

    for row in rows:
        try:
            name = decrypt(row["product_name"])
            description = decrypt(row["product_description"]) if row["product_description"] else ""
        except Exception:
            name = row["product_name"]
            description = row["product_description"] if row["product_description"] else ""

        cart_items.append({
            "id": row["id"],
            "product_id": row["product_id"],
            "product_name": name,
            "product_description": description,
            "quantity": row["quantity"]
        })
    return jsonify(cart_items)

@cart_bp.route('', methods=['POST', 'OPTIONS'])
@token_required
def add_to_cart():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    db = get_db()
    user_id = g.user["id"]

    existing = db.execute("SELECT * FROM carts WHERE user_id=? AND product_id=?", (user_id, product_id)).fetchone()
    if existing:
        new_quantity = existing["quantity"] + quantity
        db.execute("UPDATE carts SET quantity=? WHERE id=?", (new_quantity, existing["id"]))
    else:
        db.execute("INSERT INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
    db.commit()
    return jsonify({"message": "Thêm vào giỏ hàng thành công"})

@cart_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def remove_from_cart(id):
    db = get_db()
    user_id = g.user["id"]

    cart_item = db.execute("SELECT * FROM carts WHERE id=? AND user_id=?", (id, user_id)).fetchone()
    if not cart_item:
        return jsonify({"error": "Không tìm thấy sản phẩm trong giỏ hàng"}), 404

    db.execute("DELETE FROM carts WHERE id=?", (id,))
    db.commit()
    return jsonify({"message": "Xóa khỏi giỏ hàng thành công"})
