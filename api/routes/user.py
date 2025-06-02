from fastapi import APIRouter
from api.schemas.user_schemas import UserCreate
from api.services.user_service import create_user

user_router = APIRouter(prefix="/auth", tags=["users"])


@user_router.post("/users/", status_code=201)
async def route_create_user(user: UserCreate):
    """
    Create a new user.
    """
    usr = create_user(user)
    return usr
