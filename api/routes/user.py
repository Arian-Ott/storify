from fastapi import APIRouter
from api.schemas.user_schemas import UserCreate
from api.services.user_service import create_user
from fastapi import HTTPException
from api.utils.jwt import protected_route
from fastapi import Depends
from fastapi import Request
from api.routes.jwt import oauth2_bearer
from api.utils.logging import logger

user_router = APIRouter(prefix="/auth", tags=["users"])


@user_router.post("/users/", status_code=201)
async def route_create_user(user: UserCreate):
    """
    Create a new user.
    """
    try:
        usr = create_user(user)
        return usr
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@user_router.delete("/users/")
@protected_route
async def route_delete_user(request: Request, token=Depends(oauth2_bearer)):
    logger.debug(f"Request user: {request.state.user}")
    logger.debug(f"Token: {token}")
    return "AA"
