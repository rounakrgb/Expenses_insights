from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()

def create_token(username: str):
    payload = {"sub": username}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return {"username": username}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
