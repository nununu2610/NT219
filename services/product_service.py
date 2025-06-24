from flask import Blueprint, request, jsonify, g
from models.db import get_db
from models.log_model import log_action
from crypto_utils.aes_utils import encrypt, decrypt
from middleware.auth_check import token_required, require_role

product_bp = Blueprint('product', __name__, url_prefix='/products')

# ✅ Lấy danh sách tất cả sản phẩm
@product_bp.route('/', methods=['GET'])
@token_required
def get_products():
    db = get_db()
    rows = db.execute("SELECT * FROM products").fetchall()
    products = []
    for row in rows:
        products.append({
            "id": row["id"],
            "name": decrypt(row["name"]),
            "description": decrypt(row["description"]),
            "price": row["price"]
        })
    return jsonify(products), 200

# ✅ Thêm sản phẩm mới (yêu cầu quyền admin)
@product_bp.route('/', methods=['POST'])
@token_required
@require_role('admin')
def add_product():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description") or ""
    price = data.get("price")

    if not name or price is None:
        return jsonify({"message": "Thiếu tên hoặc giá sản phẩm"}), 400

    try:
        db = get_db()
        db.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                   (encrypt(name), encrypt(description), price))
        db.commit()
        log_action(g.user["id"], f"Thêm sản phẩm: {name}")
        return jsonify({"message": "Thêm sản phẩm thành công"}), 201
    except Exception as e:
        print("❌ Lỗi khi thêm sản phẩm:", str(e))
        return jsonify({"message": "Lỗi thêm sản phẩm"}), 500

# ✅ Cập nhật sản phẩm theo id
@product_bp.route('/<int:product_id>', methods=['PUT'])
@token_required
@require_role('admin')
def update_product(product_id):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description") or ""
    price = data.get("price")

    if not name or price is None:
        return jsonify({"message": "Thiếu tên hoặc giá sản phẩm"}), 400

    try:
        db = get_db()
        result = db.execute("UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
                            (encrypt(name), encrypt(description), price, product_id))
        db.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Không tìm thấy sản phẩm"}), 404

        log_action(g.user["id"], f"Cập nhật sản phẩm ID {product_id}")
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        print("❌ Lỗi khi cập nhật sản phẩm:", str(e))
        return jsonify({"message": "Lỗi khi cập nhật sản phẩm"}), 500

# ✅ Xóa sản phẩm theo ID
@product_bp.route('/<int:product_id>', methods=['DELETE'])
@token_required
@require_role('admin')
def delete_product(product_id):
    try:
        db = get_db()
        result = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        db.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Không tìm thấy sản phẩm"}), 404

        log_action(g.user["id"], f"Xóa sản phẩm ID {product_id}")
        return jsonify({"message": "Xóa sản phẩm thành công"}), 200
    except Exception as e:
        print("❌ Lỗi khi xóa sản phẩm:", str(e))
        return jsonify({"message": "Lỗi khi xóa sản phẩm"}), 500
