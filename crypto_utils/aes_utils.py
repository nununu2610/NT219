import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# ⚠️ Load biến môi trường ngay trong file này
load_dotenv()

key = os.getenv("AES_KEY")
if not key:
    raise ValueError("Thiếu biến môi trường AES_KEY!")

fernet = Fernet(key.encode())

def encrypt(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt(cipher):
    return fernet.decrypt(cipher.encode()).decode()
