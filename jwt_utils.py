
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

ALGORITHM = "HS256"

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def current_user(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    