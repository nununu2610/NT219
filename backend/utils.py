from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()


KEY = os.environ.get("AES_KEY")
if not KEY:
    raise Exception("Thiếu AES_KEY trong biến môi trường!")

fernet = Fernet(KEY.encode() if isinstance(KEY, str) else KEY)

def encrypt(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()
