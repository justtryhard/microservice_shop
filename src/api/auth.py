from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET = "SECRET123"
ALGORITHM = "HS256"

security = HTTPBearer()


def create_token(user_id: str):
    return jwt.encode({"sub": user_id}, SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials=Depends(security)):
    return verify_token(credentials.credentials)

