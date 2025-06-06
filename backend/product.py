from flask import Blueprint, request, jsonify, g
from middleware import token_required, require_role
from db import get_db
from utils import encrypt, decrypt

product_bp = Blueprint('product', __name__)

# Ghi log vào bảng logs
def log_action(user_id, action):
    db = get_db()
    db.execute("INSERT INTO logs (user_id, action) VALUES (?, ?)", (user_id, action))
    db.commit()

# Xem chi tiết sản phẩm theo ID
@product_bp.route('/products/<int:id>', methods=['GET'])
@token_required
def get_product_by_id(id):
    try:
        db=get_db()
        row = db.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
        if not row:
            return jsonify({"error": "Không tìm thấy sản phẩm"}), 404
        
        product = {
            "id": row["id"],
            "name": decrypt(row["name"]),
            "description": decrypt(row["description"]) if row["description"] else "",
            "price": row["price"]
        }

        log_action(g.user["id"], f"Xem sản phẩm i={id}")
        return jsonify(product)
    except Exception as e:
        print ("Lỗi:", e)
        return jsonify({"error": "Không thể lấy sản phẩm"}), 500

# Lấy danh sách tất cả sản phẩm (ai cũng xem được)
@product_bp.route('/products', methods=['GET', 'OPTIONS'])
@token_required
def get_products():


    try:
        db = get_db()
        rows = db.execute("SELECT * FROM products").fetchall()
        products = []

        for row in rows:
            try:
                name = decrypt(row["name"])
                description = decrypt(row["description"]) if row["description"] else ""
            except Exception as e:
                print(f"Lỗi decrypt sản phẩm id={row['id']}: {e}")
                # Nếu decrypt lỗi, dùng thẳng dữ liệu gốc
                name = row["name"]
                description = row["description"] if row["description"] else ""

            products.append({
                "id": row["id"],
                "name": name,
                "description": description,
                "price": row["price"]
            })

        log_action(g.user["id"], "Xem danh sách sản phẩm")
        return jsonify(products)
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể lấy danh sách sản phẩm"}), 500


# Thêm sản phẩm (chỉ admin)
@product_bp.route('/products', methods=['POST', 'OPTIONS'])
@token_required
@require_role('admin')
def add_product():


    try:
        data = request.get_json()
        name = encrypt(data["name"])
        description = encrypt(data.get("description", ""))
        price = data["price"]

        db = get_db()
        db.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                   (name, description, price))
        db.commit()

        log_action(g.user["id"], f"Thêm sản phẩm: {data['name']}")
        return jsonify({"message": "Thêm sản phẩm thành công"})
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể thêm sản phẩm"}), 500

# Cập nhật sản phẩm (chỉ admin)
@product_bp.route('/products/<int:id>', methods=['PUT', 'OPTIONS'])
@token_required
@require_role('admin')
def update_product(id):
    try:
        data = request.get_json()
        name = encrypt(data["name"])
        description = encrypt(data.get("description", ""))
        price = data["price"]

        db = get_db()
        db.execute("UPDATE products SET name=?, description=?, price=? WHERE id=?",
                   (name, description, price, id))
        db.commit()

        log_action(g.user["id"], f"Cập nhật sản phẩm id={id}")
        return jsonify({"message": "Cập nhật sản phẩm thành công"})
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể cập nhật sản phẩm"}), 500

# Xóa sản phẩm (chỉ admin)
@product_bp.route('/products/<int:id>', methods=['DELETE', 'OPTIONS'])
@token_required
@require_role('admin')
def delete_product(id):
    try:
        db = get_db()
        db.execute("DELETE FROM products WHERE id=?", (id,))
        db.commit()

        log_action(g.user["id"], f"Xóa sản phẩm id={id}")
        return jsonify({"message": "Xóa sản phẩm thành công"})
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể xóa sản phẩm"}), 500
