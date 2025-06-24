import jwt, datetime

REFRESH_SECRET_KEY = "refreshsecret"

def generate_refresh_token(user_id):
    return jwt.encode({"id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)}, REFRESH_SECRET_KEY, algorithm="HS256")

def save_refresh_token(db, user_id, token):
    db.execute("INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
               (user_id, token, datetime.datetime.utcnow() + datetime.timedelta(days=7)))
    db.commit()

def revoke_refresh_token(db, token):
    db.execute("UPDATE refresh_tokens SET revoked = 1 WHERE token = ?", (token,))
    db.commit()