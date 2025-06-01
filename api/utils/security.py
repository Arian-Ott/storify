from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Request, HTTPException
from functools import wraps
from datetime import datetime, timedelta
import os

from api.services.user_service import get_user

crypto_context = CryptContext(schemes=["argon2"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS512")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable not set")

def protected_route(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract Request from args or kwargs
        request: Request = kwargs.get("request")
        if request is None:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        if request is None:
            raise HTTPException(status_code=400, detail="Request object not found")

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

        token = auth_header.split(" ")[1]

        # Decode and validate JWT
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

        now_ts = int(datetime.now().timestamp())
        if payload.get("exp", 0) < now_ts:
            raise HTTPException(status_code=401, detail="Token has expired")
        if payload.get("iat", 0) > now_ts:
            raise HTTPException(status_code=401, detail="Token not yet valid")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing subject (sub) claim")

        user = get_user(user_id=user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Inject payload into kwargs if desired
        kwargs["token_payload"] = payload
        return await func(*args, **kwargs)

    return wrapper
