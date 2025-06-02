from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.services.user_service import get_user
from fastapi import HTTPException
from api.utils.security import verify_password
from api.utils.jwt import create_access_token


jwt_router = APIRouter(prefix="/jwt", tags=["jwt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/jwt/token")


@jwt_router.post("/token")
async def jwt_login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and return a JWT token (OAuth2-compatible).
    """
    user = get_user(username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        data={
            "sub": user.username,
            "uid": str(user.id),
        }
    )

    return {"access_token": token, "token_type": "bearer"}
