
from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

ALGORITHM = "HS256"

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
