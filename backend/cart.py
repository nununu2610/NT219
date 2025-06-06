from flask import Blueprint, request, jsonify, g
from middleware import token_required
from db import get_db
from utils import decrypt

cart_bp = Blueprint('cart', __name__)

# Lấy danh sách sản phẩm trong giỏ hàng của user
@cart_bp.route('/', methods=['GET'])
@token_required
def get_cart():
    try:
        db = get_db()
        rows = db.execute('''
            SELECT carts.id, products.id AS product_id, products.name, products.price, carts.quantity
            FROM carts
            JOIN products ON carts.product_id = products.id
            WHERE carts.user_id = ?
        ''', (g.user['id'],)).fetchall()

        cart_items = []
        for row in rows:
            try:
                name_decrypted = decrypt(row["name"])
            except Exception as e:
                name_decrypted = row["name"]  # fallback nếu decrypt lỗi
            cart_items.append({
                "cart_id": row["id"],
                "product_id": row["product_id"],
                "name": name_decrypted,
                "price": row["price"],
                "quantity": row["quantity"]
            })

        return jsonify(cart_items)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Thêm sản phẩm vào giỏ hàng
@cart_bp.route('/', methods=['POST'])
@token_required
def add_to_cart():
    data = request.get_json()
    product_id = data["product_id"]
    quantity = data.get("quantity", 1)

    db = get_db()
    db.execute("INSERT INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)",
               (g.user["id"], product_id, quantity))
    db.commit()

    return jsonify({"message": "Đã thêm vào giỏ hàng"})

# Xoá sản phẩm khỏi giỏ hàng theo cart_id
@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
@token_required
def remove_from_cart(cart_id):
    db = get_db()
    db.execute("DELETE FROM carts WHERE id=? AND user_id=?", (cart_id, g.user["id"]))
    db.commit()

    return jsonify({"message": "Đã xóa khỏi giỏ hàng"})

# Cập nhật số lượng sản phẩm trong giỏ hàng theo cart_id
@cart_bp.route('/<int:cart_id>', methods=['PUT'])
@token_required
def update_cart_quantity(cart_id):
    data = request.get_json()
    quantity = data.get("quantity")
    if not quantity or quantity < 1:
        return jsonify({"message": "Số lượng không hợp lệ"}), 400
    
    db = get_db()
    db.execute("UPDATE carts SET quantity = ? WHERE id = ? AND user_id = ?", (quantity, cart_id, g.user["id"]))
    db.commit()
    return jsonify({"message": "Cập nhật số lượng thành công"})
