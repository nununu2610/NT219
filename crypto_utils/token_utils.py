import jwt, datetime

ACCESS_SECRET = "supersecret"
REFRESH_SECRET = "refreshsecret"

def generate_access_token(user):
    payload = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, ACCESS_SECRET, algorithm="HS256")

def generate_refresh_token(user):
    payload = {
        "id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, REFRESH_SECRET, algorithm="HS256")

def decode_token(token, is_refresh=False):
    key = REFRESH_SECRET if is_refresh else ACCESS_SECRET
    return jwt.decode(token, key, algorithms=["HS256"])
