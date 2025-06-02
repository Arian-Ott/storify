import os
from functools import wraps
from datetime import datetime, timedelta, timezone
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from api.services.jwt import verify_token, create_access_token

def protected_route(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.cookies.get("access_token")
        

        user = verify_token(token)
        if not user:
            return "AAAAA"

        exp = user.get("exp")
        now = datetime.now(timezone.utc)
        if not exp or datetime.fromtimestamp(exp, tz=timezone.utc) < now:
            return "AAAAA"

        # Renew token if it's expiring soon
        if datetime.fromtimestamp(exp, tz=timezone.utc) < now + timedelta(minutes=10):
            expires_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
            new_token = create_access_token(
                data={
                    "sub": user["sub"],
                    "role": user.get("role", []),
                    "uid": user["uid"],
                },
                expires_delta=timedelta(minutes=expires_minutes),
            )
            response = RedirectResponse(url=request.url.path)
            response.set_cookie("access_token", new_token, httponly=True)
            return response

        request.state.user = user
        return await func(request, *args, **kwargs)

    return wrapper


def requires_role(role):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.cookies.get("access_token")
            user = verify_token(token)

            if not user or "role" not in user or role not in user["role"]:
                raise HTTPException(status_code=403, detail="Forbidden")

            request.state.user = user
            return await func(request, *args, **kwargs)

        return wrapper
    return decorator