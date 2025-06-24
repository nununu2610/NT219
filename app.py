print("✅ Đang chạy file app.py")

import os
from flask import Flask, render_template, send_file
from flask_cors import CORS
from middleware.rate_limit import limiter
from gateway.gateway import gateway_bp
from models.db import init_db, close_db
from dotenv import load_dotenv
load_dotenv()
print("🔐 AES_KEY =", os.getenv("AES_KEY"))


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_AS_ASCII'] = False  # Cho phép tiếng Việt trong JSON

CORS(app)
limiter.init_app(app)

# ✅ Khởi tạo CSDL
with app.app_context():
    init_db()

# ✅ HTML giao diện người dùng
@app.route('/')
def index_page():
    print("🔥 Truy cập index.html")
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/add-product')
def add_product():
    return render_template('add-product.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route("/navbar")
def navbar():
    return send_file("templates/navbar.html")

# ✅ Đăng ký toàn bộ API qua Gateway
app.register_blueprint(gateway_bp)

# ✅ Đảm bảo đóng DB sau mỗi request
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    print("🚀 Flask đang chạy ở http://localhost:5000")
    app.run(debug=True)
