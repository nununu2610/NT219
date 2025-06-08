import secrets
import datetime
import jwt
from db import get_db

REFRESH_SECRET_KEY = "refreshsecret"

def generate_refresh_token(user_id):
    token = jwt.encode({
        "id": user_id,
        "jti": secrets.token_hex(8),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2)
    }, REFRESH_SECRET_KEY, algorithm="HS256")

    return token if isinstance(token, str) else token.decode()


def save_refresh_token(db, user_id, token):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=7)  # hoặc thời gian bạn muốn
    db.execute(
        "INSERT INTO refresh_tokens (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, user_id, expires_at)
    )
    db.commit()



def revoke_refresh_token(db, token):
    print("Revoke refresh token:", token)
    result = db.execute("UPDATE refresh_tokens SET revoked = 1 WHERE token = ?", (token,))
    db.commit()
    print("Updated rows:", result.rowcount)

