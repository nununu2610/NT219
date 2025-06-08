from app import app  # import biến app Flask trực tiếp
from db import init_db

with app.app_context():
    init_db()
    print("Database initialized.")
