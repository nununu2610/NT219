from flask import Blueprint, request, jsonify, g
from middleware import token_required, require_role
from db import get_db
from utils import encrypt, decrypt

product_bp = Blueprint('product', __name__)

# Ghi log vào bảng logs
def log_action(user_id, action):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO logs (user_id, action) VALUES (%s, %s)", (user_id, action))
    db.commit()
    cur.close()

@product_bp.route('/products/<int:id>', methods=['GET'])
@token_required
def get_product_by_id(id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM products WHERE id=%s", (id,))
        row = cur.fetchone()
        cur.close()

        if not row:
            return jsonify({"error": "Không tìm thấy sản phẩm"}), 404

        product = {
            "id": row[0],
            "name": decrypt(row[1]),
            "description": decrypt(row[2]) if row[2] else "",
            "price": row[3]
        }

        log_action(g.user["id"], f"Xem sản phẩm id={id}")
        return jsonify(product)
    except Exception as e:
        print("Lỗi:", e)
        return jsonify({"error": "Không thể lấy sản phẩm"}), 500


@product_bp.route('/products', methods=['GET', 'OPTIONS'])
@token_required
def get_products():
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        cur.close()

        products = []
        for row in rows:
            try:
                name = decrypt(row[1])
                description = decrypt(row[2]) if row[2] else ""
            except Exception as e:
                print(f"Lỗi decrypt sản phẩm id={row[0]}: {e}")
                name = row[1]
                description = row[2] if row[2] else ""

            products.append({
                "id": row[0],
                "name": name,
                "description": description,
                "price": row[3]
            })

        log_action(g.user["id"], "Xem danh sách sản phẩm")
        return jsonify(products)
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể lấy danh sách sản phẩm"}), 500


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
        cur = db.cursor()
        cur.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
                    (name, description, price))
        db.commit()
        cur.close()

        log_action(g.user["id"], f"Thêm sản phẩm: {data['name']}")
        return jsonify({"message": "Thêm sản phẩm thành công"})
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể thêm sản phẩm"}), 500


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
        cur = db.cursor()
        cur.execute("UPDATE products SET name=%s, description=%s, price=%s WHERE id=%s",
                    (name, description, price, id))
        db.commit()
        cur.close()

        log_action(g.user["id"], f"Cập nhật sản phẩm id={id}")
        return jsonify({"message": "Cập nhật sản phẩm thành công"})
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể cập nhật sản phẩm"}), 500


@product_bp.route('/products/<int:id>', methods=['DELETE', 'OPTIONS'])
@token_required
@require_role('admin')
def delete_product(id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM products WHERE id=%s", (id,))
        db.commit()
        cur.close()

        log_action(g.user["id"], f"Xóa sản phẩm id={id}")
        return jsonify({"message": "Xóa sản phẩm thành công"})
    except Exception as e:
        print("LỖI:", e)
        return jsonify({"error": "Không thể xóa sản phẩm"}), 500
