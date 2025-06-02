import os
from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import HTTPException

from datetime import datetime
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    )
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.now()})

    return jwt.encode(to_encode, os.getenv("JWT_SECRET"), algorithm=os.getenv("JWT_ALGORITHM", "HS512"))


def verify_token(token: str):
    print("Verifying token:", token)
    try:
        payload = jwt.decode(
            token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM", "HS512")]
        )
        return payload
    except JWTError:
        raise


def has_role(token: str, role: str):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_role = payload.get("role")

    if role not in user_role:
        return False

    return True