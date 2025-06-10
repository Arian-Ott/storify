from fastapi import APIRouter
from api.schemas.user_schemas import UserCreate, UserMultipartCreate
from api.services.user_service import create_user, delete_user, get_user, change_password
from api.utils.jwt import create_access_token
from api.utils.security import verify_password
from fastapi import HTTPException
from api.utils.jwt import protected_route
from fastapi import Depends
from fastapi import Request
from api.routes.jwt import oauth2_bearer
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Form
from api.utils.jwt import visitors

user_router = APIRouter(prefix="/auth", tags=["users"])

@user_router.post("/users/change_password/multipart/")
@protected_route
async def route_change_password_multipart(
    request: Request,
    current_password: str = Form(..., min_length=8),
    new_password: str = Form(..., min_length=8),
    confirm_new_password: str = Form(..., min_length=8),
):
    """
    Change the password of the authenticated user using multipart form data.
    """
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    if not current_password or not new_password:
        raise HTTPException(status_code=400, detail="Old and new passwords are required")
    try:
        change_password(
            request.state.user["sub"],
         
            new_password,
        )
        resp = RedirectResponse(
            url="/dashboard",
            status_code=303,
            headers={"X-Success-Message": "Password changed successfully"},
        )
        resp.delete_cookie("access_token")
        return resp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

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


@user_router.post("/users/multipart/")
async def route_create_user_multipart(
    request: Request,
    username: str = Form(..., min_length=3, max_length=50),
    password: str = Form(..., min_length=8),
):
    """
    Create a new user using multipart form data.
    """

    try:
        user = UserMultipartCreate(username=username, password=password)
        create_user(user)
        return RedirectResponse(
            "/login",
            status_code=303,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@user_router.delete("/users/")
@protected_route
async def route_delete_user(request: Request, token=Depends(oauth2_bearer)):
    try:
        user = request.state.user
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        print(user["sub"])
        delete_user(user["sub"])
        resp = JSONResponse(
            content={"detail": "User deleted successfully"},
            status_code=204,
        )
        resp.delete_cookie("access_token")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}") from e


@user_router.post("/users/login")
async def route_login_user(
    username: str = Form(..., min_length=3, max_length=50),
    password: str = Form(..., min_length=8),
):
    """
    Login a user and return a JWT token.
    """

    try:
        user = get_user(username=username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.password):
            resp = RedirectResponse(
                url="/login",
                status_code=303,
            )
            resp.delete_cookie("access_token")

            return resp

        token = create_access_token(
            data={
                "sub": str(user.id),
                "username": user.username,
            }
        )

        response = RedirectResponse(
            url="/dashboard",
            status_code=303,
        )

        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=30 * 60,
        )

        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}") from e
