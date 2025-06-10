import sys
import os
from dotenv import load_dotenv
load_dotenv()
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
     origins=["http://localhost:8000", "https://nt219-xa3k.onrender.com", "https://flask-backend-s1fn.onrender.com", "https://api-security-ggok.onrender.com/"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     automatic_options=True)

@app.before_first_request
def initialize_database():
    init_db()

# @app.route('/')
# def index():
#     return "Hello, Trang chủ!"

@app.route('/debug-tables')
def debug_tables():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    cur.close()
    return jsonify([table[0] for table in tables])


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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)