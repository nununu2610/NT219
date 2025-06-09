import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, g, jsonify
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
     origins=["http://localhost:8000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     automatic_options=True)

with app.app_context():
    init_db()

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
    app.run(port=30000, debug=True)
