from flask import Blueprint, request, jsonify, g
from middleware import token_required
from db import get_db, log_action
from utils import encrypt, decrypt
from limiter import limiter

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@token_required
def get_cart():
    db = get_db()
    user_id = g.user["id"]
    cur = db.cursor()
    cur.execute("""
        SELECT carts.id, carts.product_id, carts.quantity,
               products.name AS product_name,
               products.description AS product_description
        FROM carts
        JOIN products ON carts.product_id = products.id
        WHERE carts.user_id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()

    cart_items = []
    for row in rows:
        try:
            name = decrypt(row[3])
            description = decrypt(row[4]) if row[4] else ""
        except Exception:
            name = row[3]
            description = row[4] if row[4] else ""

        cart_items.append({
            "id": row[0],
            "product_id": row[1],
            "product_name": name,
            "product_description": description,
            "quantity": row[2]
        })

    return jsonify(cart_items)


@cart_bp.route('', methods=['POST', 'OPTIONS'])
@token_required
@limiter.limit("20 per minute")
def add_to_cart():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    db = get_db()
    cur = db.cursor()
    user_id = g.user["id"]

    cur.execute("SELECT id, quantity FROM carts WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    existing = cur.fetchone()

    if existing:
        new_quantity = existing[1] + quantity
        cur.execute("UPDATE carts SET quantity=%s WHERE id=%s", (new_quantity, existing[0]))
    else:
        cur.execute("INSERT INTO carts (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (user_id, product_id, quantity))

    db.commit()
    cur.close()
    log_action(user_id, f"Thêm sản phẩm {product_id} vào giỏ hàng")
    return jsonify({"message": "Thêm vào giỏ hàng thành công"})


@cart_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def remove_from_cart(id):
    db = get_db()
    cur = db.cursor()
    user_id = g.user["id"]

    cur.execute("SELECT * FROM carts WHERE id=%s AND user_id=%s", (id, user_id))
    cart_item = cur.fetchone()

    if not cart_item:
        cur.close()
        return jsonify({"error": "Không tìm thấy sản phẩm trong giỏ hàng"}), 404

    cur.execute("DELETE FROM carts WHERE id=%s", (id,))
    db.commit()
    cur.close()
    log_action(user_id, "Xoá sản phẩm")
    return jsonify({"message": "Xóa khỏi giỏ hàng thành công"})
