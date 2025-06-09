import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, g, jsonify, render_template
from flask_cors import CORS
from db import init_db, get_db, close_db
from limiter import limiter
from flask_limiter.errors import RateLimitExceeded

from auth import auth_bp
from product import product_bp
from cart import cart_bp
from user import user_bp

app = Flask(__name__)
limiter.init_app(app)  # gắn limiter vào app

CORS(app,
     origins=["http://localhost:8000", "https://nt219-xa3k.onrender.com", "https://flask-backend-s1fn.onrender.com"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     automatic_options=True)

with app.app_context():
    init_db()

# @app.route('/')
# def index():
#     return "Hello, Trang chủ!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/add-product')
def add_product():
    return render_template('add-product.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
    return jsonify({"message": "Bạn đã gửi quá nhiều yêu cầu, vui lòng thử lại sau."}), 429

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=30000, debug=True)