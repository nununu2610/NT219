import sqlite3
import os

# Đường dẫn đến file cơ sở dữ liệu
db_path = "mydb.sqlite"

# In ra đường dẫn tuyệt đối để xác nhận đúng file
print("📂 Kết nối SQLite tại:", os.path.abspath(db_path))

# Kết nối đến CSDL
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Lấy danh sách các bảng
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("📋 Danh sách các bảng hiện có:")
for table in tables:
    print("✅", table[0])

conn.close()
