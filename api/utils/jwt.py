import os
from functools import wraps
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException
from api.services.jwt import verify_token, create_access_token
from api.utils.logging import logger


def protected_route(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not request.cookies:
            token = request.headers.get("Authorization")
            token = token.split(" ")[1] if token and "Bearer " in token else None
        else:
            token = request.cookies.get("access_token")
        logger.debug(f"Token from cookies: {token}")
        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: missing token"},
            )

        user = dict(verify_token(token))  # verify_token should raise if invalid
        exp = user.get("exp")
        now = datetime.now()
        logger.debug(f"Now: {now}, Token expiration: {datetime.fromtimestamp(exp)}")

        if (
            not exp
            or datetime.fromtimestamp(
                exp,
            )
            < now
        ):
            return RedirectResponse(url="/login")

        # Refresh token if close to expiration
        if datetime.fromtimestamp(exp) < now + timedelta(minutes=10):
            expires_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
            new_token = create_access_token(
                data={
                    "sub": user["sub"],
                    "role": user.get("role", []),
                },
                expires_delta=timedelta(minutes=expires_minutes),
            )
            result = await func(request, *args, **kwargs)
            if isinstance(result, dict):
                response = JSONResponse(content=result)
            else:
                response = result
            response.set_cookie("access_token", new_token, httponly=True)
            return response

        # No refresh needed
        request.state.user = user
        return await func(request, *args, **kwargs)

    return wrapper


def requires_role(role):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.cookies.get("access_token")
            if not token:
                raise HTTPException(status_code=401, detail="Unauthorized")

            user = verify_token(token)
            roles = user.get("role", [])
            if isinstance(roles, str):
                roles = [roles]

            if role not in roles:
                raise HTTPException(status_code=403, detail="Forbidden")

            request.state.user = user
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator


def visitors(redirect_to):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.cookies.get("access_token")
            if not token:
                return await func(request, *args, **kwargs)

            user = verify_token(token)
            if user:
                return RedirectResponse(url=redirect_to)

            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
