import sqlite3
import os

db_path = os.path.abspath("mydb.sqlite")
print(f"📂 Kết nối CSDL tại: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Kiểm tra xem cột "revoked" đã tồn tại chưa
cursor.execute("PRAGMA table_info(refresh_tokens)")
columns = [col[1] for col in cursor.fetchall()]

if "revoked" not in columns:
    print("🔧 Thêm cột 'revoked' vào bảng 'refresh_tokens'...")
    cursor.execute("ALTER TABLE refresh_tokens ADD COLUMN revoked INTEGER DEFAULT 0")
    conn.commit()
    print("✅ Thêm thành công!")
else:
    print("✅ Cột 'revoked' đã tồn tại.")

conn.close()
