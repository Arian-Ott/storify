import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from api.utils.logging import logger

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS512")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now()})

    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    logger.debug(f"Verifying token: {token}")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


def has_role(token: str, role: str) -> bool:
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    payload = verify_token(token)
    user_roles = payload.get("role", [])
    if isinstance(user_roles, str):  # if role is a string, make it a list
        user_roles = [user_roles]
    return role in user_roles
