import sqlite3

conn = sqlite3.connect('mydb.sqlite')
cursor = conn.cursor()

# Thêm cột refresh_token nếu chưa có
try:
    cursor.execute("ALTER TABLE users ADD COLUMN refresh_token TEXT;")
    print("Đã thêm cột refresh_token vào bảng users.")
except sqlite3.OperationalError as e:
    print("Lỗi:", e)

conn.commit()
conn.close()
